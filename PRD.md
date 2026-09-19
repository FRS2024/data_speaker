# PRODUCT REQUIREMENTS DOCUMENT (PRD)

**Project Title:** Conversational Data Analysis Platform (Code-Interpreting Autonomous Analyst)  
**Document Version:** 1.0.0  
**Target Release:** MVP (Phase 1, Q1) → Enterprise Scale (Phase 4, Q4)  
**Author:** Senior Business & Startup Developer / Product Lead  
**Status:** Approved for Implementation  

---

## 1. Executive Summary

### 1.1 One-Paragraph Vision
The Conversational Data Analysis Platform democratizes data intelligence by combining an intuitive, natural-language conversational interface with an isolated, deterministic Python code execution engine. By eliminating the divide between black-box LLMs that hallucinate calculations and complex BI suites that demand dedicated data engineering, the platform acts as an always-available Principal Data Analyst—empowering anyone from non-technical founders to senior machine learning practitioners to ingest, clean, explore, model, and visualize complex datasets in seconds.

### 1.2 Problem Statement
Organizations across the globe generate massive volumes of tabular, semi-structured, and scientific data, yet the path from raw file to business decision remains severely bottlenecked:
* **The Data Team Backlog:** Business stakeholders routinely wait days or weeks for simple exploratory data analysis (EDA), cohort aggregations, or chart iterations from centralized data teams.
* **The Spreadsheet Ceiling:** Spreadsheets (Microsoft Excel, Google Sheets) freeze, crash, or corrupt when processing modern datasets (>100,000 rows), lack native support for columnar formats like Parquet, and obscure complex calculation logic inside fragile cell formulas.
* **The Generative AI Hallucination Trap:** Standard commercial chat interfaces (vanilla ChatGPT, Claude) are non-deterministic text prediction engines. When asked to compute percentages, correlations, or p-values over raw text, they frequently hallucinate figures because they lack a deterministic runtime.
* **Stateless Ephemeral Tools:** Existing code-interpreting chat interfaces run stateless containers that wipe variable memory between prompts, reset state upon connection drops, and offer zero visibility into intermediate DataFrame revisions.
* **Why Now?** The convergence of frontier code-generation models (Claude 3.5 Sonnet, GPT-4o), lightweight virtualization (gVisor, Firecracker microVMs), and client-side visualization frameworks (Plotly.js) makes it possible to deliver instant, secure, stateful, and interactive conversational analytics at sub-$0.02 cost per query.

### 1.3 Solution Overview
The platform couples an advanced agentic orchestrator with a stateful, pre-warmed execution sandbox:
1. **Multi-Format Ingestion:** Accepts CSV, XLSX, TSV, JSON, Parquet, and SQLite files up to 500MB with automated MIME validation and sub-second schema profiling.
2. **Schema-Only Context Synthesis:** Extracts columns, datatypes, missingness distributions, cardinality, and memory footprints, injecting only structural metadata into the LLM system prompt—ensuring 100% data privacy and zero raw-data leakage.
3. **Conversational Wrangling & Modeling:** Translates plain-English requests into idiomatic Python (Pandas/Polars/NumPy/SciPy), executing code within a persistent IPython kernel that preserves variable state across conversational turns.
4. **Self-Healing Reflexion Loop:** Automatically captures tracebacks if code execution fails, recursively prompting the LLM to diagnose and correct errors without user intervention (up to 3 retries).
5. **Interactive Client-Side Visualizations:** Serializes chart outputs to declarative Plotly JSON, rendered client-side with native zoom, pan, hover, and SVG/PNG export.
6. **Immutable State Versioning:** Creates automatic Parquet snapshots (`df_v0`, `df_v1`) after each mutation, enabling instant time-travel, branching, and undo/redo operations.
7. **Glass-Box Transparency:** Features an expandable Monaco code drawer exposing every line of executed Python code, execution duration, and standard output/error streams.

