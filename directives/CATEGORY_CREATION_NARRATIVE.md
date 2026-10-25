# Category Creation Narrative Directive

> **Status:** MANDATORY DEFAULT for every new business plan, pitch deck and investor narrative
> **Added:** 2026-10-24 (first applied to the Metorite plan)
> **Validator:** `execution/check_category_narrative.py`

## Purpose

Every business plan this agent writes is a **category creation** argument, not a feature comparison. The plan has to convince a reader that a new way of thinking about a problem exists, that the company defines it, and that the economics of that category will flow to whoever names it first.

Three lenses do the work together:

| Lens | Source | Job in the plan | Failure it prevents |
| ---- | ------ | --------------- | ------------------- |
| **Category Design** | *Play Bigger* — Ramadan, Peterson, Lochhead, Maney (2016) | Strategy: name the problem, name the category, own the point of view | "Better/faster/cheaper" positioning inside someone else's category |
| **David Ogilvy** | *Confessions of an Advertising Man* (1963), *Ogilvy on Advertising* (1983) | Proof and promise: one big idea, specific facts, headlines that sell | Vague, adjective-heavy copy that nobody believes |
| **Rory Sutherland** | *Alchemy: The Surprising Power of Ideas That Don't Make Sense* (2019); Vice Chairman, Ogilvy UK | Psycho-logic: perceived value, anxiety reduction, signalling, reframing | Purely rational spreadsheets that miss why people actually buy |

Ogilvy is the discipline and Sutherland is the imagination. Sutherland works at the agency Ogilvy founded, so the two lenses are meant to be used together: be persuasive, and support every claim with evidence.

### Non-negotiable guardrail

**Persuasion never overrides evidence.** All rules in `AGENTS.md` (Unicode, references, tier-1 sourcing, confidence labels, TAM hierarchy discipline) still apply in full. Ogilvy himself was research-obsessed: *"The more informative your advertising, the more persuasive it will be."* A beautiful reframe with no data behind it is a red flag, not a category.

---

## Part 1 — Category Design (the strategy)

### Core concepts

| Concept | Definition | How to apply in a plan |
| ------- | ---------- | ---------------------- |
| **Category king** | The company that defines and dominates a category. *Play Bigger* reports category kings capture roughly three-quarters of their category's total market value. | Frame the plan around *becoming* the category king, not winning share. Cite the book, do not invent other "winner takes most" statistics. |
| **The problem before the product** | Customers must recognise the problem before they value the solution. Market the problem first. | Section 01 names and dramatises the problem. The product does not appear until the reader feels the problem. |
| **Missing-ness** | The gap between how things are and how they could be; the reader should feel something is missing in their world. | Every Executive Summary opens with what is missing, not with what the company does. |
| **Point of View (POV)** | A written statement of the problem, why it exists, why now, the new category and what the world looks like with it solved. | Write the POV first (Section 00). All later sections must be consistent with it. |
| **From → To** | The old way versus the new way, expressed as a shift in behaviour, not features. | Mandatory table in Section 00. Reused in pitch deck "Why now". |
| **The enemy** | The status quo, not a competitor. Usually a behaviour, a workaround or a belief. | Name it in 2–5 words (e.g. "the founder's head as the integration layer"). |
| **Category name** | 2–4 plain words a customer could repeat to a colleague. | Test: would a buyer type it into a search box? Would an analyst use it as a report title? |
| **Lightning strike** | A concentrated launch moment where the POV, product and GTM land together. | Section 06 (GTM) plans one lightning strike per stage, tied to a milestone. |
| **Flywheel** | Category design, product design and company design reinforce each other. | Section 03 (product) and 08 (team) must show how they serve the category, not just the feature roadmap. |

### Sizing a market that does not exist yet

A new category has no analyst report with its name on it. Do **not** solve this by inventing a number. Size it in three sourced layers and label confidence on each:

1. **Cost of the problem** — what the status quo costs customers today (time, leakage, missed revenue, management hours). Must cite data. Typically MEDIUM confidence.
2. **Budget migration** — which existing, researched budgets the new category will absorb or displace (e.g. a share of collaboration software, CRM add-ons, executive assistant headcount). Each source budget cited to tier-1 research. HIGH for the source budget, MEDIUM/LOW for the migration share.
3. **Bottom-up account math** — accounts × ACV with the account count sourced (government registries, industry bodies) and the ACV justified by Sections 07 and Part 3 pricing logic.

Then present all three together in Section 02. Where they disagree, show the disagreement. A plan that only shows layer 3 is a plan for an existing market.

---

## Part 2 — David Ogilvy (the discipline)

### Principles

| Principle | Ogilvy's words (verified) or paraphrase | Plan rule |
| --------- | --------------------------------------- | --------- |
| **The big idea** | *"Unless your advertising contains a big idea, it will pass like a ship in the night."* | Section 00 states one Big Idea in a single sentence. Every section headline must be traceable to it. |
| **Headlines carry the weight** | *"On the average, five times as many people read the headline as read the body copy."* | Every H2 is a claim, not a label. "Revenue Model" → "Organisation pricing makes each new customer cheaper to serve". |
| **Specific beats general** | The Rolls-Royce headline: *"At 60 miles an hour the loudest noise in this new Rolls-Royce comes from the electric clock."* | Replace adjectives with numbers and observed facts. "Fast setup" → "Live in 40 engineer-hours". |
| **Respect the reader** | *"The consumer isn't a moron; she is your wife."* | No hype, no unexplained jargon. Write for an intelligent investor who has read a hundred plans. |
| **It must sell** | *"If it doesn't sell, it isn't creative."* | Every section ends with **Investment Implications** that state what the reader should now believe. |
| **Positioning** | Decide what the product does and who it is for before writing a word. | Section 00 states the primary buyer in one line, and what the product is *not* for. |
| **Research first** | Ogilvy built campaigns from customer research and product facts. | Customer language (interviews, support tickets, usage logs) is quoted verbatim where available and labelled as internal data. |

### Language rules (enforced by the validator)

- **Plain words.** Prefer short Anglo-Saxon words to Latinate ones: "use" not "utilise", "help" not "facilitate".
- **Numbers in headlines** where a real, cited number exists.
- **One idea per paragraph.** Lead with the claim, follow with the proof.
- **No unsupported superlatives.** "Best", "only", "first", "leading", "#1" require a citation in the same sentence or must be removed.
- **Banned clichés** (unless quoted from a source): revolutionary, game-changing, game changer, cutting-edge, best-in-class, world-class, seamless, seamlessly, synergy, synergies, leverage (as a verb), next-gen, next-generation, paradigm shift, disruptive, holistic, robust solution, state-of-the-art, unlock value, empower, one-stop shop, AI-powered (in a headline).

---

## Part 3 — Rory Sutherland (the psycho-logic)

### Principles

| Principle | Idea | Plan rule |
| --------- | ---- | --------- |
| **Psycho-logic** | People buy for psychological reasons that look illogical on a spreadsheet but are perfectly rational to the buyer. | Section 05 (validation) and 07 (revenue) state the *psychological job* the product does (e.g. reassurance, status, control) alongside the functional job. |
| **Perception is the product** | Changing how something feels can be worth as much as changing what it does, and is often far cheaper. His Eurostar example: billions spent to shorten the journey, when improving how the journey felt might have created more value. | For every major cost line in the roadmap, ask: is there a perception fix that delivers the same felt value for less? Record the answer in Section 03. |
| **Anxiety reduction** | Uber's map did not make taxis arrive faster; it removed the uncertainty of waiting. Removing uncertainty is a product. | Where the product reduces uncertainty, make that the headline benefit, not "productivity" or "time saved". |
| **Costly signalling** | Things that are expensive or effortful to do signal commitment and quality. Price, setup effort and on-site presence are signals. | Section 07 explains what the price *signals*. Underpricing an executive product can destroy trust. |
| **Satisficing and fear of blame** | B2B buyers often choose the option they cannot be blamed for over the "optimal" one ("nobody got fired for buying IBM"). | Section 06 shows how the plan removes buyer risk: pilots, references, India hosting, approvals before action, exit clauses. |
| **The doorman fallacy** | Defining a role by its most visible task (opening doors) and automating it destroys the unseen value (security, status, recognition). | When the product replaces human work, Section 03 lists the unseen value of that work and how the product keeps it. |
| **Don't design for the average** | Averages hide the behaviour of the extremes, where insight lives. | Use the busiest user and the lightest user as personas alongside the average. Usage scenarios in Section 07 must include both ends. |
| **Test counterintuitive things** | His rule: *"Test counterintuitive things, because no one else will."* Also: *"The opposite of a good idea can be another good idea."* | Section 11 (risks) includes at least one "opposite strategy" considered and why it was rejected or kept as a test. |

