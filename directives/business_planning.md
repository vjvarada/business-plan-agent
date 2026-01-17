# Business Planning Agent Directive

> Standard Operating Procedure for creating comprehensive business plans through interactive collaboration, market research, financial projections, and strategic analysis.

## Goal
Work **collaboratively** with the user to create a professional business plan by:
1. Gathering the business idea and key assumptions through conversation
2. Conducting market research using real online data
3. Generating SWOT analysis, business model canvas, and financial projections
4. Delivering a polished Google Docs business plan + Google Sheets 5-year financial model

## Interactive Workflow Philosophy

**This agent is conversational, not transactional.** Don't ask for all inputs upfront. Instead:
1. Start with the business idea
2. Ask clarifying questions one topic at a time
3. Research as you go and share findings
4. Validate assumptions with the user before finalizing
5. Build the plan iteratively with user feedback

## Inputs (Gathered Progressively)

### Phase 1: Core Concept (Ask First)
| Input | Required | Description |
|-------|----------|-------------|
| Business Idea | Yes | What does the business do? (1-2 sentences) |
| Industry | Yes | Industry sector (e.g., "SaaS", "E-commerce", "Healthcare") |

### Phase 2: Market Understanding (Research + Ask)
| Input | Required | Description |
|-------|----------|-------------|
| Target Market | Yes | Who are the customers? (demographics, B2B/B2C, geography) |
| Problem Solved | Yes | What pain point does this address? |
| Competition | No | Known competitors (agent can research if unknown) |

### Phase 3: Business Model (Ask After Research)
| Input | Required | Description |
|-------|----------|-------------|
| Revenue Model | Yes | How will the business make money? |
| Pricing Strategy | No | Price points, tiers, or ranges |
| Key Costs | No | Major expense categories |

### Phase 4: Financial Assumptions (Collaborate)
| Input | Required | Description |
|-------|----------|-------------|
| Initial Investment | Yes | Starting capital amount |
| Revenue Assumptions | Yes | Customer count, price, growth rate projections |
| Cost Assumptions | Yes | Fixed costs, variable costs as % of revenue |
| Break-even Target | No | When does user expect profitability? |

### Phase 5: Output Preferences
| Input | Required | Description |
|-------|----------|-------------|
| Company Name | Yes | Name for the business plan |
| Google Drive Folder ID | No | Folder to store output documents |

## Tools/Scripts

### Market Research
- `serp_market_research.py` - Search Google, analyze competitors, track trends, get news
  - Modes: `search`, `competitors`, `trends`, `news`
  - Requires: `SERPAPI_API_KEY`

### Business Analysis (Copilot Mode)
- `generate_business_plan.py` - Generate SWOT, financials, canvas, compile plans
  - Modes: `swot`, `financials`, `canvas`, `compile`
  - **In Copilot mode**: Use `--copilot` flag to get prompts, then generate content directly
  - Standalone mode: Requires `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

### Financial Spreadsheet
- `create_financial_spreadsheet.py` - Create detailed 5-year financial projections in Google Sheets
  - Creates: Revenue, Expenses, P&L, Cash Flow, Metrics sheets
  - Requires: `credentials.json` and OAuth flow

### Google Docs
- `create_google_doc.py` - Create new documents
- `update_google_doc.py` - Update existing documents (append, prepend, replace)
  - Requires: `credentials.json` and OAuth flow

### Google Sheets
- `read_sheet.py` - Read data from sheets
- `update_sheet.py` - Create or update sheets
- `append_to_sheet.py` - Append rows to sheets
  - Requires: `credentials.json` and OAuth flow

## Conversational Workflow

### Step 1: Understand the Business Idea
**Agent asks:**
- "Tell me about your business idea. What problem are you solving and for whom?"
- "What industry would you categorize this in?"

**Agent actions:**
- Listen and summarize understanding back to user
- Identify key terms for market research

### Step 2: Research the Market
**Agent actions:**
```bash
# Search for market data
python execution/serp_market_research.py --mode search --query "[industry] market size trends 2026" --output .tmp/market_research.json

# Find competitors
python execution/serp_market_research.py --mode competitors --query "[business type]" --industry "[industry]" --output .tmp/competitors.json

