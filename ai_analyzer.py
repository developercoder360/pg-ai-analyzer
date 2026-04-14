#!/usr/bin/env python3
"""
🤖 PostgreSQL AI Column Analyzer
Uses Qwen/Qwen3.6-Plus via OpenRouter for future growth prediction
"""

import os
import json
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_DATABASE", "dumpdata"),
    "user": os.getenv("DB_USERNAME", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}
# PostgreSQL integer types reference
INT_TYPES = {
    "smallint": {
        "bytes": 2,
        "min": -32768,
        "max": 32767,
        "safe_for": "counters, flags, small quantities",
    },
    "integer": {
        "bytes": 4,
        "min": -2147483648,
        "max": 2147483647,
        "safe_for": "user IDs, order IDs, medium quantities",
    },
    "bigint": {
        "bytes": 8,
        "min": -9223372036854775808,
        "max": 9223372036854775807,
        "safe_for": "timestamps, global IDs, high-volume counters",
    },
}


def get_database_schema(conn):
    """Extract comprehensive schema info for AI analysis"""
    schema_data = {}
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # 1. Get all tables with row counts
        cur.execute("""
            SELECT 
                table_name,
                (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
            FROM information_schema.tables t
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        for table in tables:
            table_name = table["table_name"]
            schema_data[table_name] = {
                "columns": [],
                "row_count": 0,
                "bigint_columns": [],
            }
            # 2. Get row count
            try:
                cur.execute(f'SELECT COUNT(*) as cnt FROM "{table_name}"')
                schema_data[table_name]["row_count"] = cur.fetchone()["cnt"]
            except:
                pass
            # 3. Get column details
            cur.execute(
                """
                SELECT 
                    column_name, data_type, character_maximum_length,
                    is_nullable, column_default, is_identity
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """,
                (table_name,),
            )
            for col in cur.fetchall():
                col_info = {
                    "name": col["column_name"],
                    "type": col["data_type"],
                    "nullable": col["is_nullable"] == "YES",
                    "default": col["column_default"],
                    "is_identity": col["is_identity"] == "YES",
                }
                # Add stats for integer columns
                if col["data_type"] in ["bigint", "integer", "smallint"]:
                    try:
                        cur.execute(f'''
                            SELECT MIN("{col["column_name"]}") as min_v, 
                                   MAX("{col["column_name"]}") as max_v,
                                   COUNT(*) as total,
                                   COUNT(DISTINCT "{col["column_name"]}") as unique_v
                            FROM "{table_name}"
                            WHERE "{col["column_name"]}" IS NOT NULL
                        ''')
                        stats = cur.fetchone()
                        col_info["stats"] = {
                            "min": stats["min_v"],
                            "max": stats["max_v"],
                            "total_rows": stats["total"],
                            "unique_values": stats["unique_v"],
                        }
                        # Track bigint columns for optimization
                        if col["data_type"] == "bigint":
                            schema_data[table_name]["bigint_columns"].append(
                                {
                                    "column": col["column_name"],
                                    "stats": col_info["stats"],
                                }
                            )
                    except:
                        pass
                schema_data[table_name]["columns"].append(col_info)
            # 4. Get growth hints (created_at column if exists)
            date_cols = [
                c["name"]
                for c in schema_data[table_name]["columns"]
                if "date" in c["type"].lower() or "time" in c["type"].lower()
            ]
            if date_cols:
                schema_data[table_name]["date_column"] = date_cols[0]
                try:
                    cur.execute(f'''
                        SELECT 
                            MIN({date_cols[0]}) as oldest,
                            MAX({date_cols[0]}) as newest
                        FROM "{table_name}"
                        WHERE {date_cols[0]} IS NOT NULL
                    ''')
                    dates = cur.fetchone()
                    if dates["oldest"] and dates["newest"]:
                        schema_data[table_name]["date_range"] = {
                            "oldest": str(dates["oldest"]),
                            "newest": str(dates["newest"]),
                        }
                except:
                    pass
    return schema_data


def ask_qwen_for_prediction(schema_data, focus_tables=None):
    """Send schema to Qwen/Qwen3.6-Plus via OpenRouter for AI analysis"""
    # Prepare context for AI
    context = f"""
You are a senior database architect specializing in PostgreSQL optimization.
TASK: Analyze the database schema below and predict FUTURE data growth patterns.
Then recommend optimal integer datatypes (smallint/integer/bigint) for each bigint column.
RULES:
1. Consider business logic: user tables grow faster than config tables
2. Auto-increment IDs need 5-10 year buffer
3. Counters that reset can use smaller types
4. External API IDs should stay bigint (unpredictable)
5. Always include safety margin: current_max × 10 < type_limit
6. Prioritize data safety over minor storage savings
OUTPUT FORMAT (strict JSON):
{{
  "analysis": {{
    "high_growth_tables": ["table1", "table2"],
    "stable_tables": ["table3"],
    "reasoning": "brief explanation"
  }},
  "recommendations": [
    {{
      "table": "table_name",
      "column": "column_name",
      "current_type": "bigint",
      "recommended_type": "integer|smallint|bigint",
      "reason": "why this recommendation",
      "growth_prediction": "low|medium|high",
      "years_safe": 5,
      "risk_level": "low|medium|high",
      "bytes_saved_per_row": 4
    }}
  ],
  "warnings": ["any critical warnings"],
  "monitoring_queries": ["SQL queries to track growth"]
}}
DATABASE SCHEMA:
{json.dumps(schema_data, indent=2, default=str, ensure_ascii=False)[:15000]}  # Truncate if too long
Focus tables: {focus_tables if focus_tables else "all tables"}
"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",  # Required by OpenRouter
        "X-Title": "PostgreSQL AI Analyzer",
    }
    payload = {
        "model": "qwen/qwen3.6-plus",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert PostgreSQL database architect. Respond with valid JSON only.",
            },
            {"role": "user", "content": context},
        ],
        "temperature": 0.1,  # Low temperature for consistent, factual responses
        "max_tokens": 4096,
    }
    print(f"🤖 Sending schema to Qwen/Qwen3.6-Plus via OpenRouter...")
    try:
        response = requests.post(
            OPENROUTER_URL, headers=headers, json=payload, timeout=120
        )
        response.raise_for_status()
        result = response.json()
        ai_content = result["choices"][0]["message"]["content"]
        # Parse JSON from AI response (handle markdown code blocks if present)
        if ai_content.startswith("```json"):
            ai_content = ai_content.split("```json")[1].split("```")[0].strip()
        elif ai_content.startswith("```"):
            ai_content = ai_content.split("```")[1].split("```")[0].strip()
        ai_response = json.loads(ai_content)
        print("✅ AI analysis received!")
        return ai_response
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"Raw response: {ai_content[:500]}...")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None