### 1.4 Target Users & Market Segments
```
┌────────────────────────────────────────────────────────────────────────┐
│                        TARGET MARKET SEGMENTS                          │
├─────────────────────────┬─────────────────────────┬────────────────────┤
│ Business & Growth       │ Data Scientists &       │ Executives &       │
│ Operations Analysts     │ Analytics Engineers     │ Founders           │
├─────────────────────────┼─────────────────────────┼────────────────────┤
│ • Marketing, Sales, Ops │ • Mid to Senior ICs     │ • C-Suite, VPs,    │
│ • Blocked by SQL/code   │ • Tedious EDA fatigue   │   Seed/Series A-B  │
│ • Fast cohort/funnel    │ • Wants clean Jupyter   │ • Needs instant    │
│   aggregations          │   notebook exports      │   board metrics    │
└─────────────────────────┴─────────────────────────┴────────────────────┘
```

### 1.5 Key Value Propositions
* **Zero-Hallucination Quantitative Rigor:** 100% of mathematical operations, filters, statistical tests, and aggregations are executed by a deterministic Python runtime—not predicted by an LLM neural network.
* **10x Faster Time-to-Insight:** Reduces initial data profiling and exploratory analysis time from 4 hours to under 60 seconds.
* **Complete Auditability (Glass-Box):** Every chart and table is backed by readable, reproducible Python code that can be inspected, edited, or downloaded as a standalone Jupyter Notebook (`.ipynb`).
* **Enterprise Security Guarantee:** Sandboxes execute under zero-outbound-network policies (`network: none`) with dropped Linux capabilities, preventing data exfiltration.

### 1.6 High-Level Business & Operational Metrics
| Metric | Baseline / Industry | Platform Target (MVP) | Target (Year 1) |
| :--- | :--- | :--- | :--- |
| **Activation Rate** (Upload → 3+ Queries) | 22% (Standard SaaS) | > 55% | > 65% |
| **Query Success Rate** (First-Pass Execution) | 70% (Naive Code Gen) | > 88% | > 95% (with Reflexion) |
| **Median Time to First Insight (TTFI)** | 15 minutes (Excel/BI) | < 45 seconds | < 30 seconds |
| **Weekly Active Users (WAU / MAU)** | 25% | > 40% | > 48% |
| **Net Revenue Retention (NRR)** | 100% | > 115% | > 130% |

---

## 2. Product Vision & Strategy

### 2.1 Long-Term Product Vision (3–5 Years)
* **Phase 1 (Months 1–6): The Conversational File Analyst.** Best-in-class conversational execution for static datasets (CSV, Excel, Parquet) with glass-box transparency, interactive visualization, and stateful time-travel.
* **Phase 2 (Months 7–18): The Connected Data Teammate.** Direct federated querying into data warehouses (Snowflake, BigQuery, Databricks, PostgreSQL). Scheduled automated reporting, anomaly alerting via Slack/Email, and team collaboration canvases.
* **Phase 3 (Months 19–36): The Autonomous Quantitative Agent.** Proactive predictive modeling, automated causal inference, econometric forecasting, and continuous data quality monitoring operating as an autonomous, self-directing data science team member.

### 2.2 North-Star Metric
**Weekly High-Confidence Completed Analyses (WHCCA):** Defined as any user session where an analytical file is uploaded, 3 or more analytical queries are successfully executed without unrecovered runtime errors, and the user exports an artifact (Plotly chart, cleaned CSV/Parquet, or Jupyter Notebook).

### 2.3 Positioning Statement
> *“For data-driven operators, analysts, and founders who need trusted, instant insights from complex datasets without waiting on overloaded engineering teams, our platform is a conversational data intelligence workspace that combines natural language with deterministic Python execution in secure, persistent sandboxes. Unlike ChatGPT Advanced Data Analysis, we provide full state versioning, client-side interactive Plotly charts, and team collaboration; unlike legacy BI tools like Tableau, we require zero dashboard configuration and deliver answers in seconds.”*

