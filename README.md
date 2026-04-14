# 🤖 PostgreSQL Multi-AI Column Optimizer

A production-ready Python tool that analyzes PostgreSQL `BIGINT` columns, predicts future data growth using multiple AI models, and generates **safe, consensus-backed Laravel migrations** to optimize storage without risking data overflow.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-336791)](https://www.postgresql.org/)
[![Laravel](https://img.shields.io/badge/Laravel-10%2B-FF2D20)](https://laravel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

- 🔍 **Deep Schema Analysis**: Extracts table structures, row counts, min/max values, and date ranges.
- 🤖 **Multi-AI Consensus Engine**: Queries `Qwen 3.6+`, `Claude Opus 4.6 Fast`, and `Gemma 4 26B` via OpenRouter.
- 📈 **Growth Prediction**: Estimates daily growth rates & calculates years until type limits are hit.
- 🛡️ **Safety-First Recommendations**: Only suggests changes with `≥60% AI consensus` & `low/medium risk`.
- 🎨 **Auto Laravel Migration**: Generates rollback-safe `up()/down()` migration files.
- 📊 **Structured JSON Reports**: Detailed analysis for auditing & CI/CD integration.
- 🔐 **Zero-Credential-Exposure**: `.env` driven, `.gitignore` secured, API key validation built-in.

---

## 🏗️ Architecture
PostgreSQL DB ──▶ Schema Extractor ──▶ AI Prompt Builder
▲ │
│ ▼
Laravel Migration ◀── Consensus Engine ◀── Multi-AI Query (OpenRouter)
▲ │
└─────────── JSON Report ──────────────┘



12345678910111213141516171819202122232425
2. Create Virtual Environment
bash
12345
3. Install Dependencies
bash
1
4. Configure Environment
bash
12
⚙️ Configuration (.env)
env
1234567891011121314
⚠️ Never commit .env. It's pre-listed in .gitignore.
🏃 Usage
Run Full Analysis
bash
1
Expected Output
12345678910111213141516171819
Use Generated Migration in Laravel
bash
1234567891011
📁 Project Structure
1234567891011
🤖 AI Consensus Logic
Metric
Threshold
Action
Agreement
≥ 60%
✅ Generate migration
Agreement
< 60%
⏸️ Keep BIGINT (too risky)
Risk Level
High
⏸️ Skip (external IDs, unpredictable growth)
Growth Buffer
< 3 years
⏸️ Skip (not future-proof)
💡 Consensus Formula: votes_for_type / total_successful_models. Tie-breaker favors larger types for safety.
🔐 Security & Best Practices
Rotate Keys Regularly: Use OpenRouter dashboard to regenerate OPENROUTER_API_KEY.
Backup Before Migration:
bash
1
Test in Staging First: Never run generated migrations directly on production.
OneDrive Warning: Sync conflicts may corrupt .git state. Keep project outside OneDrive/iCloud.
Rate Limits: Script includes 2s delays between AI queries. Respect OpenRouter limits.
🛠️ Troubleshooting
Error
Cause
Fix
ModuleNotFoundError: dotenv
Missing deps
pip install -r requirements.txt
Connection refused
PostgreSQL down
sudo systemctl status postgresql or start via pgAdmin
401 Unauthorized
Invalid API key
Rotate key at OpenRouter
JSON decode error
AI returned markdown
Check reports/ for raw response & retry
File locked / Git errors
OneDrive sync
Move project to C:\projects\ or pause sync
📈 Cost Estimation (OpenRouter)
Model
Tokens/Run
Approx Cost
qwen/qwen3.6-plus
~2500
~$0.03
anthropic/claude-opus-4.6-fast
~2500
~$0.10
google/gemma-4-26b-a4b-it:free
~2500
$0.00 🎉
Total per run
~7500
~$0.13
💡 Costs scale linearly with schema size. Cache reports/ to avoid re-querying identical DBs.
🤝 Contributing
Fork the repository
Create feature branch (git checkout -b feat/your-idea)
Commit changes (git commit -m 'Add your feature')
Push to branch (git push origin feat/your-idea)
Open a Pull Request
Please follow Conventional Commits and ensure tests pass.
📜 License
Distributed under the MIT License. See LICENSE for more information.
👨‍💻 Author
Built with ❤️ by Hamza Siddique
📧 Contact: your.email@example.com | 🔗 GitHub: @yourusername
