# Graph Report - Conversational_Data  (2026-09-19)

## Corpus Check
- 7 files · ~10,656 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 129 nodes · 122 edges · 14 communities (11 shown, 3 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- SYSTEM ARCHITECTURE & DESIGN DOCUMENT
- TECHNICAL REQUIREMENTS DOCUMENT (TRD)
- Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)
- PRODUCT REQUIREMENTS DOCUMENT (PRD)
- 4.2 Detailed Epics & User Stories
- 14. Architecture Decision Records (ADRs)
- 2. Product Vision & Strategy
- 2. Functional Technical Requirements
- 1. Executive Summary
- 3.1 Primary Personas
- 6.2 Key User Journeys
- rules/graphify.md
- workflows/graphify.md
- SYSTEM_DESIGN.md

## God Nodes (most connected - your core abstractions)
1. `SYSTEM ARCHITECTURE & DESIGN DOCUMENT` - 15 edges
2. `PRODUCT REQUIREMENTS DOCUMENT (PRD)` - 10 edges
3. `14. Architecture Decision Records (ADRs)` - 9 edges
4. `4.2 Detailed Epics & User Stories` - 8 edges
5. `TECHNICAL REQUIREMENTS DOCUMENT (TRD)` - 8 edges
6. `1. Executive Summary` - 7 edges
7. `2. Product Vision & Strategy` - 7 edges
8. `Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)` - 6 edges
9. `3.1 Primary Personas` - 5 edges
10. `5. Non-Functional Requirements (Business Perspective)` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (14 total, 3 thin omitted)

### Community 0 - "SYSTEM ARCHITECTURE & DESIGN DOCUMENT"
Cohesion: 0.08
Nodes (25): 10.1 Predictive Warm-Pool Algorithm, 10.2 Pool State Machine, 10. Scalability & Pool Management Architecture, 11. Disaster Recovery & Business Continuity, 12. Technology Stack Evaluation Matrix, 13. System Evolution Path, 1.1 Architectural Vision, 1.2 Guiding Architectural Principles (+17 more)

### Community 1 - "TECHNICAL REQUIREMENTS DOCUMENT (TRD)"
Cohesion: 0.12
Nodes (16): 1.1 High-Level Technical Goals, 1.2 Key Technical Constraints & Non-Negotiables, 1.3 Technology Philosophy & Engineering Principles, 1. Technical Overview, 3.1 Latency Budgets & Throughput Targets, 3.2 Scalability Targets, 3.3 Security & Threat Modeling (STRIDE Analysis), 3.4 Observability & Telemetry Standards (+8 more)

### Community 2 - "Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)"
Cohesion: 0.14
Nodes (13): 1.1 Executive Summary & Core Value Proposition, 1.2 Target User Personas, 1.3 Key Features & Acceptance Criteria, 1. Product Requirements Document (PRD), 2. Technical Architecture & Component Flow, 3.1 Recommended Tech Stack, 3.2 Sandbox Execution Strategy (The Stateful Engine), 3. Technical Requirements Document (TRD) (+5 more)

### Community 3 - "PRODUCT REQUIREMENTS DOCUMENT (PRD)"
Cohesion: 0.15
Nodes (12): 5.1 Performance Expectations (User POV), 5.2 Availability & Reliability, 5.3 Security, Privacy & Compliance, 5.4 Accessibility (a11y), 5. Non-Functional Requirements (Business Perspective), 7. Success Metrics & Analytics Framework, 8.1 Business & Market Risks, 8.2 Technical Assumptions (+4 more)

### Community 4 - "4.2 Detailed Epics & User Stories"
Cohesion: 0.20
Nodes (10): 4.1 Epic Overview & MoSCoW Prioritization, 4.2 Detailed Epics & User Stories, 4. Functional Requirements, Epic 1: Ingestion & Automated Profiling (P0), Epic 2: Conversational Engine & Schema-Only Synthesis (P0), Epic 3: Stateful Sandbox Execution & Memory Kernel (P0), Epic 4: Self-Healing Reflexion Loop (P0), Epic 5: Client-Side Interactive Plotly Visualizations (P0) (+2 more)