def generate_laravel_migration(ai_recommendations):
    """Generate Laravel migration file from AI recommendations"""
    if not ai_recommendations or "recommendations" not in ai_recommendations:
        return None
    recommendations = [
        r
        for r in ai_recommendations["recommendations"]
        if r["recommended_type"] != "bigint"
    ]
    if not recommendations:
        print("ℹ️ No migrations needed (all columns should remain BIGINT)")
        return None
    ts = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    # Build migration content
    up_changes = ""
    down_changes = ""
    for rec in recommendations:
        up_changes += f"""
            // {rec["table"]}.{rec["column"]}: {rec["current_type"]} → {rec["recommended_type"]}
            // 📈 Growth: {rec["growth_prediction"]} | 🔐 Risk: {rec["risk_level"]} | 📅 Safe for: {rec["years_safe"]} years
            // 💡 Reason: {rec["reason"]}
            Schema::table('{rec["table"]}', function (Blueprint $table) {{
                $table->{rec["recommended_type"].lower()}('{rec["column"]}')->change();
            }});"""
        down_changes += f"""
            // Revert {rec["table"]}.{rec["column"]}
            Schema::table('{rec["table"]}', function (Blueprint $table) {{
                $table->bigInteger('{rec["column"]}')->change();
            }});"""
    migration_content = f"""<?php
/**
 * AI-Generated Migration: PostgreSQL Integer Optimization
 * Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 * Model: Qwen/Qwen3.6-Plus via OpenRouter
 * 
 * 📊 Analysis Summary:
 * - High Growth Tables: {ai_recommendations.get("analysis", {}).get("high_growth_tables", [])}
 * - Warnings: {ai_recommendations.get("warnings", [])}
 */
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;
use Illuminate\\Support\\Facades\\DB;
return new class extends Migration
{{
    /**
     * Run the migrations.
     * OPTIMIZATION: Reduce storage by using smaller integer types
     * SAFETY: All recommendations include 5+ year growth buffer
     */
    public function up(): void
    {{
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        try {{{up_changes}
            DB::commit();
            echo "✅ Migrations applied successfully\\n";
        }} catch (\\Exception $e) {{
            DB::rollBack();
            echo "❌ Migration failed: " . $e->getMessage() . "\\n";
            throw $e;
        }} finally {{
            Schema::enableForeignKeyConstraints();
        }}
    }}
    /**
     * Reverse the migrations.
     * Reverts all columns back to BIGINT for safety.
     */
    public function down(): void
    {{
        Schema::disableForeignKeyConstraints();
        DB::beginTransaction();
        try {{{down_changes}
            DB::commit();
            echo "✅ Rollback completed\\n";
        }} catch (\\Exception $e) {{
            DB::rollBack();
            echo "❌ Rollback failed: " . $e->getMessage() . "\\n";
            throw $e;
        }} finally {{
            Schema::enableForeignKeyConstraints();
        }}
    }}
}};
"""
    # Save to file
    os.makedirs("database/migrations", exist_ok=True)
    filename = f"database/migrations/{ts}_ai_optimize_integers.php"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(migration_content)
    print(f"🎨 Laravel migration saved: {filename}")
    return filename


