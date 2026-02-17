# Business Plan Agent 📊

> Your AI-powered business planning partner

**Type:** Business Planning Agent (Interactive)

An intelligent agent that **works with you** to create professional business plans. It conducts market research, helps validate assumptions, and generates both a business plan document (Google Docs) and 5-year financial projections (Google Sheets).

## 🎯 For Agents: Critical Decision Logic

**⚠️ BEFORE editing ANY financial model, read: [`AGENT_CHECKLIST.md`](AGENT_CHECKLIST.md)**

**Two editing approaches:**

1. **Config-Based Rebuild** - For structural changes (add/remove revenue streams, restructure TAM/SAM)
2. **Local-First Workflow** - For value updates (funding, growth rates, pricing)

**Quick rule:** Adds/removes rows? → Config Rebuild. Just values? → Local-First.

**Full decision tree:** [`directives/DECISION_TREE.md`](directives/DECISION_TREE.md)

---

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

_[Runs market research]_

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

_[Continues gathering assumptions...]_

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

**Comprehensive 15-sheet financial model:**

| Sheet                | Contents                                                                   |
| -------------------- | -------------------------------------------------------------------------- |
| Assumptions          | All input parameters + Customer Acquisition + Unit Economics               |
| Revenue              | Multi-stream revenue breakdown (Software, Hardware, Consumables, Services) |
| Operating Costs      | COGS, Fixed costs, Sales & Marketing expenses                              |
| P&L                  | Full income statement with margins and EBITDA                              |
| Cash Flow            | Operating, Investing, Financing activities                                 |
| Balance Sheet        | Assets, Liabilities, Equity with full double-entry accounting              |
| Summary              | KPI dashboard with key metrics                                             |
| Sources & References | All market research sources with URLs and inline citations                 |
| Sensitivity Analysis | Base/Upside/Downside scenario modeling                                     |
| Valuation            | DCF analysis with exit multiples and comparables                           |
| Break-even Analysis  | Contribution margin and margin of safety                                   |
| Funding & Cap Table  | Equity tracking across funding rounds                                      |
| Financial Ratios     | Investor metrics (IRR, NPV, ROE, DSCR)                                     |
| Headcount Plan       | Team growth and salary costs by department                                 |
| Geographic Expansion | Phased growth rates by region                                              |

## Workflows

### **Template-First Production Workflow** ✨ RECOMMENDED

Create production models by copying the approved 14-sheet template, then validating integrity:

```bash
# 1. Create production model from template
python execution/create_financial_model.py --company "MyCompany" --config .tmp/<project>/config/<project>_config.json --from-template

# 2. Verify template fidelity + model integrity
python execution/verify_template_copy.py --sheet-id "<SHEET_ID>"
python execution/audit_financial_model.py --sheet-id "<SHEET_ID>" --mode comprehensive
python execution/verify_sheet_integrity.py --sheet-id "<SHEET_ID>"
```

### **Local-First Draft Workflow**

Work locally without API rate limits, then sync when ready:

```bash
# 1. Create local Excel financial model
python execution/create_financial_model_local.py --company "MyCompany" --rapidtools

# 2. Create local Word business plan
python execution/create_business_plan_local.py --company "MyCompany" --industry "Tech" --description "AI platform"

# 3. Review and edit locally in Excel/Word
# (No internet required!)

# 4. Sync to Google Drive when finalized
python execution/sync_to_cloud.py --file .tmp/MyCompany_financial_model.xlsx
python execution/sync_to_cloud.py --file .tmp/MyCompany_business_plan.docx
```

**Benefits (Draft Workflow):**

- ✅ No API rate limits during development
- ✅ Faster iteration (no network calls)
- ✅ Work offline
- ✅ 100% Excel/Sheets formula compatibility (uses standard formulas: SUM, IF, VLOOKUP)
- ✅ Version control friendly (.xlsx/.docx can be committed to git)
- ✅ Formatting preserved when uploading to Google Drive

**Excel/Sheets Formula Compatibility:**

- All financial models use only **standard formulas** that work in both Excel and Google Sheets
- Compatible: `=SUM()`, `=IF()`, `=VLOOKUP()`, `=NPV()`, `=IRR()`, cross-sheet references
- Avoided: Platform-specific functions like `ARRAYFORMULA()`, `QUERY()`, `IMPORTRANGE()`, `XLOOKUP()`