### 2.4 Competitive Landscape & Differentiation Matrix

| Dimension | Our Platform | Julius AI | ChatGPT Plus (Code Interpreter) | Tableau / PowerBI | Hex / Deepnote |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Execution Environment** | Stateful persistent IPython kernel | Stateful Python container | Ephemeral / short-lived container | Proprietary query engine | Collaborative reactive notebook |
| **Data Versioning** | Immutable Parquet branching (`df_v0` → `df_v1`) | Basic session history | None (in-memory wipe on reset) | Git/VCS on workbook XML | Cell-level Git versioning |
| **Visualization Output** | Native interactive Plotly.js (pan, zoom, hover) | Static PNG / basic Plotly | Static PNG / Matplotlib | Interactive proprietary canvas | Native interactive charts |
| **Code Visibility** | Glass-box Monaco drawer + full editability | Collapsible code box | Hidden behind dropdown | Proprietary drag-and-drop / DAX | First-class code cells |
| **Data Ingestion Limit** | 500MB (multi-file) | 100MB – 250MB | 512MB (ephemeral) | Multi-GB (via extracts) | Multi-GB (via warehouse) |
| **Self-Correction** | 3-tier Reflexion loop with AST validation | Basic retry | Basic retry | Manual formula debugging | Manual code debugging |
| **Enterprise Isolation** | Zero-network gVisor / Firecracker | Multi-tenant cloud | Multi-tenant cloud | Enterprise on-prem / cloud | Cloud VPC / on-prem |

### 2.5 Monetization & Business Model

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TIERED PLG SAAS PACKAGING                       │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ FREE / STARTER    │ PRO ANALYST       │ TEAM & ENTERPRISE              │
│ $0 / month        │ $29 / month       │ $79/user/mo or Enterprise Custom│
├───────────────────┼───────────────────┼────────────────────────────────┤
│ • 100MB file max  │ • 500MB file max  │ • Multi-GB warehouse sync      │
│ • 25 queries/mo   │ • Unlimited simple│ • Dedicated warm pool workers  │
│ • Shared sandbox  │ • 500 deep credits│ • SOC2 Type II, HIPAA, SSO/SAML│
│ • Community models│ • Sonnet & GPT-4o │ • Team shared workspaces       │
│ • PNG export only │ • Plotly/Notebook │ • Private VPC sandbox option   │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

#### Unit Economics & Margin Targets
* **Cost Per Standard Query (Target):** $0.008  
  *(Breakdown: LLM API $0.005 + Sandbox Compute $0.002 + Network/Storage $0.001)*
* **Cost Per Deep Query (Reflexion / Sonnet):** $0.024
* **Target Blended Gross Margin:** ≥ 78%
* **Payback Period Target:** < 5 months on Pro Tier ($145 CAC against $348 Annual Run Rate).

### 2.6 Go-To-Market (GTM) Strategy
1. **Product-Led Growth (PLG) Viral Loops:** Shared read-only interactive analysis links with "Fork this Analysis" and "Built with Platform" watermarks on exported Plotly visualizations.
2. **Template Playground & Sample Datasets:** Pre-loaded datasets (SaaS Churn, E-commerce Cohorts, Clinical Trial Data, Venture Portfolio Analysis) enabling instant zero-upload evaluation.
3. **Developer & Data Community Engagement:** Publishing deep-dive technical benchmarks comparing LLM code-generation accuracy on messy real-world datasets; open-sourcing evaluation harnesses for agentic code sandboxes.

---

## 3. User Personas & Jobs-to-be-Done (JTBD)

### 3.1 Primary Personas

