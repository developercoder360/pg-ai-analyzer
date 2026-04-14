# 🤖 PostgreSQL Multi-AI Column Optimizer

> Intelligently optimize your PostgreSQL database storage by leveraging multiple AI models to predict data growth and generate safe Laravel migrations.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-336791)](https://www.postgresql.org/)
[![Laravel](https://img.shields.io/badge/Laravel-10%2B-FF2D20)](https://laravel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Why This Tool?](#-why-this-tool)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Output Examples](#-output-examples)
- [AI Consensus Mechanism](#-ai-consensus-mechanism)
- [Migration Safety](#-migration-safety)
- [Security Best Practices](#-security-best-practices)
- [Troubleshooting](#-troubleshooting)
- [Cost Estimation](#-cost-estimation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The PostgreSQL Multi-AI Column Optimizer is a production-ready Python tool that analyzes your database schema, uses artificial intelligence to predict future data growth patterns, and generates safe Laravel migrations to optimize column types—all while ensuring your data stays protected.

### Key Highlights

- **Multi-AI Consensus**: Queries 3 different AI models and only proceeds when they agree
- **Zero Data Loss Risk**: Only suggests downsizing when mathematically safe for years ahead
- **Laravel Integration**: Generates ready-to-use migrations with automatic rollback support
- **Fully Auditable**: Produces detailed JSON reports for every analysis

---

## 💡 Why This Tool?

### The Problem

Many Laravel applications default to using `BIGINT` columns for auto-incrementing IDs and counters. While safe, this wastes storage:

- `BIGINT` uses **8 bytes** per row (supports up to ~9.2 quintillion)
- `INTEGER` uses **4 bytes** per row (supports up to ~2.1 billion)
- `SMALLINT` uses **2 bytes** per row (supports up to ~32,767)

**Real-world impact:**
```
1 million rows × 4 unnecessary bytes = 4 MB wasted per column
10 million rows × 4 bytes × 5 columns = 200 MB wasted
100 million rows = 2 GB+ of recoverable storage
```

### The Risk

Manually changing column types is dangerous:
- ❌ Downgrading `BIGINT → INTEGER` when max value is 1.5 billion = **data overflow**
- ❌ Not accounting for growth = **migration fails in 6 months**
- ❌ Guessing instead of analyzing = **production incidents**

### The Solution

This tool eliminates guesswork by:
1. ✅ Analyzing actual data ranges and growth rates
2. ✅ Consulting multiple AI models for predictions
3. ✅ Only proceeding when there's consensus (60%+ agreement)
4. ✅ Ensuring 3+ years of safety buffer before limits are reached

---

## ✨ Features

### Core Capabilities

- 🔍 **Deep Schema Analysis**
  - Extracts table structures from `information_schema`
  - Calculates min/max values, row counts, and date ranges
  - Identifies auto-incrementing sequences
  - Tracks historical growth patterns

- 🤖 **Multi-AI Consensus Engine**
  - **Qwen 3.6 Plus**: Fast, cost-effective reasoning
  - **Claude Opus 4.6 Fast**: Advanced pattern recognition
  - **Gemma 4 26B (Free)**: Independent validation
  - Parallel querying via OpenRouter API
  - Weighted voting system with tie-breaker logic

- 📈 **Predictive Growth Analysis**
  - Calculates daily/monthly growth rates
  - Estimates years until type limits are reached
  - Accounts for seasonal variations
  - Flags unpredictable growth patterns

- 🛡️ **Safety-First Recommendations**
  - Requires ≥60% AI consensus before acting
  - Skips high-risk columns (external IDs, payment references)
  - Enforces minimum 3-year safety buffer
  - Prefers larger types when in doubt

- 🎨 **Auto-Generated Laravel Migrations**
  - Full `up()` and `down()` methods
  - Descriptive comments for each change
  - Timestamp-based naming convention
  - Drop-in ready for Laravel projects

- 📊 **Comprehensive Reporting**
  - Structured JSON output for CI/CD integration
  - Per-column risk assessment
  - AI model response details
  - Detailed reasoning logs

---

## 🏗️ How It Works

```
┌─────────────────┐
│  PostgreSQL DB  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   Schema Extractor      │
│  • Tables & columns     │
│  • Row counts & ranges  │
│  • Growth patterns      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   AI Prompt Builder     │
│  • Structures context   │
│  • Adds safety rules    │
│  • Formats for models   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Multi-AI Query Engine  │
│  ┌─────────────────┐   │
│  │ Qwen 3.6 Plus   │   │
│  │ Claude Opus 4.6 │   │
│  │ Gemma 4 26B     │   │
│  └─────────────────┘   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Consensus Analyzer     │
│  • Votes per column     │
│  • Risk assessment      │
│  • Safety validation    │
└────────┬────────────────┘
         │
         ├──────────────────┬───────────────────┐
         ▼                  ▼                   ▼
┌────────────────┐  ┌──────────────┐  ┌────────────────┐
│ Laravel        │  │ JSON Report  │  │ Execution Log  │
│ Migration      │  │              │  │                │
└────────────────┘  └──────────────┘  └────────────────┘
```

### Step-by-Step Process

1. **Connect & Extract**: Queries PostgreSQL for schema metadata and statistics
2. **Analyze Data**: Calculates current usage and growth trends
3. **Build Context**: Creates structured prompts with safety constraints
4. **Query AI Models**: Sends requests to 3 models in parallel via OpenRouter
5. **Validate Responses**: Parses JSON responses and validates recommendations
6. **Build Consensus**: Aggregates votes and applies safety thresholds
7. **Generate Output**: Creates Laravel migration and audit report

---

## 📦 Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | `3.10+` | Uses modern type hints and pattern matching |
| **PostgreSQL** | `12+` | Requires `information_schema` access |
| **OpenRouter API** | Active account | [Get API key](https://openrouter.ai/keys) |
| **Laravel** | `10+` | For using generated migrations |

### Python Packages

All dependencies are listed in `requirements.txt`:
- `psycopg2-binary` — PostgreSQL adapter
- `python-dotenv` — Environment variable management
- `requests` — HTTP client for OpenRouter API

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/pg-ai-analyzer.git
cd pg-ai-analyzer
```

> **Note**: Replace `YOUR_USERNAME` with your actual GitHub username.

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Now edit `.env` with your credentials (see [Configuration](#-configuration) section).

---

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file in the project root:

```bash
# =============================================================================
# 🔐 OpenRouter API Configuration
# =============================================================================
# Get your API key from: https://openrouter.ai/keys
# Keep this secret! Never commit to version control.
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE

# =============================================================================
# 🗄️ PostgreSQL Database Connection
# =============================================================================
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=your_database_name
DB_USERNAME=your_db_user
DB_PASSWORD=your_secure_password

# =============================================================================
# ⚙️ Analysis Configuration (Optional - Defaults Shown)
# =============================================================================

# Minimum percentage of AI models that must agree before generating migration
# Range: 0-100 (Default: 60)
# Higher = Safer but fewer optimizations
AI_CONSENSUS_THRESHOLD=60

# Minimum years a downsized column must remain safe
# Range: 1-10 (Default: 3)
# Higher = More conservative, larger safety buffer
SAFETY_YEARS=3

# Maximum tokens to send to AI models (prevents API errors on huge schemas)
# Range: 1000-30000 (Default: 12000)
# Increase if you have many tables but AI responses are truncated
MAX_SCHEMA_TOKENS=12000

# Enable debug logging (Default: false)
# Set to 'true' to see detailed API requests/responses
DEBUG_MODE=false
```

### Configuration Tips

| Setting | Conservative | Balanced | Aggressive |
|---------|--------------|----------|------------|
| `AI_CONSENSUS_THRESHOLD` | 80% | 60% | 40% |
| `SAFETY_YEARS` | 5 years | 3 years | 1 year |

**Recommendations:**
- **Production databases**: Use conservative settings (80%, 5 years)
- **Development/staging**: Balanced settings are fine (60%, 3 years)
- **Testing/analysis**: Aggressive settings to see more suggestions (40%, 1 year)

---

## 🏃 Usage

### Basic Usage

```bash
# Activate virtual environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the analyzer
python multi_ai_analyzer.py
```

### Expected Console Output

```bash
🚀 PostgreSQL Multi-AI Column Analyzer v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 AI Models: Qwen 3.6 Plus | Claude Opus 4.6 Fast | Gemma 4 26B (Free)
📦 Database: production_db@127.0.0.1:5432
⚙️  Consensus Threshold: 60% | Safety Buffer: 3 years
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/5] 🔌 Connecting to PostgreSQL...
      ✅ Connection successful

[2/5] 🔍 Extracting schema & statistics...
      📊 Found 12 tables with 8 BIGINT columns
      📈 Analyzing growth patterns...
      ✅ Schema analysis complete

[3/5] 🤖 Consulting AI models...
      ⏳ Qwen 3.6 Plus... ✅ Responded (2.3s)
      ⏳ Claude Opus 4.6 Fast... ✅ Responded (3.1s)
      ⏳ Gemma 4 26B (Free)... ✅ Responded (4.7s)

[4/5] 🧠 Building consensus...
      ✅ All 3 models responded successfully
      🎯 Analyzing 8 columns...
      
      Column: users.id
      ├─ Current max: 45,823
      ├─ AI Votes: INTEGER (3/3) - 100% consensus ✅
      ├─ Safety: 127 years until overflow
      └─ Action: Include in migration
      
      Column: orders.id
      ├─ Current max: 1,234,567
      ├─ AI Votes: INTEGER (2/3) - 67% consensus ⚠️
      ├─ Safety: 8 years until overflow
      └─ Action: Include in migration
      
      Column: transactions.external_id
      ├─ Current max: 9,876,543,210
      ├─ AI Votes: Keep BIGINT (3/3) - High risk ⚠️
      ├─ Reason: External API IDs, unpredictable growth
      └─ Action: Skip (safety first)
      
      📋 Final Results: 5 optimizations, 3 skipped

[5/5] 📝 Generating outputs...
      ✅ Migration: database/migrations/2026_04_15_160000_optimize_bigint_columns.php
      ✅ Report: reports/analysis_2026-04-15_160000.json
      ✅ Log: logs/run_2026-04-15_160000.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Analysis complete! Next steps:

1. Review the generated migration file
2. Test in staging environment:
   php artisan migrate --pretend
   
3. Apply migration:
   php artisan migrate
   
4. Verify database integrity
5. Rollback if needed:
   php artisan migrate:rollback
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Using Generated Migrations in Laravel

#### Step 1: Copy Migration File

```bash
# Copy to your Laravel project
cp database/migrations/*_optimize_bigint_columns.php \
   /path/to/your-laravel-app/database/migrations/
```

#### Step 2: Review the Migration

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * AI Consensus: 100% (3/3 models agreed)
     * Generated: 2026-04-15 16:00:00
     * Safety verified: All changes have 3+ year buffer
     */
    public function up(): void
    {
        // Optimize users.id: BIGINT → INTEGER
        // Current max: 45,823 | Integer limit: 2,147,483,647
        // Safety margin: 127 years at current growth rate
        Schema::table('users', function (Blueprint $table) {
            $table->integer('id')->change();
        });

        // Optimize orders.id: BIGINT → INTEGER
        // Current max: 1,234,567 | Integer limit: 2,147,483,647
        // Safety margin: 8 years at current growth rate
        Schema::table('orders', function (Blueprint $table) {
            $table->integer('id')->change();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->bigInteger('id')->change();
        });
        
        Schema::table('orders', function (Blueprint $table) {
            $table->bigInteger('id')->change();
        });
    }
};
```

#### Step 3: Test Migration (Dry Run)

```bash
cd /path/to/your-laravel-app

# See what SQL will be executed WITHOUT making changes
php artisan migrate --pretend
```

#### Step 4: Backup Database

```bash
# PostgreSQL backup
pg_dump -U your_username your_database > backup_$(date +%Y%m%d_%H%M%S).sql

# Or use Laravel backup package
php artisan backup:run
```

#### Step 5: Apply Migration

```bash
# Run in staging first!
php artisan migrate

# If something goes wrong, rollback:
php artisan migrate:rollback
```

---

## 📊 Output Examples

### Generated Migration File

**Location**: `database/migrations/2026_04_15_160000_optimize_bigint_columns.php`

See the example in the [Usage](#using-generated-migrations-in-laravel) section above.

### JSON Analysis Report

**Location**: `reports/analysis_2026-04-15_160000.json`

```json
{
  "metadata": {
    "timestamp": "2026-04-15T16:00:00Z",
    "database": "production_db",
    "total_tables": 12,
    "total_bigint_columns": 8,
    "models_queried": 3,
    "consensus_threshold": 60
  },
  "analysis_results": [
    {
      "table": "users",
      "column": "id",
      "current_type": "bigint",
      "current_max_value": 45823,
      "current_row_count": 45823,
      "growth_rate_per_day": 127,
      "ai_votes": {
        "integer": 3,
        "smallint": 0,
        "bigint": 0
      },
      "consensus": {
        "recommended_type": "integer",
        "agreement_percentage": 100,
        "risk_level": "low"
      },
      "safety_analysis": {
        "integer_limit": 2147483647,
        "years_until_overflow": 127,
        "safety_buffer": "excellent"
      },
      "action": "optimize",
      "reasoning": "Current usage is 0.002% of BIGINT capacity. Growth rate is steady and predictable. All models agree INTEGER provides adequate headroom for 127 years."
    },
    {
      "table": "transactions",
      "column": "external_id",
      "current_type": "bigint",
      "current_max_value": 9876543210,
      "ai_votes": {
        "integer": 0,
        "smallint": 0,
        "bigint": 3
      },
      "consensus": {
        "recommended_type": "bigint",
        "agreement_percentage": 100,
        "risk_level": "high"
      },
      "action": "skip",
      "reasoning": "External API identifier. Values are not controlled by this application. Growth pattern is unpredictable. Safety-first approach: maintain BIGINT."
    }
  ],
  "summary": {
    "optimizations_applied": 5,
    "columns_skipped": 3,
    "estimated_storage_savings": "2.3 MB per million rows",
    "migration_generated": true,
    "migration_file": "database/migrations/2026_04_15_160000_optimize_bigint_columns.php"
  }
}
```

---

## 🧠 AI Consensus Mechanism

### How Voting Works

Each AI model independently analyzes your schema and votes for the safest column type:

```
Table: orders.id
Current: BIGINT (8 bytes)
Max value: 1,234,567
Growth: +1,500/day

┌─────────────────────┬──────────┬─────────────────────────────┐
│ Model               │ Vote     │ Reasoning                   │
├─────────────────────┼──────────┼─────────────────────────────┤
│ Qwen 3.6 Plus       │ INTEGER  │ 8yr safety buffer sufficient│
│ Claude Opus 4.6     │ INTEGER  │ Growth predictable, safe    │
│ Gemma 4 26B         │ BIGINT   │ Prefer conservative approach│
└─────────────────────┴──────────┴─────────────────────────────┘

Consensus: INTEGER (2/3 votes = 67%)
Threshold: 60% required
✅ PASS - Migration will be generated
```

### Decision Rules

| Metric | Threshold | Action |
|--------|-----------|--------|
| **Agreement** | ≥ 60% | ✅ Generate migration |
| **Agreement** | < 60% | ⏸️ Keep current type (too risky) |
| **Risk Level** | `High` | ⏸️ Skip (e.g., external IDs) |
| **Growth Buffer** | < 3 years | ⏸️ Skip (not future-proof) |
| **Unpredictable Growth** | Detected | ⏸️ Skip (safety first) |

### Consensus Formula

```
consensus_percentage = (votes_for_winning_type / total_successful_models) × 100

Example:
3 models queried, all responded successfully
2 voted for INTEGER, 1 voted for BIGINT
consensus = (2/3) × 100 = 67%
```

### Tie-Breaker Logic

If there's a 3-way tie (rare), the tool defaults to the **largest type** for safety:

```
Votes: 1 × SMALLINT, 1 × INTEGER, 1 × BIGINT
Winner: BIGINT (safety first)
```

### Risk Classification

- **Low Risk**: Auto-incrementing IDs, controlled counters, date-based sequences
- **Medium Risk**: User-controlled IDs, foreign keys to stable tables
- **High Risk**: External API IDs, payment references, unpredictable sources

---

## 🛡️ Migration Safety

### Safety Guarantees

1. **Buffer Validation**: Every optimization must have ≥3 years of headroom
2. **No Data Truncation**: Current max value must fit in new type with margin
3. **Rollback Support**: Every migration includes a working `down()` method
4. **No Schema Changes**: Only column types are modified, no data loss

### Pre-Migration Checklist

Before applying any generated migration:

- [ ] ✅ **Backup your database** (pg_dump or Laravel backup)
- [ ] ✅ **Review the migration file** manually
- [ ] ✅ **Test with `--pretend` flag** to see SQL without executing
- [ ] ✅ **Run in staging environment** first
- [ ] ✅ **Verify application functionality** after migration
- [ ] ✅ **Monitor database performance** for 24-48 hours
- [ ] ✅ **Keep rollback plan ready** (`php artisan migrate:rollback`)

### What the Tool WON'T Do

- ❌ Modify columns that are close to their limits
- ❌ Change columns with unpredictable growth patterns
- ❌ Optimize external ID columns (e.g., Stripe IDs, UUIDs)
- ❌ Proceed when AI models disagree (< 60% consensus)
- ❌ Generate migrations for high-risk scenarios

### When to Skip the Migration

Don't use the generated migration if:

1. Your database is under active heavy write load
2. The table contains billions of rows (test on replica first)
3. You're unsure about the growth predictions
4. Downtime is unacceptable (use blue-green migration strategy)

---

## 🔐 Security Best Practices

### Protecting API Keys

```bash
# ✅ DO: Use environment variables
OPENROUTER_API_KEY=sk-or-v1-abc123...

# ❌ DON'T: Hardcode in scripts
api_key = "sk-or-v1-abc123..."  # NEVER DO THIS
```

### .gitignore Configuration

Ensure these files are never committed:

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Reports (may contain sensitive schema details)
reports/
logs/

# Python
venv/
__pycache__/
*.pyc
```

### Database Security

- **Read-Only Access**: Tool only needs `SELECT` permissions
- **Dedicated User**: Create a specific user for analysis
  ```sql
  CREATE USER ai_analyzer WITH PASSWORD 'secure_password';
  GRANT CONNECT ON DATABASE your_db TO ai_analyzer;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO ai_analyzer;
  ```

### API Key Rotation

```bash
# Rotate keys monthly on OpenRouter dashboard
# Update .env immediately
# Revoke old keys
```

### OneDrive/iCloud Warning

⚠️ **Critical**: Do NOT store this project in cloud-synced folders:

- OneDrive sync can corrupt `.git` state
- Credentials in `.env` may leak to cloud
- File locks cause migration failures

**Solution**: Move project to local directory:
```bash
# Windows
C:\projects\pg-ai-analyzer\

# macOS/Linux
~/projects/pg-ai-analyzer/
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. `ModuleNotFoundError: No module named 'dotenv'`

**Cause**: Dependencies not installed

**Fix**:
```bash
pip install -r requirements.txt
```

---

#### 2. `psycopg2.OperationalError: could not connect to server`

**Cause**: PostgreSQL is not running or connection details are wrong

**Fix**:
```bash
# Check if PostgreSQL is running
# Linux:
sudo systemctl status postgresql

# macOS:
brew services list

# Windows: Open pgAdmin or check Services

# Verify .env credentials match your database
DB_HOST=127.0.0.1  # Use localhost or IP
DB_PORT=5432       # Default PostgreSQL port
```

---

#### 3. `401 Unauthorized` from OpenRouter

**Cause**: Invalid or expired API key

**Fix**:
1. Go to [OpenRouter Dashboard](https://openrouter.ai/keys)
2. Regenerate API key
3. Update `.env`:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-NEW_KEY_HERE
   ```

---

#### 4. `JSONDecodeError: Expecting value`

**Cause**: AI returned markdown instead of pure JSON

**Fix**:
1. Check `reports/` folder for raw response
2. Retry with `DEBUG_MODE=true` in `.env`
3. If persistent, the AI may be overloaded—try again in 5 minutes

---

#### 5. Git Errors: `fatal: Unable to write new index file`

**Cause**: OneDrive is locking files

**Fix**:
```bash
# Move project outside OneDrive/iCloud
mv pg-ai-analyzer C:\projects\pg-ai-analyzer

# Or pause cloud sync temporarily
```

---

#### 6. Migration Fails: `Column 'id' does not exist`

**Cause**: Schema changed since analysis

**Fix**:
1. Re-run analyzer to regenerate migration
2. Don't use migrations older than 1 week

---

#### 7. `Rate limit exceeded` (OpenRouter)

**Cause**: Too many requests in short time

**Fix**:
- Tool includes 2-second delays between queries
- If error persists, wait 1 minute and retry
- Consider upgrading OpenRouter plan

---

### Debug Mode

Enable detailed logging:

```bash
# In .env
DEBUG_MODE=true

# Re-run analyzer
python multi_ai_analyzer.py

# Check logs
cat logs/run_*.log
```

### Getting Help

If you encounter an issue not listed here:

1. Check `logs/` directory for error details
2. Review `reports/` JSON for data anomalies
3. Open a GitHub Issue with:
   - Error message
   - Python version (`python --version`)
   - PostgreSQL version (`psql --version`)
   - Relevant log snippets (redact credentials!)

---

## 💰 Cost Estimation

### OpenRouter Pricing (April 2026)

| Model | Input Tokens | Output Tokens | Cost per Run |
|-------|--------------|---------------|--------------|
| **Qwen 3.6 Plus** | ~2,000 | ~500 | ~$0.03 |
| **Claude Opus 4.6 Fast** | ~2,000 | ~500 | ~$0.10 |
| **Gemma 4 26B (Free)** | ~2,000 | ~500 | **$0.00** 🎉 |
| **Total per Analysis** | ~6,000 | ~1,500 | **~$0.13** |

### Cost Scaling

```
Small schema (5 tables):    ~$0.10
Medium schema (20 tables):  ~$0.15
Large schema (100 tables):  ~$0.30
Enterprise (500 tables):    ~$0.80
```

### Cost Optimization Tips

1. **Cache results**: JSON reports can be reused for 1-2 weeks
2. **Filter tables**: Modify script to skip irrelevant tables
3. **Use free tier**: Gemma 4 26B provides good results at $0
4. **Batch analysis**: Analyze multiple databases in one session

### Monthly Budget Examples

| Usage Pattern | Runs/Month | Monthly Cost |
|---------------|------------|--------------|
| One-time audit | 1 | ~$0.13 |
| Weekly monitoring | 4 | ~$0.52 |
| Daily CI/CD | 30 | ~$3.90 |

💡 **Tip**: For cost-sensitive projects, disable paid models and use only Gemma 4 26B (free).

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/pg-ai-analyzer.git
cd pg-ai-analyzer

# Create feature branch
git checkout -b feat/your-amazing-feature

# Make changes, add tests

# Run tests (if applicable)
python -m pytest tests/

# Commit with conventional commits
git commit -m "feat: add support for MySQL databases"

# Push and create PR
git push origin feat/your-amazing-feature
```

### Contribution Guidelines

- ✅ Follow [Conventional Commits](https://www.conventionalcommits.org/)
- ✅ Add tests for new features
- ✅ Update documentation (README, code comments)
- ✅ Ensure code passes linting (`flake8` or `black`)
- ✅ One feature per pull request

### Areas for Contribution

- 🆕 **New AI Models**: Add support for GPT-4, Llama, etc.
- 🗄️ **Database Support**: MySQL, SQLite, MongoDB adapters
- 🧪 **Testing**: Unit tests, integration tests, CI/CD pipelines
- 📊 **Visualization**: Web UI for reports, charts for growth trends
- 🌍 **Internationalization**: Multi-language support
- 📝 **Documentation**: Tutorials, video guides, blog posts

### Code of Conduct

Be kind, respectful, and constructive. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What This Means

- ✅ Free to use commercially
- ✅ Modify and distribute
- ✅ Private use allowed
- ✅ No warranty provided (use at your own risk)

---

## 👨‍💻 Author

**Hamza Siddique**

- 📧 Email: [your.email@example.com](mailto:your.email@example.com)
- 🔗 GitHub: [@yourusername](https://github.com/yourusername)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- 🐦 Twitter: [@yourhandle](https://twitter.com/yourhandle)

---

## 🙏 Acknowledgments

- **OpenRouter** for providing unified AI model access
- **Anthropic**, **Alibaba Cloud**, and **Google** for their amazing AI models
- The **Laravel** community for migration best practices
- All contributors who help improve this tool

---

## 📚 Additional Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [PostgreSQL Column Types](https://www.postgresql.org/docs/current/datatype-numeric.html)
- [Laravel Migrations Guide](https://laravel.com/docs/migrations)
- [Database Optimization Best Practices](https://www.postgresql.org/docs/current/performance-tips.html)

---

## 🗺️ Roadmap

- [ ] v1.1: MySQL and SQLite support
- [ ] v1.2: Web UI for visualization
- [ ] v1.3: Automated scheduling (cron jobs)
- [ ] v2.0: Real-time monitoring dashboard
- [ ] v2.1: Slack/Discord notifications
- [ ] v3.0: Machine learning for better predictions

---

<div align="center">

**⭐ If this tool saved you time or storage, please star the repo! ⭐**

Made with ❤️ and 🤖 by developers, for developers

</div>