### **Cloud-First Workflow** (Original)

Direct creation in Google Docs/Sheets:

```bash
# Create directly in Google Drive
python execution/create_financial_model.py --company "MyCompany" --humanoid-rent
python execution/create_google_doc.py --company "MyCompany" --content "..."
```

## Execution Scripts

| Script                            | Purpose                                        | Mode        |
| --------------------------------- | ---------------------------------------------- | ----------- |
| **Local-First Scripts**           |                                                |             |
| `create_financial_model_local.py` | Create reduced Excel financial draft (.xlsx)   | Local draft |
| `create_business_plan_local.py`   | Create Word business plan (.docx)              | Local       |
| `sync_to_cloud.py`                | Upload local files to Google Drive and convert | Hybrid      |
| **Cloud-First Scripts**           |                                                |             |
| `create_financial_model.py`       | Create/copy 14-sheet Google Sheets financial model | Cloud   |
| `update_financial_model.py`       | Update existing Google Sheets models           | Cloud       |
| `format_sheets.py`                | Standardized formatting for Google Sheets      | Cloud       |
| `audit_financial_model.py`        | Validate Google Sheets model integrity         | Cloud       |
| `repair_financial_model.py`       | Fix issues in Google Sheets models             | Cloud       |
| `create_google_doc.py`            | Create business plan in Google Docs            | Cloud       |
| `update_google_doc.py`            | Update existing Google Docs                    | Cloud       |
| `create_pitch_deck.py`            | Generate investor pitch deck (Google Slides)   | Cloud       |
| **Utilities**                     |                                                |             |
| `serp_market_research.py`         | Market research via Google Search              | API         |
| `generate_business_plan.py`       | Generate SWOT, canvas, financials              | Local/Cloud |
| `sheets_utils.py`                 | Google Sheets operations (read, write, append) | Cloud       |
| `analyze_sheet_linkages.py`       | Find formula dependencies between sheets       | Cloud       |

### Stage-Gated Execution (Recommended)

Use the orchestrator to run the process in strict dependency order and persist stage state:

```bash
python execution/run_stepwise_workflow.py --project <project> --stage status
python execution/run_stepwise_workflow.py --project <project> --stage 0 --company "<CompanyName>" --config .tmp/<project>/config/<project>_config.json --execute
python execution/run_stepwise_workflow.py --project <project> --stage 1 --research-dir .tmp/<project>/research --execute
python execution/run_stepwise_workflow.py --project <project> --stage 2 --sections-dir .tmp/<project>/business_plan/sections --execute
python execution/run_stepwise_workflow.py --project <project> --stage 3 --config .tmp/<project>/config/<project>_config.json --execute
python execution/run_stepwise_workflow.py --project <project> --stage 4 --company "<CompanyName>" --config .tmp/<project>/config/<project>_config.json --execute
python execution/run_stepwise_workflow.py --project <project> --stage 5 --sections-dir .tmp/<project>/business_plan/sections --execute

# Governance check: ensure every execution script is mapped to a stage
python execution/validate_script_registry.py
```

### Reusable Patterns & Documentation

| Document                 | Purpose                                                              |
| ------------------------ | -------------------------------------------------------------------- |
| `REUSABLE_PATTERNS.md`   | 10 code patterns extracted from RapidTools project for future agents |
| `TEMP_SCRIPT_MAPPING.md` | Maps 350+ temporary scripts to reusable patterns                     |

**Key Patterns Include:**

- Sheet linkage analysis (before restructuring)
- Business plan credibility audits (math errors, unsourced claims)
- Formula preservation during sheet restructuring
- Market research consolidation from SERP data
- Rate limit handling for Google APIs
- Standardized color palettes and formatting

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

| Key                              | Required | Purpose                           |
| -------------------------------- | -------- | --------------------------------- |
| `SERPAPI_API_KEY`                | Yes      | Market research via Google Search |
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes      | Google Docs/Sheets access         |
| `OPENAI_API_KEY`                 | No\*     | Only for standalone mode          |
| `ANTHROPIC_API_KEY`              | No\*     | Only for standalone mode          |

\*When using GitHub Copilot as orchestrator, LLM keys are not needed—Copilot handles all AI reasoning.

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

_Built with the [DOE Framework](https://github.com/vjvarada/DOE-Framework-Agentic-AI)_ 🚀