#### Persona 1: Maya Lin — The Growth & Operations Analyst
* **Demographics:** Age 28; Growth Analyst at a 150-person B2B SaaS startup; proficient in Excel and intermediate SQL; knows basic Python syntax but struggles with complex Pandas indexing, groupby aggregations, and datetime wrangling.
* **Goals:** Deliver weekly cohort retention analyses, marketing attribution models, and ad-hoc campaign performance reports to executive leadership quickly and accurately.
* **Pain Points:** Spends 12 hours a week manually cleaning messy CSV exports from HubSpot, Stripe, and Google Ads; Excel freezes on 300,000-row files; data team takes 2 weeks to prioritize simple SQL queries.
* **Behaviors:** Works under tight deadlines; highly visual; needs exportable charts that match brand aesthetics for slide decks.
* **JTBD Statement:** *“When I receive unformatted, multi-source marketing and revenue exports, I want to upload them and describe my analytical questions in plain English, so that I can generate clean cohort heatmaps and executive summaries in minutes without writing complex Pandas code or crashing Excel.”*

#### Persona 2: Dr. Alex Thorne — Senior Data Scientist
* **Demographics:** Age 35; Senior Data Scientist at a Series B healthtech company; expert in Python, PyTorch, SQL, and statistical modeling.
* **Goals:** Rapidly evaluate new research datasets, inspect feature distributions, identify missingness and multi-collinearity, and generate clean starter notebooks for downstream modeling.
* **Pain Points:** Tired of writing repetitive boilerplate code for exploratory data analysis (EDA), histogram generation, and outlier trimming; irritated by "black-box" AI tools that give answers without showing the underlying code.
* **Behaviors:** Skeptical of AI outputs; insists on inspecting raw code; demands reproducibility and Jupyter notebook exportability.
* **JTBD Statement:** *“When I am exploring an unfamiliar 400MB clinical dataset, I want an autonomous assistant to profile distributions, execute statistical tests, and present verifiable code in an interactive notebook format, so that I can eliminate tedious exploratory boilerplate and jump straight into feature engineering.”*

#### Persona 3: Sarah Sterling — Non-Technical Founder & CEO
* **Demographics:** Age 41; Founder of a direct-to-consumer e-commerce brand; business background; zero coding literacy; comfortable reading business charts.
* **Goals:** Monitor customer acquisition cost (CAC), lifetime value (LTV), repeat purchase velocity, and inventory turnover on demand.
* **Pain Points:** Cannot extract answers from raw database exports without hiring expensive freelance analysts; existing BI dashboards are rigid and do not answer "why" questions when metrics dip.
* **Behaviors:** Asks high-level questions on mobile and desktop; values clarity and direct answers; requires plain-language takeaways alongside charts.
* **JTBD Statement:** *“When our weekly repeat customer rate suddenly drops, I want to drag and drop our Shopify and Klaviyo CSVs and ask why in conversational language, so that I can diagnose the business problem immediately without waiting for an analyst.”*

#### Persona 4: Elena Rostova — VP of Information Security & Compliance
* **Demographics:** Age 46; CISO/Compliance Director at a FinTech enterprise; oversees data governance, SOC2, GDPR, and ISO 27001 compliance.
* **Goals:** Ensure employees do not leak proprietary IP, customer PII, or financial records into third-party AI models; guarantee enterprise network isolation.
* **Pain Points:** Shadow AI usage (employees pasting sensitive CSV data into consumer ChatGPT); lack of audit logs and compliance guarantees in commercial AI tools.
* **Behaviors:** Audits architecture diagrams, SOC2 reports, and data flows; demands strict data residency, encryption at rest/in transit, and zero outbound network access from execution sandboxes.
* **JTBD Statement:** *“When our analytical staff leverages AI to accelerate data workflows, I want mathematical execution to occur in isolated, air-gapped sandboxes with zero LLM data retention, so that our customer data remains completely protected and compliant with privacy regulations.”*

---

## 4. Functional Requirements

