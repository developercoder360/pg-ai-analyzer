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
