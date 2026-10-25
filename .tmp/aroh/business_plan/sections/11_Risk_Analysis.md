# Risk Analysis: The Decisive Risk Is That the Category Forms Slowly — or Around Someone Else

> **Last Updated:** 2026-10-25
> **Project:** Aroh
> **Status:** Draft

## Executive Summary

Most of Aroh's risks are ordinary for an early software company: an unproven price, an unfinished product, a small team. The risk that matters most is particular to category creation: **owners may adopt Owner Intelligence more slowly than the plan needs, or a better-funded company may claim the category first.** The plan concentrates the first risk into one dated milestone — **fifty paid contracts by March 2027** — and the stress tests show why it matters: with those customers, DEWiN's ₹5 Cr bridges the pre-launch (about ₹3.7 Cr of costs fall due before the March receipts) and customer prepayments then carry the business even if the later ramp halves; without them, the previous plan needs about ₹6.0 Cr of outside money [[1]](#ref-1). The competitive map makes the second risk visible, with frontier AI labs now shipping proactive personal agents [[4]](#ref-4).

Two risks are specific to how Aroh is built. Its AI runs today on DeepSeek's API outside India, while Indian government guidance has steered officials away from DeepSeek on office devices [[6]](#ref-6); and its email and WhatsApp channels depend on Google's and Meta's platform reviews. Both have mitigations already in the plan: AI processing moves into India before the first paid contract, and both platform reviews are scheduled and budgeted in the pre-launch period.

Each risk below has an owner-level mitigation and an early-warning signal the team will track monthly.

---

## Fourteen risks, each with a mitigation and an early warning

| # | Risk | Likelihood | Impact | Mitigation | Early warning |
| - | ---- | :--------: | :----: | ---------- | ------------- |
| 1 | **The category forms slowly** — owners don't adopt the 07:30 brief as a habit | Medium | High | Free pilots on one loop; the brief must prove itself in week one; the five pilot measures in Section 05 | Daily brief opens below most working days by pilot week three |
| 2 | **The March 2027 milestone is missed** — fewer than fifty paid contracts in pre-launch, or a ramp below 150 / 300 / 500 | Medium–High | High | DEWiN funds the pre-launch so no outside money is committed before the evidence; milestone gates hold back hiring and marketing; a 30% slower ramp leaves ₹1.5 Cr at the lowest point; the full downside (about ₹6.0 Cr) needs a ~₹5 Cr seed and a gated agent-cloud budget [[1]](#ref-1) | Fewer than 25 paid contracts by the end of February 2027 |
| 3 | **Someone else claims the category** — frontier labs (Claude Duet, OpenAI dots), Microsoft, Zoho or a funded start-up | Medium | High | Claim "Owner Intelligence" first in India; build what global players won't (Tally, Indian ERPs, WhatsApp Business, India hosting); annual lightning strikes [[4]](#ref-4) | A global agent product launching organisation-level features in India |
| 4 | **AI processing outside India blocks sales** | High (until migrated) | High | Pilots disclose processing location; every paid contract runs on India-hosted DeepSeek V4-class models, Sarvam or Claude via Bedrock India [[6]](#ref-6), [[5]](#ref-5) | Procurement objections in pilots; migration slipping past the first contract |
| 5 | **India-hosted AI costs more than today's API** | Medium | Low–Medium | AI is about 6% of revenue; at 3× cost the lowest cash point on DEWiN's ₹5 Cr is ₹1.2 Cr [[1]](#ref-1); self-hosting breaks even at ~137 organisations, reached in FY2027–28 | Hosting quotes above 2× today's per-request cost |
| 6 | **Platform dependency** — Google restricted-scope review (Gmail), Meta policy (WhatsApp Business groups) | Medium | Medium | Review budgeted and scheduled pre-launch (₹12.7L security & certification); WhatsApp treated as the cockpit, not the database; Microsoft 365 and IMAP email paths | Review findings; Meta policy changes |
| 7 | **Data protection and agent security** — an agent with email and ERP access has a large blast radius | Medium | High | Approval before sensitive actions, audit log, least-privilege connectors, prompt-injection defences, written employee consent; DPDP Rules compliance ahead of May 2027 [[7]](#ref-7) | Security incident; penetration-test findings |
| 8 | **Onboarding creeps above 20 hours** — the services trap | Medium | Medium | Start every customer on email plus one system; developers productise every connector and exception pattern; FDE hours logged per onboarding | Average hours per onboarding above 30 |
| 9 | **Price resistance** — ₹18L a year is too much for smaller owners | Medium | Medium | Qualify to the ₹100 Cr+ profile; anchor to the owner's office cost (₹21.6–₹31.7L), not software prices; a 20% price cut still leaves ₹1.3 Cr at the lowest point [[1]](#ref-1) | Pilot conversion below 50% |
| 10 | **Execution and team** — product gaps (job queue, enforced security, email/WhatsApp in preview) with a small current team scaling to 53, while onboarding sixty organisations in four months | High | High | Close the gaps before the first paid contract; four FDEs from pre-launch; hire ahead of demand [[2]](#ref-2) | Production gaps open when the first paid contracts start |
| 11 | **Ownership and IP** — DEWiN owns Aroh, while building blocks come from Metorite / Hathi Labs | Medium | High (at fundraise or exit) | Document IP assignment for Aroh-specific work to DEWiN and a perpetual, transferable licence for pre-existing Hathi components before any outside round [[3]](#ref-3) | Investor due-diligence questions |
| 12 | **Macroeconomic and currency** — slower growth or a weaker rupee | Low–Medium | Medium | AI costs are dollar-linked but small; prices are in rupees; the plan's stakes rest on growth (IMF: $6T by 2030) [[8]](#ref-8) | Rupee well beyond ₹95/US$; promoter capex freezes |
| 13 | **Infrastructure and compute cost overrun** — agent swarms and production infrastructure are budgeted generously (₹4–7 Cr a year of development cloud, ₹3,000 per customer a month of production infrastructure) | Medium | Medium | Costs are explicit lines in the model, scale with customers and revenue, and are held to half budget in the downside; unit economics keep an 92% variable margin after infrastructure and AI | Cloud spend above 8% of revenue |
| 14 | **March 2027 receipts arrive late** — fifty customers are onboarded in March and billed annually upfront, but payment terms or approvals push cash into April–May | Medium | Medium–High | DEWiN's ₹5 Cr covers all pre-launch costs (₹3.7 Cr) with ₹1.3 Cr to spare, but only about one and a half months of costs; invoice on signing, offer bank-transfer terms of 15 days, and keep a standby shareholder loan of ₹2 Cr | Fewer than half of March invoices paid within 30 days |

## The opposite strategies, tested

Rory Sutherland's rule is to test the opposite of a good idea, because it may be another good idea [[9]](#ref-9). Three opposites were considered during the planning stages:

| Plan choice | The opposite | Why the plan chose as it did | Kept as a test? |
| ----------- | ------------ | ---------------------------- | --------------- |
| **One organisation-level price, ₹1.5L a month** | Self-serve ₹500 per seat plus AI credits (Metorite's original pricing) | At ₹500 a seat, about 4,760 paid seats are needed just to cover the founding team; the price would also signal "tool", not "runs your business" (Section 07) | No — but smaller friendly firms may be offered a seat-based trial outside the plan |
| **Free pilot, then full price** | Paid pilot (₹1.5–2L, credited to the contract) | Owner decision: lower friction for a new category; the ₹6L setup fee restores the commitment signal | **Yes** — if conversion falls below 50%, test paid pilots |
| **Claim a new name, "Owner Intelligence"** | Use the familiar "AI Chief of Staff" label | At least 11 products already use it; a contested label can't be owned (Section 00) | Yes — "works like a chief of staff" remains the explanation in sales conversations |

## What the plan asks investors to underwrite

Of the fourteen risks, three decide the outcome: **adoption speed and the March 2027 milestone (1, 2), category ownership (3) and India-hosted AI (4).** The first is answered by a date — fifty paid contracts by 31 March 2027 — before outside investors are asked to commit; the second by moving first and building India-specific depth; the third by a migration the plan commits to before taking any customer's money.

### Key Insights

- The decisive risk is the March 2027 milestone: with fifty paid contracts the business is self-funding; without them the previous plan needs ~₹6.0 Cr [[1]](#ref-1).
- Frontier labs' personal agents are the fastest-moving competitive threat; Aroh's defence is organisation-level, India-specific depth [[4]](#ref-4).
- AI processing outside India is a high-likelihood sales risk today, with a committed fix before the first paid contract [[6]](#ref-6), [[5]](#ref-5).
- IP and ownership between DEWiN and Hathi Labs must be documented before any outside round [[3]](#ref-3).

### Investment Implications

The risks are concentrated in the first eighteen months and are measurable early: pilot behaviour, conversion, onboarding hours and the India-hosting migration all show up within the pre-launch period and FY2027–28. An investor is underwriting a short, well-instrumented period of uncertainty, after which the business either funds itself or shows clearly that it won't — with enough cash left to change course.

---

## References & Sources

### Internal Data

<a name="ref-1"></a>

1. **Driver-level stress tests**
   - Lowest cash on DEWiN's ₹5 Cr (after the pre-launch bridge of ₹3.7 Cr): ₹1.3 Cr (base), ₹1.5 Cr (30% slower ramp), ₹1.6 Cr (halved ramp), ₹1.9 Cr (no paid pre-launch customers); downside (previous plan) needs ₹6.0 Cr, lowest cash ₹4.0 Cr with a ₹5 Cr seed
   - Source: `.tmp/aroh/config/sensitivity_calc.py` (Section 10)
   - URL: N/A (internal)

<a name="ref-2"></a>

2. **Metorite product repository — admitted gaps**
   - No durable job queue; memory off by default; security controls designed but not enforced; email and WhatsApp in preview; two organisations in production
   - Source: Hathi Labs (internal repo `Hathi-Labs/Metorite`, `COMPETITIVE_COMPARISON.md`)
   - URL: https://metorite.com/

<a name="ref-3"></a>

3. **Aroh: Strategic Narrative and Investor-Ready Business Case**
   - DEWiN should own Aroh IP and customer contracts; pre-existing Hathi libraries under a perpetual, transferable, sublicensable licence; software bill of materials and pre-existing-IP schedule from day one
   - Source: DEWiN / Hathi Labs (internal strategy document)
   - URL: N/A (internal)

### Company Announcements

<a name="ref-4"></a>

4. **Anthropic launches Claude Duet as a proactive "chief of staff" agent**
   - Morning brief, actions with approval; personal agent for Claude Pro/Max subscribers (US waitlist)
   - Source: Techiexpert, 21 Oct 2026 (official page not found)
   - URL: https://techiexpert.com/anthropic-launches-claude-duet-to-work-as-a-proactive-ai-chief-of-staff/

<a name="ref-5"></a>

5. **AWS — Amazon Bedrock expands Claude model availability to India**
   - Claude Opus 5, Sonnet 5 and Haiku 4.5 via geographic cross-Region inference across Mumbai and Hyderabad; 29 Sep 2026
   - Source: Amazon Web Services
   - URL: https://aws.amazon.com/about-aws/whats-new/2026/09/claude-region-expansion-in-sk/

### News & Media

<a name="ref-6"></a>

6. **Australian and Indian government employees warned against DeepSeek use**
   - India's Finance Ministry internal advisory (29 Jan 2025) asked officials to avoid AI tools such as ChatGPT and DeepSeek on office devices (reported by Reuters)
   - Source: Semafor, 5 Feb 2025
   - URL: https://www.semafor.com/article/02/05/2025/australian-and-indian-government-employees-warned-against-deepseek-use

### Government Policy & Legislation

<a name="ref-7"></a>

7. **PIB — DPDP Rules, 2025 Notified**
   - Rules notified 14 Nov 2025; eighteen-month phased compliance
   - Source: Press Information Bureau, Government of India (17 Nov 2025)
   - URL: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf

### Government & Macroeconomic Data

<a name="ref-8"></a>

8. **IMF World Economic Outlook — GDP, current prices (NGDPD), India**
   - Nominal GDP 2030: US$6.13T
   - Source: International Monetary Fund, DataMapper (accessed 24 Oct 2026)
   - URL: https://www.imf.org/external/datamapper/api/v1/NGDPD/IND

### Books & Frameworks

<a name="ref-9"></a>

9. **Rory Sutherland — *Alchemy: The Surprising Power of Ideas That Don't Make Sense* (2019)**
   - "The opposite of a good idea can be another good idea"; test counterintuitive things
   - Source: WH Allen / Penguin Random House
   - URL: N/A (book)