### 4.1 Epic Overview & MoSCoW Prioritization
```
┌────────────────────────────────────────────────────────────────────────┐
│                      EPIC ARCHITECTURE & ROADMAP                       │
├───────────────────────────────────────────────────────┬────────────────┤
│ EPIC                                                  │ PRIORITY       │
├───────────────────────────────────────────────────────┼────────────────┤
│ Epic 1: Multi-Format Ingestion & Automated Profiling  │ Must Have (P0) │
│ Epic 2: Conversational Engine & Schema-Only Synthesis │ Must Have (P0) │
│ Epic 3: Stateful Sandbox Execution & Memory Kernel    │ Must Have (P0) │
│ Epic 4: Self-Healing Reflexion Loop                   │ Must Have (P0) │
│ Epic 5: Client-Side Interactive Plotly Visualizations │ Must Have (P0) │
│ Epic 6: Glass-Box Monaco Code Inspection & Export     │ Must Have (P0) │
│ Epic 7: Immutable DataFrame Versioning & Time-Travel  │ Should Have(P1)│
│ Epic 8: Multi-File Relational Merging & Joining       │ Should Have(P1)│
│ Epic 9: Multi-LLM Dynamic Routing Engine              │ Should Have(P1)│
│ Epic 10: Natural Language Report & Dashboard Export   │ Could Have (P2)│
└───────────────────────────────────────────────────────┴────────────────┘
```

### 4.2 Detailed Epics & User Stories

#### Epic 1: Ingestion & Automated Profiling (P0)
* **Story 1.1:** As an analyst, I want to drag and drop files up to 500MB (CSV, XLSX, TSV, JSON, Parquet, SQLite) into the chat window, so that I can immediately begin analyzing them without manual formatting.
  * *Acceptance Criteria:*
    1. System validates file size (≤ 500MB) and performs binary magic-number MIME sniffing.
    2. Upload utilizes chunked multipart uploads directly to S3/Cloudflare R2 with progress bars.
    3. Handles corrupted delimiters, mixed datatypes, and missing headers gracefully with automated fallbacks.
* **Story 1.2:** As a user, I want the system to instantly summarize my uploaded dataset upon ingestion, so that I understand its dimensions, columns, and quality before writing a prompt.
  * *Acceptance Criteria:*
    1. Automatically generates a profile within 2.5 seconds of upload completion.
    2. Displays row count, column count, memory footprint, data types per column, and percentage of null values.
    3. Renders a formatted preview table showing the top 5 rows.

#### Epic 2: Conversational Engine & Schema-Only Synthesis (P0)
* **Story 2.1:** As an analyst, I want to type natural language analytical questions, so that the system generates and runs appropriate Python code to answer me.
  * *Acceptance Criteria:*
    1. System synthesizes a JSON schema representation of the DataFrame (column names, types, value ranges, samples).
    2. Raw data rows are never sent to the LLM; only schema context is injected into the prompt.
    3. The LLM returns a response containing structured natural language explanations and an executable Python code block.

#### Epic 3: Stateful Sandbox Execution & Memory Kernel (P0)
* **Story 3.1:** As an analyst, I want my calculations to persist across conversational turns, so that if I clean a column in Step 1, it remains clean when I calculate correlations in Step 2.
  * *Acceptance Criteria:*
    1. Each user session is bound to an isolated, running IPython kernel.
    2. Modifying the in-memory DataFrame (`df`) persists variables in the kernel's `globals()` dictionary.
    3. Container execution is subject to a strict 60-second execution timeout and 4GB RAM ceiling.
    4. Sandboxes operate with zero outbound internet access (`network: none`).

#### Epic 4: Self-Healing Reflexion Loop (P0)
* **Story 4.1:** As a non-technical user, I want the system to automatically fix syntax errors or runtime exceptions, so that I am not exposed to broken Python code or confusing tracebacks.
  * *Acceptance Criteria:*
    1. If code execution yields a non-zero exit code or Python traceback, the orchestrator captures standard error.
    2. The orchestrator feeds the failing code, error traceback, and schema context back to the LLM in an automated reflection turn.
    3. System attempts up to 3 automatic retries before reporting failure.
    4. Upon successful recovery, the user receives the correct final output with an indicator showing automatic self-correction occurred.

