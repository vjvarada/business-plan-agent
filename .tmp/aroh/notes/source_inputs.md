# Metorite — Source Inputs (Stage 0 intake)

> **Captured:** 2026-10-24
> **Purpose:** Raw facts extracted from user-supplied sources, before any assumption is locked.

## Sources

| # | Source | Type | Notes |
| - | ------ | ---- | ----- |
| S1 | `Aroh_ Strategic Narrative and Investor-Ready Business Case.docx.md` (Downloads) | Strategy narrative | Written for "Aroh" (DEWiN-owned, Hathi-built). Uses Metorite cost assessment as telemetry. |
| S2 | https://claude.ai/artifact/KENqXY5J6s59B8hqHEvAAq | Metorite cost plan (22 Oct 2026) | JS calculator; defaults extracted below |
| S3 | `C:\Users\VijayRaghavVarada\Documents\Github\Metorite` | Product repo | Explored by subagent |
| S4 | https://metorite.com/ | Website | "All your work, in one app." By Hathi Labs. 14-day free trial, no public pricing |

## S2 — Metorite cost plan defaults (measured / given / estimate)

| Input | Value | Label |
| ----- | ----- | ----- |
| Users per organisation | 10 | — |
| AI requests/user/day at 1.0× (busiest user) | 432 | Measured |
| Active days/month | 22 | — |
| Main model cost per request | $0.0030 | Measured |
| Cheaper model cost per request | $0.0008 | Measured |
| Cheaper-model share (default) | 50% (today ~21%) | Target |
| Usage multiplier (default) | 0.55× | Measured avg active days |
| FX | ₹88/US$ | — |
| Servers fixed | $24/mo | Estimate |
| Servers + storage per user | $0.928/mo (incl. 5 GB files) | Estimate |
| Developers | 4 × ₹2.10L/mo | Estimate |
| Claude 20x plans | 2 per dev × ₹23,999/mo | Published |
| Forward-deployed engineers (FDE) | 4 × ₹2.50L/mo | Given |
| FDE Claude 5x plan | ₹11,999/mo each | Published |
| Customer success | 1 per 50 orgs × ₹1.50L/mo | Estimate |
| CAC | ₹20,000/org | Given, minimum (known orgs) |
| Setup hours/org | 40 | — |
| Outsourced engineer rate | ₹2,000/hr | Only if outsourced |
| Engineer hours/month | 140 | — |
| Laptop (MacBook Pro 32 GB) | ₹2.30L × 4 FDEs | Estimate |
| Google Gmail security review (CASA) | ₹2.20L (range ₹45k–₹4L) | Mid of range |
| External pentest | ₹3.00L (range ₹1.2L–₹12L) | Mid of range |
| ISO 27001 | ₹5.00L (range ₹2L–₹8L) | Mid of range |
| DPDP compliance | ₹2.50L (range ₹1.5L–₹4L) | Mid of range |

### Derived at defaults (100 orgs, 0.55×, 50% cheap model)

| Metric | Value |
| ------ | ----- |
| Blended cost/request | $0.0019 (₹0.167) |
| AI cost per user/month | ₹874 |
| AI cost per org/month | ₹8,740 |
| Servers total/month | ₹83,776 |
| Fixed team + tools/month | ₹23.80L |
| Total monthly operating cost | ₹33.38L |
| **Cost per org/month** | **₹33,380** |
| One-time (CAC + laptops + security) | ₹41.9L |
| Year-1 total cost | ₹4.43Cr |

## S3 — Metorite repo facts (explored 2026-10-24)

| Fact | Value | Evidence |
| ---- | ----- | -------- |
| Positioning | "AI-driven company operating system… sold as multi-tenant SaaS"; site: "Run your company on agents" | `site/index.html` |
| Origin | Fracktal Works' internal multi-agent platform; productised since 2026-08-08 | `README.md`, `project-docs/AGENTS.md` |
| Operator | Hathi Labs; Fracktal Works is customer zero (D36) | `site/contact.html` |
| Target | Indian SMBs, INR, Razorpay, India-only data residency at launch | `work_plan.md` D19.6 |
| Live apps | 10 (Tasks, Calendar, Profile, Access, Projects, People, Chat, Approvals, Organisation, Appearance) | `specs/launch_surface.md` |
| Preview apps | Email, WhatsApp, Notes/meeting bot, CRM, Dashboard, Workflows, Workshop, Memories, Artifacts, Integrations | same |
| Agents | task-manager, crm-assistant, projects-assistant, sales, delivery, triage, reconciler, billing, strategy | `agent_registry.json` |
| **Live pricing (D49)** | **₹500/user/month flat + AI credits**; 14-day trial; signup max 10 users | `CLAUDE.md`, `site/refunds.html` |
| AI credits | ₹10 unit; provider cost × 2 (D19.2); rate card ships all-zero today | `specs/credit_pricing.md` |
| Production LLM | DeepSeek (chat / V4 pro); Whisper via Groq | `infra/litellm/config.yaml` |
| Hosting | Hostinger VPS (~$15–29/mo) + Supabase Mumbai | `deploy/hostinger/README.md` |
| Traction | No paying customers; 2 orgs in production; Fracktal onboarding incomplete | `credit_pricing.md`, `HANDOFF.md` |
| Team in repo | Vijay (owner) + Nithin (22 commits); Claude co-author on 616 commits | git log |
| Compliance | DPDP doctrine drafted; SOC 2/ISO open; Google restricted-scope review not yet addressed | `specs/saas_operations_doctrine.md` |
| "Aroh" | Zero mentions in repo | grep |

## Cross-source reconciliation flags

1. **AI cost per interaction:** S1 assumes ₹0.40/interaction → ₹20,900/org/month at base. S2 measured blended ₹0.167/request → ₹8,740/org/month. S1 is ~2.4× more conservative.
2. **Pricing vs. cost:** S1 base ACV ₹18L (₹1.5L/month) vs. S2 fully-loaded cost ₹33K/org/month at 100 orgs.
3. **CAC:** S1 ₹6–10L fully loaded per enterprise logo; S2 ₹20K (warm/known orgs only).
4. **Product scope:** S4 shows a team workspace (email, WhatsApp, projects, tasks, people, AI assistant). S1 positions an owner/CEO "AI chief of staff" (Aroh). Positioning must be reconciled.
5. **Entity:** S1 says DEWiN should own Aroh IP; S4 says Metorite is by Hathi Labs.
6. **Pricing gap:** live price ₹500/seat → ₹5,000/org/month at 10 users vs cost-to-serve ₹34,139/org/month (FX ₹95). At ₹500/seat the fixed team (₹23.8L/month) needs ~4,760 paid seats to cover salaries alone.
7. **AI vendor:** ~~S2 costs use Anthropic rates~~ — corrected 2026-10-24: S2's per-request rates come from Metorite's own usage log and price feed (production = DeepSeek V4). "Anthropic India pricing" in S2 covers only developers' Claude plans.
8. **FX:** S2 uses ₹88/US$; user locked ₹95/US$ (A-002).
