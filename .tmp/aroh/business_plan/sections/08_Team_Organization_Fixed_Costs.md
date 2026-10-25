# Team & Costs: A Company Designed to Earn Trust, Teach the Category and Productise

> **Last Updated:** 2026-10-25
> **Project:** Aroh
> **Status:** Draft — generated from the cost model by `write_section08.py`

## Executive Summary

Category design says the company itself must be built to serve the category, not just the product [[1]](#ref-1) — here, the Owner Intelligence category. Aroh's organisation does three jobs: **earn the owner's trust** in person (forward-deployed engineers on site), **teach the market a new category** (a marketing budget that grows with revenue), and **productise** what it learns so that onboarding stays near 20 engineer-hours per customer (developers building reusable connectors).

In the base case the team grows from **13 people at the end of the pre-launch period to 21, 33 and 53** at the end of FY2027–28, FY2028–29 and FY2029–30 [[3]](#ref-3). The five-month pre-launch stub loses **₹2.70 Cr at EBITDA level** — the team is in place, but the fifty direct customers are onboarded only in March and contribute almost no recognised revenue yet. From FY2027–28 EBITDA is **₹9.93 Cr, ₹20.35 Cr and ₹41.67 Cr** [[3]](#ref-3). If those fifty do not sign, the downside (the previous plan) loses ₹2.54 Cr, ₹5.65 Cr and ₹4.93 Cr before turning profitable — the case Section 09 funds against.

The unit economics are strong if the assumptions hold: each customer costs about **₹8.6L to acquire** in FY2029–30, pays that back in about **2.4 months** once the ₹6L setup fee is counted, and is worth about **₹94L over five years — 10.9 times its acquisition cost** [[3]](#ref-3).

---

## The organisation is shaped by the category, not by a template

| Job the category demands | Who does it | Why this shape |
| ------------------------ | ----------- | -------------- |
| **Earn the owner's trust** | Forward-deployed engineers (FDEs), on site for pilots and onboarding | An owner hands over email, ERP and WhatsApp only to people they have met. Sutherland's costly signalling: turning up in person says "we are serious" in a way no demo can [[2]](#ref-2). |
| **Teach the market a new category** | Founders, then a sales lead and account executives; marketing of at least 10% of revenue from FY2028–29 | Owners must recognise the problem before they buy the answer; that takes evangelism, events and stories. |
| **Productise what we learn** | Developers (4 → 4 → 6 → 10) | Every connector and exception pattern built once keeps onboarding near 20 hours — the difference between software and services economics [[4]](#ref-4). |
| **Keep customers** | Customer success, one person per 30 live organisations | A new category needs more hand-holding than a mature one. |

## The team grows from 13 to 53 people

**Base case, end-of-period headcount** [[3]](#ref-3), [[5]](#ref-5):

| Role | Monthly salary (FY2027–28) | Pre-launch* | FY2027–28 | FY2028–29 | FY2029–30 | Basis |
| ---- | -------------------------: | ---: | ---: | ---: | ---: | ----- |
| Leadership | ₹6.0L | 3 | 3 | 3 | 3 | Owner decision |
| Developers | ₹2.1L + 2 Claude 20x plans | 4 | 4 | 6 | 10 | Owner decision |
| Forward-deployed engineers | ₹2.5L + 1 Claude 5x plan | 4 | 4 | 6 | 12 | Capacity rule, with the plan as a floor |
| Customer success | ₹1.5L | 2 | 5 | 10 | 17 | 1 per 30 live organisations |
| Sales lead + account executives (₹3.0L / ₹1.0L + 15% commission) | | 0 | 5 | 8 | 11 | Founder-led in pre-launch; 1 AE per 25 new customers |
| **Total** | | **13** | **21** | **33** | **53** | |

*Pre-launch is a five-month stub period (November 2026–March 2027), not a financial year, and is not annualised. Its figures are recognised revenue and cost for those five months only; annual contracts signed in March are billed upfront but recognised over the following twelve months. Salaries rise 10% a year from FY2028–29; staff are paid from the start of the period they join ("hire ahead of demand").

**FDE capacity check.** Onboarding takes about 20 engineer-hours per organisation; an FDE spends 60% of a 140-hour month on it [[5]](#ref-5):

| | Pre-launch* | FY2027–28 | FY2028–29 | FY2029–30 |
| - | ---: | ---: | ---: | ---: |
| Onboardings (free pilots + direct contracts) | 60 | 141 | 236 | 329 |
| Onboarding hours | 1,200 | 2,820 | 4,714 | 6,572 |
| FDEs needed for onboarding | 2.9 | 2.8 | 4.7 | 6.5 |
| FDEs planned | 4 | 4 | 6 | 12 |
| Share of FDE onboarding capacity used | 71% | 70% | 78% | 54% |

The pre-launch surge — ten pilots and fifty direct contracts in about four months — is what sizes the early FDE team.

## People are the cost; AI stays a small share of revenue

**Base case, ₹ crore** [[3]](#ref-3):

| Line | Pre-launch* | FY2027–28 | FY2028–29 | FY2029–30 |
| ---- | ------: | ------: | ------: | ------: |
| **Revenue** | **0.78** | **25.38** | **52.59** | **95.76** |
| AI processing | 0.05 | 1.43 | 3.14 | 5.64 |
| Production infrastructure (compute, RAM, storage, bandwidth, backups, monitoring) | 0.21 | 0.85 | 1.29 | 1.92 |
| Customer success | 0.15 | 0.90 | 1.98 | 3.70 |
| Forward-deployed engineers (salaries) | 0.50 | 1.20 | 1.98 | 4.36 |
| **Cost of delivery** | **0.91** | **4.38** | **8.39** | **15.62** |
| **Gross profit** | **−0.13** | **21.00** | **44.19** | **80.14** |
| Gross margin | -17.0% | 82.7% | 84.0% | 83.7% |
| Engineering (incl. the team's AI tools) | 0.54 | 1.30 | 2.10 | 3.80 |
| Leadership | 0.90 | 2.16 | 2.38 | 2.61 |
| Sales salaries | 0.00 | 0.84 | 1.32 | 1.89 |
| Sales commission | 0.00 | 2.66 | 4.46 | 6.21 |
| Category-creation marketing | 0.20 | 1.00 | 5.26 | 9.58 |
| Development and operations cloud (agent swarms, CI, staging) | 0.40 | 2.00 | 4.00 | 7.00 |
| Onboarding and pilot travel | 0.30 | 0.70 | 1.18 | 1.64 |
| General and administrative | 0.10 | 0.40 | 3.16 | 5.75 |
| Security and certification (one-time) | 0.13 | 0.00 | 0.00 | 0.00 |
| **Operating expenses** | **2.57** | **11.07** | **23.84** | **38.47** |
| **EBITDA** | **−2.70** | **9.93** | **20.35** | **41.67** |
| EBITDA margin | -346% | 39% | 39% | 44% |
| Laptops for every new hire (capital spend) | 0.24 | 0.10 | 0.19 | 0.35 |

**Two infrastructure layers are costed explicitly.**

- **Production** (charged to cost of delivery): a platform floor of ₹4L a month from day one — multi-zone, India-hosted, with monitoring and backups — plus ₹3,000 per customer per month for compute, RAM, storage and bandwidth — about 3.4 times the ₹880 per organisation measured on today's setup, to cover redundancy, disaster recovery and India-hosted capacity. AI calls are priced separately at today's measured DeepSeek V4 cost per request [[6]](#ref-6).
- **Development and operations** (an operating expense): a cloud budget of ₹0.4 Cr in pre-launch, then ₹2 / 4 / 7 Cr a year, for development and test environments, CI, and swarms of AI agents doing engineering, DevOps and customer-support work [[5]](#ref-5). It sits on top of the Claude plans already costed for developers and engineers. In the downside it is held to half until customers justify it.
- **People's equipment:** every new hire gets a laptop — ₹2.3L for engineers, ₹1.2L for everyone else.

The founders' thesis is that this is why margins run high: AI-driven development and delivery let a team of 53 serve 500 customers. It is a plan assumption, not yet an observed result, and the reasonability checks below treat it that way. From FY2028–29 marketing and G&A grow with revenue — at least 10% and 6% of revenue respectively — so the cost base keeps pace with 500 customers. Security and certification (₹12.7L) is spent in pre-launch because it must be complete before the first paid contract.

**Revenue per employee:** ₹1.21 Cr in FY2027–28, ₹1.59 Cr in FY2028–29 and ₹1.81 Cr in FY2029–30.

## The downside keeps a smaller team

If the fifty pre-launch contracts do not materialise, the plan falls back to the previous ramp (0 → 20 → 90 → 250) and its smaller team [[3]](#ref-3):

| Downside | Pre-launch* | FY2027–28 | FY2028–29 | FY2029–30 |
| -------- | ------: | ------: | ------: | ------: |
| **Revenue** | **0.00** | **2.40** | **13.00** | **40.07** |
| Headcount, end of period | 9 | 12 | 21 | 40 |
| **EBITDA** | **−2.54** | **−5.65** | **−4.93** | **4.42** |

## Each customer pays back its acquisition cost in under three months

**Base case, at FY2029–30 costs** [[3]](#ref-3):

| Measure | Value | How it is calculated |
| ------- | ----: | -------------------- |
| Customer acquisition cost (CAC) | ₹8.6L | Sales salaries, commission, marketing, travel and pilot AI ÷ new customers |
| First-year contribution | ₹15.8L (88%) | ₹18L subscription − AI, servers and customer success |
| Onboarding cost per customer | ₹0.62L | 20 FDE-hours ÷ 70% conversion at FY2029–30 FDE cost |
| **Payback, counting the setup fee** | **2.4 months** | (CAC − net setup fee) ÷ monthly contribution |
| Payback, ignoring the setup fee | 6.5 months | CAC ÷ monthly contribution |
| Lifetime value, 5 years | ₹93.9L | Contribution with 7% uplift, extra seats and 10% churn, plus net setup fee |
| **LTV : CAC** | **10.9×** | |

The CAC sits inside the ₹6–10L planning range in the source strategy document [[4]](#ref-4).

## Five reasonability checks, stated plainly

| Check | Finding | Implication |
| ----- | ------- | ----------- |
| **EBITDA margins are very high** | 39% in FY2028–29 and 44% in FY2029–30, after the full infrastructure and agent-cloud costs and with marketing and G&A scaled to revenue | The founders attribute this to AI-driven development and delivery; credible only if the early surge happens and onboarding stays near 20 hours, so investors will discount it |
| **The plan front-loads its hardest sale** | Fifty paid contracts in January–March 2027 from a standing start | The pre-launch period is funded by DEWiN so the seed is priced on this evidence (Section 09) |
| **Commission is material** | 15% of the ₹18L first-year subscription is ₹2.7L per deal — ₹6.21 Cr (6% of revenue) in FY2029–30 | Owner chose subscription-only commission |
| **LTV : CAC of 10.9× is high** | It depends on 10% churn, no discounting and 70% pilot conversion — all unproven | Section 10 stress-tests each |
| **AI cost assumes no India-hosting premium** | India-hosted processing assumed to cost the same per request as today's API | AI is about 6% of revenue; Section 10 tests 3× |

**Not in these figures:** employee stock options and founder equity (Section 09).

### Key Insights

- The organisation serves the category: FDEs earn trust in person, marketing teaches the category, developers productise so costs don't grow one-for-one with customers.
- Base case: 13 → 21 → 33 → 53 people; EBITDA ₹−2.70 (pre-launch stub) / ₹9.93 / ₹20.35 / ₹41.67 Cr [[3]](#ref-3).
- Gross margin, with onboarding and support people included, runs 83–84%; AI stays a small share of revenue.
- CAC ₹8.6L, payback about 2.4 months with the setup fee, five-year LTV : CAC of 10.9× [[3]](#ref-3).

### Investment Implications

If fifty owners sign by March 2027, Aroh posts a modest loss only in the five-month pre-launch stub, is profitable from FY2027–28 and strongly cash-generating by FY2029–30. If they do not, the downside is the original plan: a team of 9 to 40 people and about ₹13.12 Cr of operating losses before break-even. Every cost line here can be dialled down if the ramp is slow; the milestone gates in Section 09 make sure it is.

---

## References & Sources

### Books & Frameworks

<a name="ref-1"></a>

1. **Al Ramadan, Dave Peterson, Christopher Lochhead, Kevin Maney — *Play Bigger* (2016)**
   - Category design: company design, product design and category design reinforce each other
   - Source: HarperBusiness (ISBN 9780062407610)
   - URL: https://stvp.stanford.edu/wp-content/uploads/sites/3/2024/09/how-to-be-a-category-king-entire-talk-transcript.pdf

<a name="ref-2"></a>

2. **Rory Sutherland — *Alchemy: The Surprising Power of Ideas That Don't Make Sense* (2019)**
   - Costly signalling: effort and expense as evidence of commitment
   - Source: WH Allen / Penguin Random House
   - URL: N/A (book)

### Internal Data

<a name="ref-3"></a>

3. **Aroh cost and unit-economics model**
   - Computed by `.tmp/aroh/config/cost_calc.py` (output `cost_results.json`), on top of `revenue_calc.py`
   - Source: Aroh plan working files (internal)
   - URL: N/A (internal)

<a name="ref-4"></a>

4. **Aroh: Strategic Narrative and Investor-Ready Business Case**
   - CAC planning range ₹6–10L per logo; connector platform vs services economics
   - Source: DEWiN / Hathi Labs (internal strategy document)
   - URL: N/A (internal)

<a name="ref-5"></a>

5. **Aroh assumption register — owner decisions**
   - Headcount, salaries, capacity rule, 20-hour onboarding, marketing and G&A scaling, travel, customer-success ratio, 10% raises (A-042 to A-079)
   - Source: `.tmp/aroh/notes/assumption_register.md`
   - URL: N/A (internal)

<a name="ref-6"></a>

6. **Metorite Cost Plan (prepared 22 Oct 2026), recalculated at ₹95/US$**
   - Developer ₹2.1L/month; FDE ₹2.5L/month; CS ₹1.5L/month; Claude 20x ₹23,999 and 5x ₹11,999 per month; laptops ₹2.3L; security one-time ₹12.7L; AI cost per request measured from Metorite's usage log (DeepSeek V4)
   - Source: Hathi Labs (internal)
   - URL: https://claude.ai/artifact/KENqXY5J6s59B8hqHEvAAq