#### Epic 5: Client-Side Interactive Plotly Visualizations (P0)
* **Story 5.1:** As an analyst, I want charts to be fully interactive rather than static images, so that I can zoom, pan, inspect data points, and isolate series.
  * *Acceptance Criteria:*
    1. Generated Python scripts serialize visualizations to Plotly JSON specs (`fig.to_json()`) rather than invoking GUI display methods (`fig.show()`).
    2. Frontend intercepts Plotly JSON payloads and renders them via `react-plotly.js`.
    3. Visualizations support interactive hover tooltips, zoom, pan, box select, and instant export to high-resolution PNG, SVG, and CSV.

#### Epic 6: Glass-Box Code Inspection & Export (P0)
* **Story 6.1:** As a data scientist, I want to inspect the exact Python code generated and executed for every message, so that I can audit calculations and ensure statistical validity.
  * *Acceptance Criteria:*
    1. Every assistant response includes a collapsible "View Code" drawer powered by Monaco Editor with Python syntax highlighting.
    2. Displays exact execution duration (ms), memory delta, and raw standard output/error streams.
    3. Users can copy the Python code snippet with one click.
    4. Users can export the entire conversation history as a reproducible, sequentially ordered Jupyter Notebook (`.ipynb`).

#### Epic 7: Immutable DataFrame Versioning & Time-Travel (P1)
* **Story 7.1:** As an analyst, I want every data-modifying operation to create a restorable checkpoint, so that I can undo mistakes or compare before-and-after results.
  * *Acceptance Criteria:*
    1. Any code snippet mutating `df` triggers an automatic background snapshot to Parquet storage (`df_v0.parquet`, `df_v1.parquet`).
    2. UI displays an interactive timeline of revisions with diff summaries (e.g., *"3 columns dropped, 45 null values imputed"*).
    3. Users can revert to any prior state (`df_vX`) with a single click, instantly rehydrating the IPython memory space.

---

## 5. Non-Functional Requirements (Business Perspective)

```
┌────────────────────────────────────────────────────────────────────────┐
│                      SERVICE LEVEL OBJECTIVES (SLO)                    │
├────────────────────────────┬─────────────────────────────┬─────────────┤
│ METRIC                     │ USER-FACING TARGET          │ SEVERITY    │
├────────────────────────────┼─────────────────────────────┼─────────────┤
│ Sandbox Acquisition Latency│ < 150 ms (from warm pool)   │ Critical    │
│ Time to First Token (TTFT) │ < 800 ms (SSE streaming)    │ High        │
│ End-to-End Simple EDA Run  │ < 3.0 seconds total         │ High        │
│ System Uptime (Monthly)    │ ≥ 99.9% (Pro) / 99.95% (Ent)│ Critical    │
│ Maximum File Ingestion Size│ 500 MB per file             │ High        │
└────────────────────────────┴─────────────────────────────┴─────────────┘
```

### 5.1 Performance Expectations (User POV)
* **Interactive Responsiveness:** Code generation streaming begins in under 800ms. Standard transformations on 1,000,000 rows complete in under 2.5 seconds.
* **Warm Sandbox Acquisition:** Users must never wait for cold-start container provisioning; warm pool allocation must complete in ≤ 150ms.

### 5.2 Availability & Reliability
* **High Availability Target:** 99.9% availability for Pro tiers; 99.95% for Enterprise tiers (excluding planned maintenance windows).
* **Fault Tolerance:** If a sandbox pod crashes due to an out-of-memory (OOM) error, the user session must display a graceful error notification within 1 second and immediately provision a fresh container.