### Community 5 - "14. Architecture Decision Records (ADRs)"
Cohesion: 0.22
Nodes (9): 14. Architecture Decision Records (ADRs), ADR-001: Selection of gVisor (`runsc`) for Sandbox Container Virtualization, ADR-002: Schema-Only Context Injection Strategy, ADR-003: Declarative Client-Side Plotly Serialization, ADR-004: Parquet-Based Checkpointing for Immutable State Versioning, ADR-005: Stateful IPython Kernel Architecture Over Stateless Execution, ADR-006: Asynchronous Server-Sent Events (SSE) Over WebSockets for Output Streaming, ADR-007: Multi-Tier Reflexion Loop with AST Pre-Validation (+1 more)

### Community 6 - "2. Product Vision & Strategy"
Cohesion: 0.25
Nodes (8): 2.1 Long-Term Product Vision (3–5 Years), 2.2 North-Star Metric, 2.3 Positioning Statement, 2.4 Competitive Landscape & Differentiation Matrix, 2.5 Monetization & Business Model, 2.6 Go-To-Market (GTM) Strategy, 2. Product Vision & Strategy, Unit Economics & Margin Targets

### Community 7 - "2. Functional Technical Requirements"
Cohesion: 0.25
Nodes (8): 2.1.1 REST Endpoints Specification, 2.1.2 Real-Time Event Stream (Server-Sent Events), 2.1 API Contracts & Interaction Protocols, 2.2 Domain Data Models & Database Schemas, 2.3 Business Logic & Edge Cases, 2. Functional Technical Requirements, PostgreSQL 16 Relational DDL, Pydantic v2 Core Domain Schemas

### Community 8 - "1. Executive Summary"
Cohesion: 0.29
Nodes (7): 1.1 One-Paragraph Vision, 1.2 Problem Statement, 1.3 Solution Overview, 1.4 Target Users & Market Segments, 1.5 Key Value Propositions, 1.6 High-Level Business & Operational Metrics, 1. Executive Summary

### Community 9 - "3.1 Primary Personas"
Cohesion: 0.33
Nodes (6): 3.1 Primary Personas, 3. User Personas & Jobs-to-be-Done (JTBD), Persona 1: Maya Lin — The Growth & Operations Analyst, Persona 2: Dr. Alex Thorne — Senior Data Scientist, Persona 3: Sarah Sterling — Non-Technical Founder & CEO, Persona 4: Elena Rostova — VP of Information Security & Compliance

### Community 10 - "6.2 Key User Journeys"
Cohesion: 0.40
Nodes (5): 6.1 Design Principles, 6.2 Key User Journeys, 6. User Experience & Design Principles, Journey 1: Happy Path — From Messy CSV to Executive Visualization, Journey 2: Critical Edge Case — Self-Healing Runaway Type Error

## Knowledge Gaps
- **89 isolated node(s):** `graphify`, `Workflow: graphify`, `1.1 One-Paragraph Vision`, `1.2 Problem Statement`, `1.3 Solution Overview` (+84 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 96 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PRODUCT REQUIREMENTS DOCUMENT (PRD)` connect `PRODUCT REQUIREMENTS DOCUMENT (PRD)` to `4.2 Detailed Epics & User Stories`, `2. Product Vision & Strategy`, `1. Executive Summary`, `3.1 Primary Personas`, `6.2 Key User Journeys`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Why does `SYSTEM ARCHITECTURE & DESIGN DOCUMENT` connect `SYSTEM ARCHITECTURE & DESIGN DOCUMENT` to `14. Architecture Decision Records (ADRs)`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `4. Functional Requirements` connect `4.2 Detailed Epics & User Stories` to `PRODUCT REQUIREMENTS DOCUMENT (PRD)`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **What connects `graphify`, `Workflow: graphify`, `1.1 One-Paragraph Vision` to the rest of the system?**
  _89 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SYSTEM ARCHITECTURE & DESIGN DOCUMENT` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._
- **Should `TECHNICAL REQUIREMENTS DOCUMENT (TRD)` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `Project Blueprint: Conversational Data Analysis Platform (Julius AI Clone)` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._