---

## Part 4 — How the standard plan changes

### New section: `00_Category_Design.md` (written FIRST, before Market Drivers)

Required headings (the validator checks for them):

```markdown
# Category Design: [Category Name]

> **Last Updated:** YYYY-MM-DD
> **Project:** [Project]
> **Status:** Draft/Review/Final

## Executive Summary
## The Big Idea            <!-- one sentence, Ogilvy -->
## The Problem We Name     <!-- missing-ness, before any product mention -->
## The Enemy               <!-- the status quo, 2–5 words + explanation -->
## From → To               <!-- table: Old way | New way, 4–8 rows -->
## Category Name           <!-- 2–4 words + rejected alternatives -->
## Point of View           <!-- 300–600 words, the POV document -->
## The Psychological Job   <!-- Sutherland: what the buyer feels, not just does -->
## Who It Is For (and Not For)
## Proof Points            <!-- the facts that make the POV believable, cited -->
## Key Insights
## Investment Implications
## References & Sources
```

### Lens map for the existing sections

Section filenames **do not change** (`extract_config_from_plan.py` depends on 02, 07, 08, 09, 10). Only the lens and the headlines change.

| # | Section | Category-creation lens | Ogilvy test | Sutherland test |
| - | ------- | ---------------------- | ----------- | --------------- |
| 00 | Category Design | POV, enemy, from→to, name | One big idea | Psychological job |
| 01 | Market Drivers | Why the old category is breaking *now* | Specific dated facts | What anxiety is rising? |
| 02 | TAM/SAM/SOM | Three-layer sizing (problem cost, budget migration, bottom-up) | Show the math | Is value felt or only computed? |
| 03 | Technology Architecture | Product as proof of the POV | Name the demonstrable facts | Perception fixes vs engineering fixes; doorman fallacy |
| 04 | Competitive Analysis | Old categories vs the new one, not a feature matrix | No unsupported "only/first" | Why buyers stay with the status quo |
| 05 | Customer Validation | Evidence that customers already feel the problem | Verbatim customer language | Behaviour, not stated intent |
| 06 | Go-To-Market | Evangelise the problem; lightning strikes | Headline per channel | Remove buyer blame/risk |
| 07 | Revenue Model | Pricing as category signal | Numbers, not adjectives | What does the price signal? Extremes, not averages |
| 08 | Team & Costs | Company design serving the category | Specific roles and costs | — |
| 09 | Fundraising | Capital to win the category, not just runway | Milestones as facts | Investor's fear of missing the category king |
| 10 | Financial Projections | Category-king trajectory vs follower case | Every figure reconciles | — |
| 11 | Risk Analysis | Risk that the category never forms, or forms around someone else | Plain statement of risk | One "opposite strategy" tested |

### Stage 0 additions (Scope Lock)

In addition to business model, geographies, timeline and currency, the agent must ask:

1. **What is missing?** — In the customer's words, what do they not have today?
2. **The enemy** — What status-quo behaviour or workaround are we replacing?
3. **Category name candidates** — Offer 3–5 options and ask the user to pick or reject. **Run a label-ownership search first** (who already uses each name, where, for which buyer) and show it with the options — a crowded label needs a qualifier (niche down: buyer, geography or job).
4. **From → To** — Confirm the 4–8 shifts.
5. **Psychological job** — What does the buyer *feel* when it works (relief, control, status, safety)?
6. **Trade-off question:** Create a new category (higher education cost, higher prize) or reposition inside an existing one (faster, smaller prize)?