### 5.3 Security, Privacy & Compliance
* **Zero-Network Isolation:** Sandboxes must have all external networking disabled (`network: none`) to prevent SSRF and data exfiltration.
* **Data Privacy:** Raw data rows must never be logged in application logs or transmitted to third-party LLM providers; LLM prompts contain only schema structures.
* **Regulatory Compliance:** Full compliance readiness for GDPR (Articles 15 & 17: Right of Access and Right to Erasure), CCPA, and SOC2 Type II trust principles (Security, Confidentiality, Availability).
* **Data Retention Policies:** Free tier data deleted after 7 days of inactivity; Pro tier retained for 90 days; Enterprise configurable (including zero-retention / purge on session disconnect).

### 5.4 Accessibility (a11y)
* **Standards Compliance:** Full compliance with WCAG 2.1 Level AA.
* **Assistive Tech Support:** Screen-reader accessible tables with ARIA labels; accessible tabular data alternatives for all generated Plotly visualizations; keyboard navigation across all interactive drawers.

---

## 6. User Experience & Design Principles

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CORE SPLIT-PANE UI LAYOUT                       │
├───────────────────────────────────┬────────────────────────────────────┤
│ LEFT: CONVERSATIONAL STREAM (45%) │ RIGHT: DATA & VISUAL WORKSPACE(55%)│
├───────────────────────────────────┼────────────────────────────────────┤
│ • File upload / drop zone         │ • Tabs: [Data Table] [Charts] [EDA]│
│ • Chat history & message cards    │ • Full interactive Plotly canvas   │
│ • Streaming token output          │ • Virtualized 10,000-row preview   │
│ • Collapsible Monaco Code Drawer  │ • Timeline & Checkpoint bar        │
│ • Prompt input + template pills   │ • Export (PNG, SVG, CSV, Notebook) │
└───────────────────────────────────┴────────────────────────────────────┘
```

### 6.1 Design Principles
1. **Glass-Box Transparency:** Never hide the machine. Show users the exact Python code that produced their insights.
2. **Deterministic Confidence:** Visual cues must communicate whether an output was extracted directly from code execution or generated as natural language interpretation.
3. **Zero-Friction Immersion:** Everything happens within a single split-pane interface; users never switch tabs or lose context while examining data and charts.

### 6.2 Key User Journeys

#### Journey 1: Happy Path — From Messy CSV to Executive Visualization
1. **Upload:** User drops `q3_marketing_spend.csv` (140MB) onto the canvas.
2. **Instant Profiling:** Within 1.8s, the right panel displays a schema preview: 12 columns, 450,000 rows, 4.2% missing values in `customer_id`.
3. **Conversational Query:** User types: *"Filter out missing customer IDs, convert transaction_date to datetime, and plot a weekly revenue trend split by acquisition channel."*
4. **Execution & Stream:** The left panel streams the natural language plan; Monaco drawer indicates Python execution (`pandas` + `plotly.express`).
5. **Interactive Visualization:** The right panel renders a multi-line Plotly chart with smooth animations, custom brand palette, and interactive legend toggles.
6. **Code Inspection:** User clicks "View Code", audits the `pd.to_datetime` and `.groupby()` logic, and exports the figure as an SVG for their executive slide deck.

#### Journey 2: Critical Edge Case — Self-Healing Runaway Type Error
1. **Prompt:** User requests: *"Calculate the 90th percentile revenue for each country."*
2. **Failure:** The `revenue` column contains currency strings (e.g., `"$1,250.00"`). Python execution throws `TypeError: can't multiply sequence by non-int of type 'float'`.
3. **Reflexion Loop:** The orchestrator intercepts the stderr traceback, constructs a reflection prompt, and dispatches it to the model.
4. **Correction:** The model recognizes the string formatting, writes code to strip `$` and `,`, casts to `float64`, and re-computes `df.groupby('country')['revenue'].quantile(0.90)`.
5. **Resolution:** The user sees a completed bar chart with a subtle notification badge: *"Resolved column formatting issue automatically."*