# Get industry trends
python execution/serp_market_research.py --mode trends --query "[industry]" --output .tmp/trends.json
```

**Agent shares findings:**
- "Based on my research, here's what I found about the market..."
- "These are the main competitors I identified: ..."
- "Key trends to be aware of: ..."

### Step 3: Define Target Market
**Agent asks:**
- "Based on the research, who specifically would be your ideal customer?"
- "Are you targeting B2B or B2C? What geography?"
- "What's the approximate size of this addressable market?"

### Step 4: Build Revenue Model
**Agent asks:**
- "How will you charge customers? (subscription, one-time, usage-based, etc.)"
- "What price range are you considering?"
- "What's a realistic number of customers you could acquire in Year 1?"

### Step 5: Gather Financial Assumptions
**Agent presents template and asks for input:**
- "Let's build your financial model. I'll need some assumptions:"
  - Starting investment
  - Monthly fixed costs (rent, salaries, tools)
  - Variable costs per customer/sale
  - Expected customer growth rate
  - Pricing per unit/subscription

**Agent validates:**
- "Based on your assumptions, you'd need X customers to break even. Does that sound achievable?"

### Step 6: Generate Outputs
**Agent creates:**
1. SWOT Analysis (Copilot generates directly)
2. Business Model Canvas (Copilot generates directly)
3. 5-Year Financial Projections (script + Copilot refinement)
4. Full Business Plan Document
5. Financial Spreadsheet

## Outputs
| Output | Location | Description |
|--------|----------|-------------|
| Business Plan Document | Google Docs | Full business plan with all sections |
| Financial Projections | Google Sheets | 5-year financial model with multiple sheets |
| Market Research Data | `.tmp/` | JSON files with research data |
| SWOT Analysis | `.tmp/swot.json` | Structured SWOT data |
| Business Model Canvas | `.tmp/canvas.json` | BMC components |
| Assumptions Log | `.tmp/assumptions.json` | All user-provided assumptions |

## Financial Spreadsheet Structure

The `create_financial_spreadsheet.py` script creates a Google Sheet with:

### Sheet 1: Assumptions
- All input assumptions in one place
- Easy to modify and see impact

### Sheet 2: Revenue Model
- Monthly/Annual revenue by year
- Customer growth projections
- Average revenue per customer

### Sheet 3: Expenses
- Fixed costs breakdown
- Variable costs (% of revenue)
- Total operating expenses by year

### Sheet 4: Profit & Loss
- Revenue
- Cost of Goods Sold
- Gross Profit
- Operating Expenses
- Net Income
- Margins (%)

### Sheet 5: Cash Flow
- Starting cash
- Cash inflows (revenue, investment)
- Cash outflows (expenses)
- Ending cash balance
- Runway calculation

### Sheet 6: Key Metrics
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (LTV)
- LTV:CAC Ratio
- Monthly Burn Rate
- Break-even Point
- Growth Rates

## Edge Cases and Error Handling

### SerpAPI Rate Limits
- Free tier: 100 searches/month
- If rate limited, wait and retry or use cached data
- Consider upgrading for heavy usage

### Google OAuth
- First run requires browser authentication
- Token refreshes automatically after initial auth
- If token expires, delete `token.json` and re-authenticate

### LLM API Errors (Standalone Mode Only)
- Supports both OpenAI and Anthropic
- Falls back to available provider
- **In Copilot Mode**: No LLM keys needed - Copilot handles generation

### Missing Data
- If market research fails, proceed with available data
- Financial projections can be generated with minimal inputs
- Document which data sources were unavailable
- Always validate assumptions with user before proceeding

### Unrealistic Assumptions
- If user provides assumptions that seem unrealistic, **flag them**
- Compare to industry benchmarks from research
- Suggest adjustments with reasoning

## Best Practices

1. **Be conversational** - Don't dump questions; ask progressively
2. **Research before asking** - Use market data to inform your questions
3. **Validate assumptions** - Challenge unrealistic numbers politely
4. **Show your work** - Share research findings before asking for input
5. **Save intermediate outputs** to `.tmp/` for debugging and reuse
6. **Review before finalizing** - Summarize the plan before creating docs
7. **Use specific industry terms** in queries for better results
8. **Back up Google Docs links** - save document IDs

## Example Conversation Flow

**User:** "I want to start a SaaS business that helps restaurants manage their inventory"

**Agent:** 
"Great idea! Restaurant inventory management is a real pain point. Let me do some quick research on this market..."

*[Runs market research]*

"I found some interesting data:
- The restaurant management software market is projected to reach $X by 2028
- Key players include Toast, MarketMan, and BlueCart
- Restaurants typically spend 28-35% of revenue on food costs

A few questions to help me understand your concept better:
1. Are you targeting independent restaurants, chains, or both?
2. What makes your approach different from existing solutions?"

**User:** "Independent restaurants, and we'll use AI to predict demand and reduce waste"

**Agent:**
"AI-powered demand prediction is a great differentiator! That aligns with the sustainability trend I'm seeing in the market research.

For the financial model, I need to understand your pricing:
- Similar tools charge $99-299/month for single locations
- What price point were you considering?
- How many restaurants do you think you could acquire in Year 1?"

*[Continues gathering assumptions...]*

## Required Environment Variables
```env
SERPAPI_API_KEY=your_serpapi_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json

# Optional - only needed for standalone mode (not Copilot mode)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Dependencies
```
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
google-search-results  # SerpAPI
openai
anthropic
python-dotenv
gspread
pandas
```