Record the answers in `.tmp/<project>/notes/category_design_brief.md` and in the assumption register.

### Pitch deck narrative arc

Replace the generic Problem → Solution order with:

1. **The missing-ness** (the human truth)
2. **The enemy** (the status quo and why it is breaking now)
3. **From → To** (the new world)
4. **The category** (name + POV in one line)
5. **The product as proof** (one day in the life)
6. **Why now** (cited drivers)
7. **Evidence** (customers, usage, behaviour)
8. **The economic engine** (pricing as signal, unit economics)
9. **The category-king outcome** (what winning looks like, with valuation logic)
10. **The ask**

---

## Part 5 — Quality checklist

Run after each section, and before any Stage gate sign-off:

```bash
python execution/check_category_narrative.py --sections-dir .tmp/<project>/business_plan/sections
```

Manual checks:

- [ ] Section 00 exists and contains every required heading
- [ ] The Big Idea is one sentence and appears (verbatim or echoed) in the Executive Summary of 00 and 01
- [ ] The problem is described before the product in 00, 01 and the deck
- [ ] Category name is 2–4 words and used consistently in every section
- [ ] The enemy is the status quo, not a named competitor
- [ ] Every H2 headline is a claim, not a label (Ogilvy)
- [ ] No banned clichés; every superlative has a citation
- [ ] At least one psychological-value claim (Sutherland) per section 03, 05, 06, 07
- [ ] Market sizing shows all three layers with confidence labels
- [ ] All `AGENTS.md` reference and Unicode standards still pass

## Common pitfalls

| Mistake | Why it's wrong | Correct approach |
| ------- | -------------- | ---------------- |
| Leading with the product | Readers don't value an answer before they recognise the problem | Missing-ness first, product second |
| Naming a competitor as the enemy | Places you inside their category | The enemy is the status quo behaviour |
| Clever category name | Customers can't repeat it | 2–4 plain words a buyer would search for |
| "Saves X hours" as the headline | Rational benefit, weak felt value | Lead with the felt outcome (certainty, control), prove with hours |
| Inventing a category TAM | Breaks the evidence standard | Three-layer sizing with sources and confidence |
| Pricing to cost | Price is a signal; cheap reads as unimportant | Price to the value and the signal, show cost separately |
| Quoting Sutherland/Ogilvy decoratively | Quotes are not proof | Use the principles to shape structure; quotes sparingly, only verified ones |
| Inventing quotes | Breaks credibility | Only use quotes listed in this directive or verified from the source; otherwise paraphrase and say so |

## Learnings log

| Date | Project | Learning |
| ---- | ------- | -------- |
| 2026-10-24 | aroh | Directive created. Source strategy doc (Aroh narrative) already used "anxiety reduction" as the core benefit — a natural Sutherland fit. |
| 2026-10-24 | aroh | Validator accepts Key Insights / Investment Implications at H2 or H3 (AGENTS.md template uses H3). "the first" as an ordinal ("the first cohort") is not a superlative; only "the first to" / "first-ever" are flagged. |
| 2026-10-24 | aroh | Verify proof points from the source strategy doc before reuse: Gartner and PwC block direct fetch (403) — confirm via search. PwC India "66% vs 42%" compares a concern rate (India, ~50 CEOs) with a top-concern rate (global) — state the caveat. Play Bigger's 76% is the authors' own research — label it so. |
| 2026-10-24 | aroh | Category label was locked at Stage 0 before checking who else used it; Stage 1 research then found 11+ "AI Chief of Staff" products. Now: label-ownership search happens before the name is offered (Stage 0, question 3). |
| 2026-10-24 | aroh | `consolidate_market_research.py` only read SERP `organic_results`; it now normalises agent-verified findings files. Name research files with the categorizer's keywords (`market_research_<project>_*.json`, `competitors_research_<project>.json`) or they land in "general". |
| 2026-10-24 | aroh | Group references by category, but number them sequentially in list order (renumber inline citations to match) so anchors run 1, 2, 3… with no jumps. |