---

## 7. Success Metrics & Analytics Framework

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ANALYTICS & KPI HIERARCHY                       │
├────────────────────────────────────────────────────────────────────────┤
│                          NORTH STAR METRIC                             │
│         Weekly High-Confidence Completed Analyses (WHCCA)              │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│ PRODUCT ENGAGEMENT       │ TECHNICAL EXCELLENCE     │ BUSINESS & GROWTH│
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ • Upload-to-Query Conv.  │ • P95 Execution Latency  │ • Trial-to-Paid  │
│   (Target: > 80%)        │   (Target: < 3.5s)       │   (Target: > 8%) │
│ • 3+ Queries / Session   │ • Reflexion Recovery Rate│ • Gross Margin   │
│   (Target: > 65%)        │   (Target: > 82%)        │   (Target: > 75%)│
│ • WAU / MAU Ratio        │ • Sandbox Crash Rate     │ • Net Revenue    │
│   (Target: > 40%)        │   (Target: < 0.1%)       │   Retention >125%│
└──────────────────────────┴──────────────────────────┴──────────────────┘
```

---

## 8. Risks, Assumptions & Open Questions

### 8.1 Business & Market Risks
* **Foundational Model Commoditization:** Risk that OpenAI or Anthropic release direct native competitors within their standard consumer chat apps.  
  * *Mitigation:* Focus aggressively on proprietary workflows: team collaboration, live enterprise data warehouse connectors, deep data versioning, custom Plotly styling, and enterprise VPC compliance guarantees.
* **Inference Cost Volatility:** Risk that high token usage during multi-turn Reflexion loops erodes gross margins.  
  * *Mitigation:* Enforce strict model routing: use lightweight models (Gemini 1.5 Flash / GPT-4o-mini) for schema extraction and basic queries; reserve Claude 3.5 Sonnet for complex modeling and self-correction.

### 8.2 Technical Assumptions
* **Sandbox Bootstrapping:** Assumes warm pool architecture can sustain container assignment latencies under 150ms under peak burst traffic (100 concurrent requests/sec).
* **In-Memory Limits:** Assumes 4GB RAM per container is sufficient for 95% of standard user datasets (≤ 500MB CSVs expand to 1.5GB–2.5GB in uncompressed Pandas memory).

### 8.3 Open Questions
1. Should the platform support real-time user-installed custom pip packages (`!pip install`) in the MVP, or should we restrict execution to a pre-baked manifest of 150 scientific computing libraries?  
   * *Initial Decision:* Pre-bake top 150 scientific packages in MVP to eliminate network access and preserve sub-150ms sandbox assignment.
2. What is the optimal storage strategy for intermediate Parquet checkpoints when users execute 50+ turns on a 400MB dataset?  
   * *Initial Decision:* Implement differential copy-on-write column versioning with automated pruning of unreferenced checkpoint branches after 7 days.

---

## 9. Comprehensive Product Roadmap

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRODUCT ROADMAP TIMELINE                        │
├─────────────────────────┬─────────────────────────┬────────────────────┤
│ Q1: MVP LAUNCH          │ Q2: TEAM COLLABORATION  │ Q3-Q4: ENTERPRISE  │
├─────────────────────────┼─────────────────────────┼────────────────────┤
│ • 500MB File Ingestion  │ • Multi-file joins      │ • Snowflake/BigQuery│
│ • Schema-only prompt    │ • Shared workspace URLs │ • VPC deployment   │
│ • Warm IPython sandbox  │ • Team comment threads  │ • SOC2 Type II     │
│ • Plotly interactive viz│ • Scheduled email alerts│ • Custom PyPI repo │
│ • 3-attempt Reflexion   │ • R language kernel     │ • Autonomous agents│
│ • Parquet time-travel   │ • Custom brand palettes │ • Role-based RBAC  │
└─────────────────────────┴─────────────────────────┴────────────────────┘
```
