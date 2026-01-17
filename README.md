# Business Plan Agent 📊

> Your AI-powered business planning partner

**Type:** Business Planning Agent (Interactive)

An intelligent agent that **works with you** to create professional business plans. It conducts market research, helps validate assumptions, and generates both a business plan document (Google Docs) and 5-year financial projections (Google Sheets).

## What This Agent Does

🔍 **Researches** your market using real Google search data  
📈 **Analyzes** competitors, trends, and market size  
💡 **Helps you** think through your business model and assumptions  
📄 **Creates** a professional business plan document  
📊 **Builds** a detailed 5-year financial spreadsheet

## 🚀 Quick Start

### 1. Double-click to open
```
business-plan-agent.code-workspace
```

VS Code will automatically:
- Open the workspace
- Run setup (creates venv, installs dependencies)
- Prompt to install recommended extensions

### 2. Add your credentials

**Google OAuth** (required for Docs/Sheets):
- Download `credentials.json` from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- Place it in the workspace root

**SerpAPI** (required for market research):
- Get your key from [SerpAPI](https://serpapi.com/)
- Add to `.env`: `SERPAPI_API_KEY=your_key_here`

### 3. Select the agent
- Open Copilot Chat (`Ctrl+Shift+I`)
- Select **"business-plan-agent"** from the agent dropdown

### 4. Tell it your idea
Just describe your business idea:
> "I want to start a SaaS platform that helps restaurants manage their inventory using AI"

The agent will guide you through the rest!

## Example Conversation

**You:** I'm thinking of starting a mobile app that helps pet owners track their dog's health and find vets nearby.

**Agent:** Great idea! Pet care is a growing market. Let me do some research...

*[Runs market research]*

Here's what I found:
- The pet tech market is projected to reach $20B by 2028
- Main competitors: Petcube, Whistle, Fi
- 67% of US households own a pet

A few questions:
1. Are you targeting all pet owners or a specific segment?
2. How will you monetize - subscription, freemium, or one-time purchase?

**You:** Subscription model, targeting dog owners specifically, $9.99/month

**Agent:** Perfect. For the financial model, I need a few more assumptions:
- How many subscribers do you expect in Year 1?
- What's your estimated customer acquisition cost?
- What are your main fixed costs (developers, servers, etc.)?

*[Continues gathering assumptions...]*

**Agent:** Based on our conversation, here are your deliverables:
- 📄 [PetTrack Business Plan 2026](https://docs.google.com/document/d/xxx)
- 📊 [PetTrack 5-Year Financial Projections](https://docs.google.com/spreadsheets/d/xxx)

## What Gets Created

### Business Plan Document (Google Docs)
1. Executive Summary
2. Company Description  
3. Market Analysis (with real research data)
4. SWOT Analysis
5. Business Model Canvas
6. Marketing & Sales Strategy
7. Financial Projections Summary
8. Appendix

### Financial Spreadsheet (Google Sheets)
| Sheet | Contents |
|-------|----------|
| Assumptions | All input parameters in one place |
| Revenue | Customer growth + revenue projections |
| Expenses | Fixed costs + variable costs breakdown |
| Profit & Loss | Full P&L statement by year |
| Cash Flow | Cash position + runway |
| Key Metrics | CAC, LTV, margins, break-even |
## Execution Scripts

| Script | Purpose |
|--------|---------|
| `serp_market_research.py` | Market research via Google Search |
| `generate_business_plan.py` | Generate SWOT, canvas, financials |
| `create_financial_spreadsheet.py` | Create 5-year financial model |
| `create_google_doc.py` | Create business plan document |
| `update_google_doc.py` | Update existing documents |
| `read_sheet.py` / `update_sheet.py` | Google Sheets operations |

## Project Structure

```
business-plan-agent/
├── business-plan-agent.code-workspace  # ← Double-click to open!
├── setup.ps1 / setup.sh     # One-command setup
├── credentials.json         # Google OAuth (you add this)
├── .env                     # API keys (auto-created from .env.example)
├── AGENTS.md                # Full system prompt
├── .github/agents/          # Custom Copilot agent config
├── directives/
│   └── business_planning.md # Main SOP for business plans
└── execution/
    ├── serp_market_research.py
    ├── generate_business_plan.py
    ├── create_financial_spreadsheet.py
    ├── create_google_doc.py
    └── ...
```

## Required API Keys

| Key | Required | Purpose |
|-----|----------|---------|
| `SERPAPI_API_KEY` | Yes | Market research via Google Search |
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | Google Docs/Sheets access |
| `OPENAI_API_KEY` | No* | Only for standalone mode |
| `ANTHROPIC_API_KEY` | No* | Only for standalone mode |

*When using GitHub Copilot as orchestrator, LLM keys are not needed—Copilot handles all AI reasoning.

## Troubleshooting

**"SERPAPI_API_KEY not set"**
- Add your key to `.env`: `SERPAPI_API_KEY=your_key`

**"credentials.json not found"**
- Download OAuth credentials from Google Cloud Console
- Enable Google Docs and Sheets APIs
- Place `credentials.json` in workspace root

**"token.json expired"**
- Delete `token.json` and run any Google script again
- Browser will open for re-authentication

---

*Built with the [DOE Framework](https://github.com/vjvarada/DOE-Framework-Agentic-AI)* 🚀