def export_ai_report(ai_recommendations, schema_summary):
    """Export comprehensive AI analysis report"""
    report = {
        "generated_at": datetime.now().isoformat(),
        "model_used": "qwen/qwen3.6-plus",
        "database": DB_CONFIG["database"],
        "schema_summary": schema_summary,
        "ai_analysis": ai_recommendations,
        "action_items": [],
    }
    # Generate action items
    if ai_recommendations:
        for rec in ai_recommendations.get("recommendations", []):
            if rec["recommended_type"] != "bigint":
                report["action_items"].append(
                    {
                        "action": f"Change {rec['table']}.{rec['column']} to {rec['recommended_type']}",
                        "priority": "high" if rec["risk_level"] == "low" else "medium",
                        "estimated_savings_mb": round(
                            (8 - INT_TYPES[rec["recommended_type"]]["bytes"])
                            * schema_summary.get(rec["table"], {}).get("row_count", 0)
                            / (1024 * 1024),
                            2,
                        ),
                    }
                )
    # Save report
    with open("ai_analysis_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str, ensure_ascii=False)
    print(f"📄 AI Report saved: ai_analysis_report.json")
    # Print summary
    print("\n" + "=" * 60)
    print("🤖 AI ANALYSIS SUMMARY")
    print("=" * 60)
    analysis = ai_recommendations.get("analysis", {})
    print(f"📈 High Growth Tables: {analysis.get('high_growth_tables', [])}")
    print(f"📊 Stable Tables: {analysis.get('stable_tables', [])}")
    print(f"💡 Reasoning: {analysis.get('reasoning', 'N/A')}")
    print(f"\n🎯 Recommendations:")
    for rec in ai_recommendations.get("recommendations", [])[:5]:  # Show top 5
        status = (
            "✅ OPTIMIZE" if rec["recommended_type"] != "bigint" else "⏸️  KEEP BIGINT"
        )
        print(f"  {status} {rec['table']}.{rec['column']} → {rec['recommended_type']}")
        print(
            f"     📈 {rec['growth_prediction']} growth | 🔐 {rec['risk_level']} risk | 📅 {rec['years_safe']}y safe"
        )
    if ai_recommendations.get("warnings"):
        print(f"\n⚠️  Warnings:")
        for w in ai_recommendations["warnings"]:
            print(f"  • {w}")
    print("=" * 60)
    return report


def main():
    print("🚀 PostgreSQL AI Column Analyzer")
    print(f"🤖 Model: Qwen/Qwen3.6-Plus via OpenRouter")
    print(f"📦 Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
    print("-" * 60)
    # Validate API key
    # ✅ NAYA (CORRECTED) CODE:
    if (
        not OPENROUTER_API_KEY
        or "YOUR-KEY" in OPENROUTER_API_KEY
        or len(OPENROUTER_API_KEY) < 20
    ):
        print("❌ OPENROUTER_API_KEY missing ya invalid hai!")
        print(
            "💡 .env file mein apni real key paste karein: OPENROUTER_API_KEY=sk-or-v1-..."
        )
        return
    try:
        # Connect to database
        print("🔌 Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected!")
        # Extract schema
        print("🔍 Extracting database schema...")
        schema_data = get_database_schema(conn)
        # Create summary for report
        schema_summary = {
            table: {
                "row_count": data["row_count"],
                "bigint_columns": len(data["bigint_columns"]),
                "total_columns": len(data["columns"]),
            }
            for table, data in schema_data.items()
        }
        print(f"📊 Found {len(schema_data)} tables, analyzing bigint columns...")
        # Ask AI for predictions
        ai_response = ask_qwen_for_prediction(schema_data)
        if ai_response:
            # Generate outputs
            export_ai_report(ai_response, schema_summary)
            generate_laravel_migration(ai_response)
        else:
            print("⚠️  Could not get AI response. Check API key and try again.")
        conn.close()
        print("\n✅ Analysis complete!")
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection error: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Is PostgreSQL running? (services.msc or pgAdmin)")
        print("  2. Are credentials correct in .env?")
        print("  3. Is port 5432 allowed through firewall?")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
