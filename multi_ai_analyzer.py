#!/usr/bin/env python3
"""
🤖 Multi-AI PostgreSQL Column Analyzer
Uses Qwen + Claude + Gemma via OpenRouter for consensus-based predictions
"""

import os
import json
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Optional
import time

# 🔐 Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_DATABASE', 'dumpdata'),
    'user': os.getenv('DB_USERNAME', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# 🎯 AI Models to consult (in priority order)
AI_MODELS = [
    {
        'id': 'qwen/qwen3.6-plus',
        'name': 'Qwen 3.6 Plus',
        'temp': 0.1,
        'max_tokens': 4096,
        'strength': 'Technical analysis & code generation'
    },
    {
        'id': 'anthropic/claude-opus-4.6-fast',
        'name': 'Claude Opus 4.6 Fast',
        'temp': 0.2,
        'max_tokens': 4096,
        'strength': 'Safety-first reasoning & risk assessment'
    },
    {
        'id': 'openrouter/elephant-alpha',
        'name': 'Elephant Alpha',
        'temp': 0.1,
        'max_tokens': 2048,
        'strength': 'Fast validation & consensus checking'
    }
]

INT_TYPES = {
    'smallint': {'bytes': 2, 'min': -32768, 'max': 32767, 'safe_for': 'counters, flags'},
    'integer': {'bytes': 4, 'min': -2147483648, 'max': 2147483647, 'safe_for': 'user IDs, order IDs'},
    'bigint': {'bytes': 8, 'min': -9223372036854775808, 'max': 9223372036854775807, 'safe_for': 'timestamps, global IDs'}
}

def get_database_schema(conn) -> Dict:
    """Extract comprehensive schema info for AI analysis"""
    schema_data = {}
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Get all tables
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [row['table_name'] for row in cur.fetchall()]
        
        for table_name in tables:
            schema_data[table_name] = {'columns': [], 'row_count': 0, 'bigint_columns': []}
            
            # Row count
            try:
                cur.execute(f'SELECT COUNT(*) as cnt FROM "{table_name}"')
                schema_data[table_name]['row_count'] = cur.fetchone()['cnt']
            except:
                pass
            
            # Column details
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default, is_identity
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """, (table_name,))
            
            for col in cur.fetchall():
                col_info = {
                    'name': col['column_name'],
                    'type': col['data_type'],
                    'nullable': col['is_nullable'] == 'YES',
                    'is_identity': col['is_identity'] == 'YES'
                }
                
                # Stats for integer columns
                if col['data_type'] in ['bigint', 'integer', 'smallint']:
                    try:
                        cur.execute(f'''
                            SELECT MIN("{col['column_name']}") as min_v, 
                                   MAX("{col['column_name']}") as max_v,
                                   COUNT(*) as total
                            FROM "{table_name}"
                            WHERE "{col['column_name']}" IS NOT NULL
                        ''')
                        stats = cur.fetchone()
                        col_info['stats'] = {
                            'min': stats['min_v'],
                            'max': stats['max_v'],
                            'total_rows': stats['total']
                        }
                        if col['data_type'] == 'bigint':
                            schema_data[table_name]['bigint_columns'].append({
                                'column': col['column_name'],
                                'stats': col_info['stats']
                            })
                    except:
                        pass
                
                schema_data[table_name]['columns'].append(col_info)
            
            # Date column for growth analysis
            date_cols = [c['name'] for c in schema_data[table_name]['columns'] 
                        if 'date' in c['type'].lower() or 'time' in c['type'].lower()]
            if date_cols:
                schema_data[table_name]['date_column'] = date_cols[0]
    
    return schema_data

def build_ai_prompt(schema_data: Dict, focus_tables: List[str] = None) -> str:
    """Build a structured prompt for AI models"""
    
    focus_note = f"\nFocus on these tables: {', '.join(focus_tables)}" if focus_tables else ""
    
    return f"""You are a senior PostgreSQL database architect.

TASK: Analyze the schema below and predict FUTURE data growth. Recommend optimal integer types (smallint/integer/bigint) for each bigint column.

RULES:
1. Safety first: current_max × 10 < type_limit for auto-increment IDs
2. Consider business context: user tables grow faster than config tables
3. External API IDs → always keep BIGINT (unpredictable)
4. Counters that reset → can use SMALLINT
5. Include 3-5 year growth buffer minimum
6. Prioritize data integrity over minor storage savings

OUTPUT FORMAT (strict JSON):
{{
  "analysis": {{
    "high_growth_tables": ["table1"],
    "stable_tables": ["table2"],
    "reasoning": "brief explanation"
  }},
  "recommendations": [
    {{
      "table": "table_name",
      "column": "column_name",
      "current_type": "bigint",
      "recommended_type": "integer|smallint|bigint",
      "reason": "why",
      "growth_prediction": "low|medium|high",
      "years_safe": 5,
      "risk_level": "low|medium|high",
      "bytes_saved_per_row": 4
    }}
  ],
  "warnings": ["critical warnings"],
  "monitoring_queries": ["SQL to track growth"]
}}

DATABASE SCHEMA (truncated if large):
{json.dumps(schema_data, indent=2, default=str, ensure_ascii=False)[:12000]}
{focus_note}

Respond with valid JSON only. No markdown, no explanations outside JSON."""

def query_ai_model(model_config: Dict, prompt: str) -> Optional[Dict]:
    """Query a single AI model via OpenRouter"""
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "Multi-AI PostgreSQL Analyzer"
    }
    
    payload = {
        "model": model_config['id'],
        "messages": [
            {"role": "system", "content": "You are an expert PostgreSQL architect. Respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": model_config['temp'],
        "max_tokens": model_config['max_tokens']
    }
    
    print(f"  🤖 Querying {model_config['name']} ({model_config['id']})...")
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=180)
        response.raise_for_status()
        
        result = response.json()
        ai_content = result['choices'][0]['message']['content']
        
        # Parse JSON (handle markdown code blocks)
        if '```json' in ai_content:
            ai_content = ai_content.split('```json')[1].split('```')[0].strip()
        elif '```' in ai_content:
            ai_content = ai_content.split('```')[1].split('```')[0].strip()
        
        parsed = json.loads(ai_content)
        print(f"  ✅ {model_config['name']} responded successfully")
        return {'model': model_config['id'], 'response': parsed, 'status': 'success'}
        
    except requests.exceptions.Timeout:
        print(f"  ⏰ {model_config['name']} timed out")
        return {'model': model_config['id'], 'error': 'timeout', 'status': 'failed'}
    except requests.exceptions.RequestException as e:
        print(f"  ❌ {model_config['name']} API error: {str(e)[:100]}")
        return {'model': model_config['id'], 'error': str(e), 'status': 'failed'}
    except json.JSONDecodeError as e:
        print(f"  ❌ {model_config['name']} JSON parse error")
        return {'model': model_config['id'], 'error': 'invalid_json', 'status': 'failed'}
    except Exception as e:
        print(f"  ❌ {model_config['name']} unexpected error: {e}")
        return {'model': model_config['id'], 'error': str(e), 'status': 'failed'}

def consolidate_recommendations(ai_responses: List[Dict]) -> Dict:
    """Consolidate multiple AI responses into consensus recommendations"""
    
    successful = [r for r in ai_responses if r['status'] == 'success']
    
    if not successful:
        return {
            'error': 'No AI models responded successfully',
            'recommendations': [],
            'warnings': ['All AI queries failed - using fallback heuristics']
        }
    
    # Collect all recommendations
    all_recs = []
    for resp in successful:
        recs = resp['response'].get('recommendations', [])
        for rec in recs:
            rec['_source_model'] = resp['model']
            all_recs.append(rec)
    
    # Group by table.column
    from collections import defaultdict
    grouped = defaultdict(list)
    for rec in all_recs:
        key = f"{rec['table']}.{rec['column']}"
        grouped[key].append(rec)
    
    # Consensus logic
    consolidated = []
    for key, recs in grouped.items():
        # Count votes for each recommended_type
        votes = {}
        for r in recs:
            t = r['recommended_type']
            votes[t] = votes.get(t, 0) + 1
        
        # Pick the most voted type (tie-breaker: prefer larger type for safety)
        best_type = max(votes.keys(), key=lambda t: (votes[t], -INT_TYPES.get(t, {}).get('bytes', 0)))
        
        # Calculate consensus metrics
        consensus_strength = votes[best_type] / len(recs)
        sources = [r['_source_model'] for r in recs if r['recommended_type'] == best_type]
        
        # Pick the most detailed reason
        best_rec = max([r for r in recs if r['recommended_type'] == best_type], 
                      key=lambda r: len(r.get('reason', '')))
        
        consolidated.append({
            'table': best_rec['table'],
            'column': best_rec['column'],
            'current_type': best_rec['current_type'],
            'recommended_type': best_type,
            'reason': best_rec['reason'],
            'consensus_strength': round(consensus_strength * 100),
            'agreeing_models': sources,
            'growth_prediction': best_rec.get('growth_prediction', 'unknown'),
            'years_safe': best_rec.get('years_safe', 3),
            'risk_level': 'high' if consensus_strength < 0.6 else best_rec.get('risk_level', 'medium'),
            'bytes_saved_per_row': INT_TYPES.get(best_type, {}).get('bytes', 8)
        })
    
    # Collect warnings from all models
    all_warnings = []
    for resp in successful:
        all_warnings.extend(resp['response'].get('warnings', []))
    
    # Collect high-growth tables (consensus)
    high_growth = []
    for resp in successful:
        high_growth.extend(resp['response'].get('analysis', {}).get('high_growth_tables', []))
    high_growth = list(set(high_growth))  # Unique
    
    return {
        'models_consulted': len(successful),
        'total_recommendations': len(consolidated),
        'consensus_threshold': 60,  # 60% agreement minimum
        'analysis': {
            'high_growth_tables': high_growth,
            'reasoning': f"Consensus from {len(successful)} AI models"
        },
        'recommendations': consolidated,
        'warnings': list(set(all_warnings)),
        'model_details': [
            {'model': r['model'], 'status': r['status']} 
            for r in ai_responses
        ]
    }

def generate_laravel_migration(consolidated: Dict) -> Optional[str]:
    """Generate Laravel migration from consolidated recommendations"""
    
    if 'error' in consolidated or not consolidated.get('recommendations'):
        return None
    
    # Filter: only optimize if consensus >= 60% AND risk != high
    to_migrate = [
        r for r in consolidated['recommendations']
        if r['recommended_type'] != 'bigint' 
        and r['consensus_strength'] >= 60 
        and r['risk_level'] != 'high'
    ]
    
    if not to_migrate:
        print("ℹ️ No migrations meet safety criteria (consensus >= 60% AND risk != high)")
        return None
    
    ts = datetime.now().strftime('%Y_%m_%d_%H%M%S')
    
    up_changes = ""
    down_changes = ""
    
    for rec in to_migrate:
        up_changes += f"""
            // {rec['table']}.{rec['column']}: {rec['current_type']} → {rec['recommended_type']}
            // 🤖 Consensus: {rec['consensus_strength']}% | Models: {', '.join(rec['agreeing_models'])}
            // 📈 Growth: {rec['growth_prediction']} | 🔐 Risk: {rec['risk_level']} | 📅 Safe: {rec['years_safe']}y
            Schema::table('{rec['table']}', function (Blueprint $table) {{
                $table->{rec['recommended_type'].lower()}('{rec['column']}')->change();
            }});"""
        
        down_changes += f"""
            Schema::table('{rec['table']}', function (Blueprint $table) {{
                $table->bigInteger('{rec['column']}')->change();
            }});"""
    
    migration = f'''<?php
/**
 * Multi-AI Consensus Migration: PostgreSQL Integer Optimization
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 * Models: {consolidated['models_consulted']} AI experts consulted
 * Consensus Threshold: {consolidated['consensus_threshold']}%
 * 
 * 📊 Analysis:
 * - High Growth Tables: {consolidated['analysis'].get('high_growth_tables', [])}
 * - Warnings: {consolidated['warnings']}
 */

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;
use Illuminate\\Support\\Facades\\DB;

return new class extends Migration
{{
    public function up(): void
    {{
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        
        try {{{up_changes}
            DB::commit();
        }} catch (\\Exception $e) {{
            DB::rollBack();
            throw $e;
        }} finally {{
            Schema::enableForeignKeyConstraints();
        }}
    }}

    public function down(): void
    {{
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        
        try {{{down_changes}
            DB::commit();
        }} catch (\\Exception $e) {{
            DB::rollBack();
            throw $e;
        }} finally {{
            Schema::enableForeignKeyConstraints();
        }}
    }}
}};
'''
    
    os.makedirs('database/migrations', exist_ok=True)
    filename = f"database/migrations/{ts}_multi_ai_optimize.php"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(migration)
    
    print(f"🎨 Migration saved: {filename}")
    return filename

def export_report(consolidated: Dict, schema_summary: Dict):
    """Export comprehensive multi-AI report"""
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'models_used': [m['id'] for m in AI_MODELS],
        'database': DB_CONFIG['database'],
        'schema_summary': schema_summary,
        'consolidated_analysis': consolidated,
        'action_items': []
    }
    
    # Generate actionable items
    for rec in consolidated.get('recommendations', []):
        if rec['recommended_type'] != 'bigint' and rec['consensus_strength'] >= 60:
            report['action_items'].append({
                'action': f"Change {rec['table']}.{rec['column']} to {rec['recommended_type']}",
                'priority': 'high' if rec['risk_level'] == 'low' else 'medium',
                'consensus': f"{rec['consensus_strength']}%",
                'models': rec['agreeing_models'],
                'estimated_savings_mb': round(
                    (8 - INT_TYPES[rec['recommended_type']]['bytes']) * 
                    schema_summary.get(rec['table'], {}).get('row_count', 0) / (1024*1024), 2
                )
            })
    
    # Save
    os.makedirs('reports', exist_ok=True)
    with open('reports/multi_ai_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str, ensure_ascii=False)
    
    # Print summary
    print("\n" + "="*70)
    print("🤖 MULTI-AI CONSENSUS SUMMARY")
    print("="*70)
    print(f"✅ Models Responded: {consolidated.get('models_consulted', 0)}/{len(AI_MODELS)}")
    print(f"🎯 Recommendations: {consolidated.get('total_recommendations', 0)}")
    
    print(f"\n📈 High Growth Tables: {consolidated['analysis'].get('high_growth_tables', [])}")
    
    print(f"\n🔍 Top Recommendations:")
    for rec in consolidated.get('recommendations', [])[:5]:
        status = "✅" if rec['recommended_type'] != 'bigint' and rec['consensus_strength'] >= 60 else "⏸️"
        print(f"  {status} {rec['table']}.{rec['column']} → {rec['recommended_type']}")
        print(f"     🤖 Consensus: {rec['consensus_strength']}% | 🔐 {rec['risk_level']} risk")
    
    if consolidated.get('warnings'):
        print(f"\n⚠️  Warnings:")
        for w in consolidated['warnings'][:3]:
            print(f"  • {w}")
    
    print("="*70)
    
    return report

def main():
    print("🚀 PostgreSQL Multi-AI Column Analyzer")
    print(f"🤖 Models: {[m['name'] for m in AI_MODELS]}")
    print(f"📦 Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
    print("-"*70)
    
    # Validate API key
    if not OPENROUTER_API_KEY or len(OPENROUTER_API_KEY) < 20:
        print("❌ OPENROUTER_API_KEY not set or invalid in .env!")
        print("💡 Add: OPENROUTER_API_KEY=sk-or-v1-YOUR-KEY")
        return
    
    try:
        # Connect to DB
        print("🔌 Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected!")
        
        # Extract schema
        print("🔍 Extracting schema...")
        schema_data = get_database_schema(conn)
        
        schema_summary = {
            table: {
                'row_count': data['row_count'],
                'bigint_columns': len(data['bigint_columns'])
            }
            for table, data in schema_data.items()
        }
        
        bigint_count = sum(len(d['bigint_columns']) for d in schema_data.values())
        print(f"📊 Found {len(schema_data)} tables, {bigint_count} bigint columns")
        
        # Build prompt
        prompt = build_ai_prompt(schema_data)
        
        # Query all AI models (with small delay to avoid rate limits)
        print("\n🔄 Consulting AI models...")
        ai_responses = []
        
        for i, model in enumerate(AI_MODELS):
            result = query_ai_model(model, prompt)
            ai_responses.append(result)
            if i < len(AI_MODELS) - 1:
                time.sleep(2)  # Rate limit friendly
        
        # Consolidate responses
        print("\n🧠 Consolidating AI responses...")
        consolidated = consolidate_recommendations(ai_responses)
        
        # Generate outputs
        export_report(consolidated, schema_summary)
        generate_laravel_migration(consolidated)
        
        conn.close()
        print("\n✅ Multi-AI analysis complete!")
        
    except psycopg2.OperationalError as e:
        print(f"❌ DB connection error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()