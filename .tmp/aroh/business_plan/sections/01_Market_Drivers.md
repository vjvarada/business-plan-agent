# Market Drivers: Why the Owner Can No Longer Be the Integration Layer

> **Last Updated:** 2026-10-24
> **Project:** Aroh
> **Status:** Draft

## Executive Summary

The way Indian owners run their businesses — personally joining every system, report and WhatsApp thread — was workable when businesses were smaller and slower. It is breaking now, for reasons that arrived together in the last two years.

The first is the stakes. India's next stage of growth depends on its mid-sized businesses growing, and that growth depends on owners having the attention to pursue it: the IMF expects India to pass $6T in 2030 [[1]](#ref-1), while research on Indian firms finds owners working 68-hour weeks and reluctant to delegate [[4]](#ref-4). The second is that the tools have changed: the cost of running AI at a fixed level of quality is falling about 40× a year [[8]](#ref-8), and frontier models can now run inside India [[15]](#ref-15). The third is pressure: Indian companies have adopted AI faster than they have made their data ready [[13]](#ref-13), [[9]](#ref-9), and Indian CEOs worry about keeping pace more than their global peers [[10]](#ref-10). The fourth is law: India's data protection rules, notified in November 2025, phase in through 2027 [[12]](#ref-12) and turn informal information flows into a liability.

Together these make **Owner Intelligence** both possible and necessary. Each driver below is stated as a claim, followed by the evidence and what it means for the category.

---

## India's growth ambition now depends on owners who have time to grow

The IMF projects India's nominal GDP at $4.06T in 2026, crossing $5T in 2029 and **$6T in 2030** ($6.13T) [[1]](#ref-1). Reaching that milestone on time — or sooner — depends on more Indian firms growing from small to large. Today, too few do:

- A 40-year-old US manufacturing plant employs almost **eight times** as many workers as one under five years old; surviving Indian plants show little growth with age, a gap that could lower manufacturing productivity by about 25% [[6]](#ref-6).
- "Dwarfs" — firms with fewer than 100 workers that are more than 10 years old — make up more than half of India's organised manufacturing firms but contribute only 14% of its jobs and 8% of its productivity [[2]](#ref-2).
- Medium enterprises are just **0.3%** of registered MSMEs (67,923 firms), yet earn about 40% of MSME export income [[3]](#ref-3).

The research points to the owner's attention as one reason firms stall:

- **Owners are already stretched.** In a field study of Indian textile firms, owners worked an average of **68 hours a week**. Major decisions stayed within the owning family because owners did not trust outsiders, and firm size tracked the number of family members available to share control. Lack of information was a primary reason firms had not adopted better management; better information let owners delegate more, and better management raised productivity **17%** in the first year [[4]](#ref-4).
- **Indian CEOs are pulled into operations.** Across 1,114 CEOs — 356 of them in India — **36%** of CEOs in lower-income countries (Brazil and India) behave in ways mismatched to what their firms need, against 5% in high-income countries. That mismatch accounts for up to 13% of the labour-productivity gap between richer and poorer countries [[5]](#ref-5).

One caveat, stated plainly: economists dispute whether India has a "missing middle" in its firm-size distribution [[7]](#ref-7). The problem Aroh addresses is not a hole in the distribution; it is firms that stop growing once their owner runs out of attention.

**What it means for the category:** the owner who cannot let go because they cannot see is not only a private frustration — it is a constraint on national growth. Owner Intelligence supplies the information flow that the research links to delegation. Aroh cannot move GDP on its own, but it is aimed at a constraint the evidence identifies, at the moment India most needs its businesses to grow.

## AI became cheap enough to watch every business, every day

Owner Intelligence reads, reasons and drafts across a business's systems all day. Two years ago that would have cost more than the job was worth. It no longer does.

- **The trend:** Epoch AI finds that the price of matching GPT-4's performance on PhD-level science questions fell **40× per year**, with declines ranging from 9× to 900× per year depending on the performance level [[8]](#ref-8).
- **Aroh's own numbers:** Metorite's measured costs put a blended AI request at about **₹0.18** (at ₹95/US$), or roughly **₹944 per user per month** at average usage [[14]](#ref-14). For a 10-user organisation that is about ₹9,435 a month — a small fraction of an organisation-level fee.

**What it means for the category:** the economics of "always watching" now work for a ₹100 Cr business, not only for a conglomerate. Cost will keep falling; the scarce asset is the owner's trust, not the compute.

## Indian companies adopted AI faster than they made their data ready

- **47%** of Indian organisations have several GenAI use cases live in production; **91%** say speed of deployment is the biggest factor in what they buy [[13]](#ref-13).
- **69%** plan to increase AI investment and **73%** report some measurable return — yet only **4%** say their enterprise data is fully ready for AI at scale [[9]](#ref-9).

**What it means for the category:** buyers want results quickly, from data that is messy and spread across systems. That favours a product that works *across* existing systems, shows its sources and goes live fast — not one that asks the customer to clean and centralise their data first.

## Indian CEOs feel the pressure to keep pace more than their global peers

PwC's 29th CEO Survey reports that **66%** of Indian CEOs are concerned about keeping pace with technology and AI, against **42%** of CEOs globally who name it as their top concern [[10]](#ref-10). The India sample is small (around 50 CEOs) and the two figures do not measure exactly the same thing, but the direction is consistent with the other evidence: Indian business leaders feel AI pressure acutely.

**What it means for the category:** the anxiety Aroh addresses is already present and named by its buyers. Aroh does not have to create the worry; it has to resolve it.

## Frontier AI can now run inside India

On 29 September 2026, Amazon Bedrock made Claude Opus 5, Claude Sonnet 5 and Claude Haiku 4.5 available in India through geographic cross-Region inference across its Mumbai and Hyderabad Regions, so customers can keep inference processing within India [[15]](#ref-15). Open-weight models have reached the same point: DeepSeek released V4 under the MIT licence in April 2026 [[17]](#ref-17), so a frontier-class model can be run on Indian infrastructure by whoever chooses to host it.

**What it means for the category:** an owner can now be told, truthfully, that their business data is processed in India by frontier models. India hosting is a trust and procurement advantage — it removes a reason to say no. Aroh will present it that way, and not as a blanket legal requirement — data localisation obligations under Indian law need sector-by-sector legal review.

## Data protection law turns informal information flows into a liability

The Government of India notified the Digital Personal Data Protection Rules on **14 November 2025**, with an **18-month** phased compliance period [[12]](#ref-12) — bringing the main obligations into force by around May 2027.

Today, much of what an owner knows arrives through forwarded WhatsApp messages, personal inboxes and spreadsheets passed between people. Under the new rules, that informal flow of personal data carries obligations around notice, consent and security.

**What it means for the category:** for years, the status quo was the safe choice and new software was the risky one. Data protection law reverses that. A governed system — with consent, permissions, approvals and an audit trail — becomes the option an owner cannot be blamed for choosing.

## Software budgets are rising, but they are spent per department and per employee

Gartner forecasts Indian software spending to grow **17.6% to $24.7B** in 2026 [[11]](#ref-11). Most of that money buys departmental systems and per-employee tools: Microsoft 365 Copilot, for example, costs **₹2,495 per user per month**, paid yearly, on top of a qualifying Microsoft 365 licence [[16]](#ref-16).

**What it means for the category:** budgets are growing, but nothing in them is bought *for the owner* or works *across* departments. Owner Intelligence is a new line item with a different buyer — the gap category creation exists to fill.

## Seven drivers point the same way

| Driver | Evidence | Effect on the Owner Intelligence category | Timing |
| ------ | -------- | ----------------------------------------- | ------ |
| National growth stakes | $6T GDP in 2030 [[1]](#ref-1); owners at 68 hrs/week, delegation limited by trust and information [[4]](#ref-4) | Owner attention becomes a growth issue, not a comfort issue | 2026–2030 |
| AI cost collapse | Inference price for fixed capability −40×/year [[8]](#ref-8) | "Always watching" becomes affordable for ₹100 Cr firms | Now, continuing |
| Adoption ahead of readiness | 47% in production vs 4% data-ready [[13]](#ref-13), [[9]](#ref-9) | Favours cross-system products that go live fast | Now |
| CEO pressure | 66% India vs 42% global [[10]](#ref-10) | The anxiety is already named by buyers | Now |
| India-hosted frontier AI | Bedrock India, 29 Sep 2026 [[15]](#ref-15) | Removes a trust objection | From Q4 2026 |
| Data protection law | DPDP Rules 14 Nov 2025, 18-month phase-in [[12]](#ref-12) | Status quo becomes the risky choice | Through May 2027 |
| Rising, fragmented budgets | Software +17.6% to $24.7B [[11]](#ref-11); per-user AI pricing [[16]](#ref-16) | Room for a new, owner-level line item | 2026 onward |

### Key Insights

- India's path to $6T by 2030 [[1]](#ref-1) runs through firms that grow; the evidence ties stalled growth to owners who are stretched and cannot delegate without better information [[4]](#ref-4), [[5]](#ref-5).
- The status quo — the owner as integration layer — is being squeezed from four sides at once: cost, pressure, trust and law.
- AI cost is no longer the constraint: inference prices for a fixed capability fall about 40× a year [[8]](#ref-8). The constraint is the owner's trust.
- Data protection law [[12]](#ref-12) flips the risk calculation: informal information flows become the liability, and governed software becomes the safe choice.
- India-hosted frontier AI [[15]](#ref-15) removes the last easy reason for an owner to say no.

### Investment Implications

The drivers favour a company that moves now. Costs are falling for everyone, so the advantage will not come from cheaper AI; it will come from being the first name owners associate with Owner Intelligence, and from the trust built while the law and the market shift. The window is roughly the DPDP phase-in period to May 2027: during that time owners are re-examining how information flows through their businesses, and the category leader will be the company in the room when they do.

---

## References & Sources

### Government & Macroeconomic Data

<a name="ref-1"></a>

1. **IMF World Economic Outlook — GDP, current prices (NGDPD), India**
   - Nominal GDP (US$T): 2025 3.909; 2026 4.060; 2029 5.542; 2030 6.130; 2031 6.744
   - Accessed 24 Oct 2026 (October 2026 WEO series)
   - Source: International Monetary Fund, DataMapper
   - URL: https://www.imf.org/external/datamapper/api/v1/NGDPD/IND

<a name="ref-2"></a>

2. **Economic Survey 2018–19, Vol. 1, Ch. 3 — Nourishing Dwarfs to become Giants**
   - Firms with < 100 workers and > 10 years old: more than half of organised manufacturing firms, 14% of employment, 8% of productivity
   - Source: Ministry of Finance, Government of India (Jul 2019)
   - URL: https://www.indiabudget.gov.in/budget2019-20/economicsurvey/doc/vol1chapter/echap03_vol1.pdf

<a name="ref-3"></a>

3. **NITI Aayog — Designing a Policy for Medium Enterprises (May 2025)**
   - Medium enterprises: 0.3% of registered MSMEs (67,923 firms); ~40% of MSME export income
   - Source: NITI Aayog (prepared with ASCI)
   - URL: https://www.niti.gov.in/sites/default/files/2025-05/Designing-a-Policy-for-Medium-Enterprises.pdf

### Academic Research

<a name="ref-4"></a>

4. **Bloom, Eifert, Mahajan, McKenzie, Roberts — "Does Management Matter? Evidence from India"**
   - Owners averaged 68 hours/week; decision power kept within the family due to lack of trust in outsiders; informational barriers a primary reason for poor management; +17% productivity in the first year
   - Source: Quarterly Journal of Economics 128(1), 2013; NBER Working Paper 16658 (2011)
   - URL: https://doi.org/10.1093/qje/qjs044

<a name="ref-5"></a>

5. **Bandiera, Hansen, Prat, Sadun — "CEO Behavior and Firm Performance"**
   - 1,114 CEOs in six countries (356 in India); 36% CEO–firm mismatch in Brazil/India vs 5% in high-income countries; mismatch explains up to 13% of the cross-country labour-productivity gap
   - Source: Journal of Political Economy 128(4), 2020; NBER Working Paper 23248
   - URL: https://doi.org/10.1086/705331

<a name="ref-6"></a>

6. **Hsieh & Klenow — "The Life Cycle of Plants in India and Mexico"**
   - 40-year-old US plants employ almost 8× the workers of plants under 5; Indian plants show little growth; ~25% manufacturing productivity effect
   - Source: Quarterly Journal of Economics, 2014; NBER Working Paper 18133
   - URL: https://www.nber.org/papers/w18133

<a name="ref-7"></a>

7. **Hsieh & Olken — "The Missing 'Missing Middle'"**
   - Finds no bimodal "missing middle" in the firm-size distribution of India, Indonesia and Mexico
   - Source: Journal of Economic Perspectives 28(3), 2014
   - URL: https://www.aeaweb.org/articles?id=10.1257/jep.28.3.89

### Market Research & Industry Reports

<a name="ref-8"></a>

8. **Epoch AI — LLM inference prices have fallen rapidly but unequally across tasks**
   - Price to reach GPT-4's performance on PhD-level science questions fell 40× per year; range 9×–900× per year by milestone
   - Published 12 Mar 2025
   - Source: Epoch AI
   - URL: https://epoch.ai/data-insights/llm-inference-price-trends

<a name="ref-9"></a>

9. **Dun & Bradstreet AI Momentum Survey (India release)**
   - 69% plan to increase AI investment; 73% report measurable return; 4% have data fully AI-ready
   - Released Mumbai, 4 Aug 2026
   - Source: Dun & Bradstreet India
   - URL: https://www.dnb.co.in/media/press-release-details/3161

<a name="ref-10"></a>

10. **PwC 29th Annual Global CEO Survey — India findings (2026)**
   - 66% of Indian CEOs concerned about keeping pace with technology and AI vs 42% globally (top concern)
   - India sample ~50 of 4,454 CEOs
   - Source: Business Today (reporting PwC India); PwC
   - URL: https://www.businesstoday.in/amp/magazine/deep-dive/story/india-inc-needs-to-make-ai-centric-culture-a-c-suite-imperative-524893-2026-04-09

<a name="ref-11"></a>

11. **Gartner — India IT Spending Forecast 2026**
   - India software spending $24.7B in 2026, +17.6%; total IT $176.3B
   - Released 18 Nov 2025
   - Source: Gartner
   - URL: https://www.gartner.com/en/newsroom/press-releases/2025-11-18-gartner-forecasts-india-it-spending-to-exceed-176-billion-us-dollars-in-2026

<a name="ref-12"></a>

12. **PIB — DPDP Rules, 2025 Notified: A Citizen-Centric Framework for Privacy Protection**
   - Rules notified 14 Nov 2025; eighteen-month period for phased compliance
   - Source: Press Information Bureau, Government of India (17 Nov 2025)
   - URL: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf

### Company Announcements & Pricing

<a name="ref-13"></a>

13. **EY — The AIdea of India 2026: India Survey on GenAI Adoption**
   - 47% with multiple GenAI use cases in production; 91% cite speed of deployment as the biggest buying factor
   - 200+ Indian enterprise leaders; published 16 Nov 2025
   - Source: EY India
   - URL: https://www.ey.com/en_in/insights/ai/agentic-ai-india/aidea-survey-findings

<a name="ref-14"></a>

14. **Metorite Cost Plan (prepared 22 Oct 2026), recalculated at ₹95/US$**
   - Blended AI request $0.0019 (50% cheaper-model routing) ≈ ₹0.18; ₹944/user/month at 0.55× usage
   - Source: Hathi Labs (internal)
   - URL: https://claude.ai/artifact/KENqXY5J6s59B8hqHEvAAq

### Government Policy & Legislation

<a name="ref-15"></a>

15. **AWS — Amazon Bedrock expands Claude model availability to India, South Korea and Singapore**
   - Claude Opus 5, Sonnet 5 and Haiku 4.5 in India via geographic cross-Region inference across Mumbai and Hyderabad
   - Posted 29 Sep 2026
   - Source: Amazon Web Services
   - URL: https://aws.amazon.com/about-aws/whats-new/2026/09/claude-region-expansion-in-sk/

### Internal Data

<a name="ref-16"></a>

16. **Microsoft 365 Copilot — Enterprise Pricing (India)**
   - ₹2,495 per user/month, paid yearly, GST extra; requires a qualifying Microsoft 365 licence
   - Source: Microsoft
   - URL: https://www.microsoft.com/en-in/copilot/pricing/enterprise

### Open-Weight Models

<a name="ref-17"></a>

17. **Simon Willison — DeepSeek V4 (24 Apr 2026)**
    - V4 open weights on Hugging Face under the standard MIT licence; V4-Pro 1.6T total / 49B active parameters; V4-Flash 284B / 13B active
    - Source: Simon Willison's Weblog
    - URL: https://feeds.simonwillison.net/2026/Apr/24/deepseek-v4/
