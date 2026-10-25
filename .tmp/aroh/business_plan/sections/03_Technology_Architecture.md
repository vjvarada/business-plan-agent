# Technology Architecture: The Product Is the Proof of the Point of View

> **Last Updated:** 2026-10-24
> **Project:** Aroh
> **Status:** Draft

## Executive Summary

A category is only as believable as the product that demonstrates it. Aroh's architecture is built to prove one claim every day: that **Owner Intelligence** can watch a whole business, tell the owner what matters, show its sources and act only with permission.

Aroh does not start from zero. Its building blocks run in production today as Metorite, developed by Hathi Labs: ten live apps, an approval card before any change, row-level separation of each company's data, a model router that can switch AI providers, and databases hosted in Mumbai [[3]](#ref-3). What Aroh adds is the Chief of Staff layer on top — connectors to the systems owners already use, an exception engine, the 07:30 brief and 18:30 close-out, and an Enterprise Execution Graph that learns what actually leads to good and bad outcomes [[5]](#ref-5).

Two architectural choices follow from the category's promise. First, **trust is designed in**, because software that can read email and change records has a far larger blast radius than a chatbot. Second, **AI processing moves into India before the first paid contract.** Aroh runs on DeepSeek V4-class models today at a measured ₹0.18 per request [[4]](#ref-4); because those model weights are openly licensed [[7]](#ref-7), the same class of model can be served from Indian infrastructure [[1]](#ref-1), [[8]](#ref-8) — so every paying customer's data is both stored and processed in India.

---

## Aroh works the way a good chief of staff works

A good chief of staff observes, filters, prepares and acts within a mandate. Aroh's autonomy model follows the same four steps, with defaults that keep the owner in charge [[5]](#ref-5):

| Step | Example | Default |
| ---- | ------- | ------- |
| **Observe** | Detect that debtor ageing has worsened | Automatic |
| **Recommend** | Suggest a review with the CFO | Automatic |
| **Prepare** | Draft the email, WhatsApp reply or CRM update | Automatic |
| **Execute** | Send the message, change the record, approve the workflow | Set by policy; sensitive actions always need explicit approval |

Autonomy is configured by **user × system × action × amount**. A reminder to an internal sales manager and approval of a large payment never share a permission.

**A day with Aroh:**

| Time | What happens |
| ---- | ------------ |
| 07:30 | "Three things deserve your attention today" — e.g., receivables over a threshold have worsened, a key customer's forecast has changed, a factory milestone now threatens a commitment |
| 07:35 | The owner taps the first item. Aroh reconciles ERP receivables, CRM account data, the CFO's email and an authorised message thread. Every statement links to its source. |
| 07:37 | Aroh suggests three actions, marking which are recommended and which need approval |
| 07:38 | The owner approves a message to the regional head, a CRM follow-up and a CFO review; Aroh watches for the reply |
| During the day | Silence — unless a threshold is crossed, a commitment is missed or something changes a decision |
| 18:30 | "Seven actions started; five completed; two need attention tomorrow." |

## Production building blocks already exist as Metorite

Aroh is assembled from building blocks that are already running, not from a slide [[3]](#ref-3):

| Building block | Status today | Role in Aroh |
| -------------- | ------------ | ------------ |
| 10 live apps — My Tasks, Calendar, Profile, Access, Projects, People, AI Chat, Approvals, Organisation, Appearance | Live | The owner's and executive team's workspace |
| Approval card before any AI change | Live | The "nothing happens without me" guarantee |
| Row-level multi-tenancy | Live | Each company's data kept separate in the database itself |
| Model router (LiteLLM) across providers | Live (DeepSeek in production; Claude, OpenAI, Gemini configured as options) | Vendor-neutral model plane |
| Specialist agents — tasks, CRM, projects, sales (Zoho CRM), delivery, triage, reconciliation, billing, strategy | Registered | Seed of the Chief of Staff's skills |
| Evaluation harness (17 golden trajectories) | Built | Regression tests for agent behaviour |
| Email (Microsoft 365, Gmail, IMAP), WhatsApp Business via Meta's official platform, CRM, meeting notes | Preview | The channels Aroh watches |
| Postgres + pgvector on Supabase, Mumbai region | Live | India-hosted system of record |

**Gaps, stated plainly** [[3]](#ref-3): email and WhatsApp are still in preview; there is no durable job queue yet; long-term memory is off by default; several security controls are designed but not yet enforced; and only two organisations run in production. These are the first items on the build plan below.

## What Aroh adds turns a workspace into Owner Intelligence

| Layer | What it does | Why the category needs it |
| ----- | ------------ | ------------------------- |
| **Business connectors** | Reads ERP/accounting (e.g., Tally, Zoho, Odoo), CRM, email, calendar and authorised WhatsApp Business flows | The owner's context lives in many systems; Aroh must see across them |
| **Exception engine** | Thresholds and patterns that decide what deserves attention | "Silence unless something matters" is the product |
| **Brief and close-out** | 07:30 brief, 18:30 close-out, on mobile and WhatsApp | The daily promise customers can check |
| **Provenance** | "Why Aroh knows this" on every claim | Trust in the number |
| **Policy engine** | Permissions by user × system × action × amount | Act only within the mandate |
| **Enterprise Execution Graph** | Person → Account → Order → Project → Commitment → Decision → Action → Outcome | Organisational memory and the data moat |

**WhatsApp is the cockpit, not the database.** Aroh connects only through Meta's official WhatsApp Business Platform [[3]](#ref-3). It will not scrape personal sessions. Reading existing group conversations depends on Meta's platform policy, so the plan treats it as a dependency, not a promised feature [[5]](#ref-5).

## The moat is the Execution Graph, not the customer's data

Aroh will not build its value on owning customer data — that would make it harder to sell and harder to acquire [[5]](#ref-5). The defensible asset is what Aroh learns about *how work gets done*:

1. **Organisational memory per customer** — which promises were made, who was assigned, what happened. This raises switching costs and improves relevance month by month.
2. **Product-level evaluation intelligence** — anonymised or permissioned failure cases, synthetic evaluations and policy templates that make Aroh better without exposing any one customer's content.
3. **Workflow intelligence** — which signals actually come before a missed collection, a lost sale or a late project. This is worth far more than raw chat history.

The progression: data aggregation → business context → execution graph → predictive exceptions → trusted actions → organisational memory.

## AI processing moves into India before the first paid contract

**Today.** Metorite routes requests to DeepSeek V4 models through DeepSeek's own API: V4-Pro for reasoning and V4-Flash for routine work [[3]](#ref-3). Measured over 15 users, a main-model request costs **$0.0030** and a cheaper-model request **$0.0008**; with half of requests on the cheaper model, a request costs about **₹0.18** at ₹95/US$ [[4]](#ref-4). Customer data is stored in Mumbai, but AI processing happens outside India.

**Why that has to change before Aroh takes money.** India's Finance Ministry told its officials to avoid AI tools such as ChatGPT and DeepSeek on office devices, citing the confidentiality of government data [[10]](#ref-10). An owner's procurement team will raise the same question. An Owner Intelligence product that reads the owner's email, ERP and messages cannot ask for that trust while processing outside the country.

**How it moves.** DeepSeek released V4 as open weights under the MIT licence — V4-Pro with 1.6T total parameters (49B active per token) and V4-Flash with 284B (13B active) [[7]](#ref-7). That means the same class of model can run on Indian infrastructure:

| Route | What exists today | Trade-off |
| ----- | ----------------- | --------- |
| Indian cloud hosts of open models | Yotta and Krutrim have served DeepSeek models from Indian data centres [[8]](#ref-8), [[9]](#ref-9) | Fastest; depends on a provider offering V4-class models at scale |
| Self-hosting on Indian GPUs | IndiaAI Compute lists 8 × H200 at ₹785/hour on a 12-month reservation [[1]](#ref-1) | Full control; Aroh carries the operations work |
| Indian model providers | Sarvam serves its own models from Indian data centres (Section 04) | Different models; quality at Aroh's tasks to be tested |
| Frontier models in Indian regions | Claude Opus 5, Sonnet 5 and Haiku 4.5 on Amazon Bedrock in Mumbai and Hyderabad [[2]](#ref-2) | Escalation path for the hardest reasoning; higher cost per request |

**Decision (owner, Stage 3):**

1. **Pilots** may run on the current API, with written disclosure that AI processing happens outside India.
2. **Every paid contract** runs on India-hosted processing, through one of the routes above, behind Aroh's own model router.
3. **The financial model** prices AI at today's measured DeepSeek V4 cost per request. This is an owner assumption — an India-hosted provider may charge a premium — and Stage 4 tests it in sensitivity analysis.

**When self-hosting pays.** The source strategy document estimated that private hosting would beat API pricing at around 35–40 organisations, using an assumed ₹0.40 per interaction [[5]](#ref-5). At the measured ₹0.18, the bar is higher. A node large enough for V4-Pro (8 × H200, an engineering estimate) costs about ₹8.8L a month all-in:

| Usage level | API cost per org/month (measured) | Organisations needed for a self-hosted node to break even |
| ----------- | --------------------------------: | --------------------------------------------------------: |
| Typical user (0.1×) | ₹1,716 | Never (API cheaper than per-org variable cost) |
| Average active day (0.55×) | ₹9,435 | ~137 |
| Busiest user today (1.0×) | ₹17,155 | ~62 |

*Node = 8 × H200 at ₹785/hr × 730 hrs (₹5.73L) + ₹1.08L overhead + ₹2.0L MLOps = ₹8.81L/month fixed, plus ₹3,000 per org variable [[1]](#ref-1), [[5]](#ref-5). Break-even = fixed cost ÷ (API cost − variable cost) per org. How many organisations one node can serve at acceptable latency is unvalidated and must be load-tested. 10 users per org; 22 active days; 50% cheaper-model routing [[4]](#ref-4).*

At the base-case ramp (150 customers at the end of FY2027–28, 300 a year later), self-hosting starts to make economic sense during FY2027–28 — and earlier if India-hosted API providers charge a large premium. The trigger is measured utilisation, not customer count. A dedicated private deployment for a single customer is available on request, priced to cover its cost, and is not part of the base financial model.

## Trust is designed in, because an agent with access has a larger blast radius

| Control | Purpose |
| ------- | ------- |
| Tenant isolation at the database row level | One company can never see another's data |
| Per-connector scopes and least-privilege credentials | Aroh reads only what the owner authorises |
| Approval workflows and deterministic action policies | Nothing sensitive happens without a human |
| Tamper-resistant action log | Every action can be audited |
| Provenance on every important claim | The owner can check where a number came from |
| Prompt-injection defences and data-loss prevention | Email and messages cannot instruct Aroh to act |
| Written employee consent before ingesting email or WhatsApp | Meets data-protection expectations from day one |
| Data stored in India; AI processing in India for every paid customer; customer-managed encryption for large deployments | Removes the procurement objection |

**Certification roadmap and cost** (mid-point estimates, not quotes) [[4]](#ref-4):

| Item | Why it matters | Estimate |
| ---- | -------------- | -------: |
| Google restricted-scope security review (Gmail) | Required before Gmail access goes live | ₹2.2L |
| External penetration test | Independent proof the controls hold | ₹3.0L |
| ISO 27001 certificate | Asked for by larger organisations | ₹5.0L |
| DPDP compliance work | Policies, contracts and processes | ₹2.5L |
| **Total one-time** | | **₹12.7L** |

## Perception fixes deliver felt value for less than engineering fixes

Rory Sutherland's rule: before paying to change reality, ask whether changing perception delivers the same felt value [[6]](#ref-6). For each worry an owner has, Aroh's roadmap chooses the cheaper fix first:

| What the owner feels | Expensive engineering fix | Cheaper perception fix Aroh ships first |
| -------------------- | ------------------------- | --------------------------------------- |
| "Is it still watching?" | Real-time streaming of every event | A midday "nothing needs you" check-in |
| "Can I trust this number?" | Perfect accuracy everywhere | Source shown and a confidence label on every claim |
| "Is it doing things behind my back?" | Fine-grained autonomy settings at launch | An approval card before action, and the 18:30 log of everything done |
| "Why is it slow?" | Faster, costlier models | A progress line: "Checking Tally and your inbox…" |
| "Setup will take months" | Every integration on day one | A useful first brief in week one from email plus one core system |

## Aroh keeps what a human chief of staff provides

The doorman fallacy warns against replacing a role by its visible task and losing its unseen value [[6]](#ref-6). A human chief of staff gives more than a schedule:

| Unseen value of a human chief of staff | How Aroh keeps it |
| -------------------------------------- | ----------------- |
| Discretion | Permissions per person and topic; sensitive items go only to the owner |
| Judgment | Ranked priorities with reasons; learns from what the owner accepts or overrides |
| Loyalty | Works for the owner; customer data stays the customer's |
| Memory | The Execution Graph remembers every commitment and outcome |
| Tact | Drafts in the owner's voice; nothing sent without approval |

## Swarms of agents build, run and support the platform

The founders' plan is to run Aroh the way it expects its customers to run: with AI agents doing a large share of the engineering, DevOps and customer-support work, supervised by a small human team. That needs real compute, so the financial model budgets it explicitly rather than treating it as a rounding error:

| Layer | What it pays for | Budget (base case) |
| ----- | ---------------- | ------------------ |
| **Development and operations cloud** | Development and test environments, continuous integration, staging, and always-on agent swarms for engineering, DevOps and support | ₹0.4 Cr in pre-launch, then ₹2.0 / 4.0 / 7.0 Cr a year (half that in the downside until customers justify it) |
| **Production infrastructure** | India-hosted compute, RAM, storage, bandwidth and internet connectivity, backups and disaster recovery, monitoring and security tooling | ₹4L a month platform floor plus ₹3,000 per customer a month |
| **AI processing** | Model calls for customers' briefs, drafts and actions | About ₹944 per user per month at average usage (measured) |
| **People's equipment and tools** | Laptops for every hire (₹2.3L engineers, ₹1.2L others) and Claude plans for developers and engineers | In the cost model (Section 08) |

The bet is that agents raise each person's output enough to keep headcount near 53 at 500 customers. That is a founder-stated assumption, not an observed result; the first evidence will be how many engineer-hours each new customer takes (target: 20) and how much support is resolved without a human.

## The build plan turns building blocks into Aroh within the 3-year horizon

| Phase | Focus | Exit test |
| ----- | ----- | --------- |
| **Year 1 — Prove it** | Close the production gaps (job queue, enforced security, email and WhatsApp out of preview); ship connectors for the launch sectors' common systems; 07:30 brief and 18:30 close-out; India-hosted AI processing before the first paid contract; Google security review and penetration test | Design partners use the brief daily; approvals work end to end |
| **Year 2 — Repeat it** | Reusable connector and configuration platform so onboarding stays near 40 engineer-hours; Execution Graph and predictive exceptions; ISO 27001 | New customers live without custom code |
| **Year 3 — Scale it** | Dedicated deployments on request; private serving where measured utilisation justifies it; deeper autonomy for proven workflows | Gross margin holds as customers grow |

The build plan's discipline: **every custom connector or bespoke dashboard pushes Aroh towards services economics; every reusable capability pushes it towards software economics** [[5]](#ref-5).

### Key Insights

- Aroh's building blocks already run in production as Metorite [[3]](#ref-3); the gaps are known and listed.
- Aroh runs on DeepSeek V4-class models at a measured ₹0.18 per request [[4]](#ref-4); because the weights are openly licensed [[7]](#ref-7), processing moves to Indian infrastructure before the first paid contract.
- At measured costs, a self-hosted node breaks even at roughly 137 organisations of average usage — reached during FY2027–28 in the base case; the trigger is measured utilisation.
- Trust is the product's foundation: approvals, sources, audit logs, consent, and data both stored and processed in India for paying customers.
- Perception fixes (sources shown, check-ins, approval cards) deliver the "control that brings calm" feeling before expensive engineering does.
- The Execution Graph, not customer data, is the moat.

### Investment Implications

Investors are not funding a research project. The core platform exists, runs in production and has a measured cost per user. Capital goes into the layer that makes it a category — connectors, the exception engine, the Execution Graph and the certifications that let owners say yes. The API-first decision keeps fixed infrastructure cost low until usage proves otherwise, protecting runway while the category is being established.

---

## References & Sources

### Government & Public Infrastructure

<a name="ref-1"></a>

1. **IndiaAI Compute Portal — GPU Price List**
   - 12-month reserved: H100 SXM (1×) ₹117/hr; H100 SXM (8×) ₹936/hr; H200 SXM (8×) ₹785/hr; L40S (1×) ₹45/hr
   - Last updated 14 Oct 2026
   - Source: IndiaAI Mission, Government of India
   - URL: https://compute.indiaai.gov.in/pricelist

### Company Announcements

<a name="ref-2"></a>

2. **AWS — Amazon Bedrock expands Claude model availability to India, South Korea and Singapore**
   - Claude Opus 5, Sonnet 5 and Haiku 4.5 in India via geographic cross-Region inference across Mumbai and Hyderabad
   - Posted 29 Sep 2026
   - Source: Amazon Web Services
   - URL: https://aws.amazon.com/about-aws/whats-new/2026/09/claude-region-expansion-in-sk/

### Internal Data

<a name="ref-3"></a>

3. **Metorite product repository, competitive assessment and website**
   - 10 live apps; approval card before any change; row-level multi-tenancy; LiteLLM router (DeepSeek in production); 17-trajectory eval harness; Supabase Mumbai; preview apps and admitted gaps (`COMPETITIVE_COMPARISON.md`, `project-docs/specs/launch_surface.md`, `infra/litellm/config.yaml`)
   - Source: Hathi Labs (internal repo `Hathi-Labs/Metorite`)
   - URL: https://metorite.com/

<a name="ref-4"></a>

4. **Metorite Cost Plan (prepared 22 Oct 2026), recalculated at ₹95/US$**
   - Measured from Metorite's own usage log and price feed (production on DeepSeek V4), 15 users, 24 Sep–22 Oct 2026: main model $0.0030/request, cheaper model $0.0008/request, 50% routing; 432 requests/day at 1.0×; security cost ranges (mid-points used)
   - Source: Hathi Labs (internal)
   - URL: https://claude.ai/artifact/KENqXY5J6s59B8hqHEvAAq

<a name="ref-5"></a>

5. **Aroh: Strategic Narrative and Investor-Ready Business Case**
   - Autonomy model; day-in-the-life; Enterprise Execution Graph; private-serving block assumptions (₹4.5L infra, ₹2.0L MLOps, ₹3,000/org, 50 orgs/block); WhatsApp policy dependency
   - Source: DEWiN / Hathi Labs (internal strategy document)
   - URL: N/A (internal)

### Books & Frameworks

<a name="ref-6"></a>

6. **Rory Sutherland — *Alchemy: The Surprising Power of Ideas That Don't Make Sense* (2019)**
   - Perception versus reality; the doorman fallacy
   - Source: WH Allen / Penguin Random House
   - URL: N/A (book)

### Open-Weight Models & Indian Hosting

<a name="ref-7"></a>

7. **Simon Willison — DeepSeek V4 (24 Apr 2026)**
   - V4 open weights on Hugging Face under the standard MIT licence; V4-Pro 1.6T total / 49B active parameters; V4-Flash 284B / 13B active; 1M-token context
   - Source: Simon Willison's Weblog
   - URL: https://feeds.simonwillison.net/2026/Apr/24/deepseek-v4/

<a name="ref-8"></a>

8. **Hiranandani's Yotta starts AI chatbot by deploying DeepSeek on Indian servers**
   - DeepSeek models served from Yotta's Mumbai data centre (Feb 2025)
   - Source: Outlook Business
   - URL: https://www.outlookbusiness.com/news/hiranandanis-yotta-starts-ai-chatbot-by-deploying-deepseek-on-indian-servers

<a name="ref-9"></a>

9. **Krutrim now hosts DeepSeek models on its cloud**
   - DeepSeek models live on Krutrim cloud, hosted on Indian servers (2025)
   - Source: Inc42
   - URL: https://inc42.com/buzz/krutrim-now-hosts-deepseek-models-on-its-cloud

### News & Media

<a name="ref-10"></a>

10. **Australian and Indian government employees warned against DeepSeek use**
    - India's Finance Ministry internal advisory (29 Jan 2025) asked officials to avoid AI tools such as ChatGPT and DeepSeek on office devices, citing confidentiality of government data (reported by Reuters)
    - Source: Semafor, 5 Feb 2025
    - URL: https://www.semafor.com/article/02/05/2025/australian-and-indian-government-employees-warned-against-deepseek-use
