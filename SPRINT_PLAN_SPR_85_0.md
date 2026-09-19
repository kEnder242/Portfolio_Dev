# 📋 Sprint Plan: [SPR-85.0] The DNA Synapse Graph, Voice Vector Switcher & Semantic Manuscript

> **Sprint Type:** Core Architectural & UX Evolution  
> **Status:** ACTIVE & HEADS-DOWN  
> **Date:** September 2026  
> **Assigned Lead:** AGY + Sovereign Operator  
> **Applicable Operational Laws:** BKM-004 (QQ Protocol), BKM-020 (Intent Preservation), BKM-024 (Live Validation), BKM-040 (Git Discipline), BKM-049 (Owner Tag Mandate), BKM-060 (Polymorphic DNA Schema), PHL-035 (Invariant Truth & Fluid Projection)

---

## 🧭 Executive Summary & Core Objectives

Sprint 85 builds directly upon the foundations established in Sprint 84 (`[FEAT-594]`, `[FEAT-595]`, `[PHL-035]`), bringing the **Voice Vector Space** and **DNA Connection Web** to full visual and interactive maturity:
1. **`[FEAT-596]` The DNA Forge 2D Connections Web (Neural Synapse View):** Interactive SVG/Canvas force-directed knowledge graph in `dna_forge.html` rendering 1st-degree `explicit_links` and semantic vector cosine distance edges across all 8 polymorphic domains (`PHL`, `WIS`, `FEAT`, `BKM`, `SPRINT`, `DISC`, `RDNA`, `ART`, `RESUME`).
2. **The Voice Vector Space Live Refactoring Switcher:** Real-time UI slider/toggle in `writer.html` enabling authors to rotate a document between *Scientific Manuscript*, *Executive Brief*, and *ATS Recruiter Bullets* by dynamically swapping mutation variants while preserving invariant citations.
3. **Manuscript #2 Compilation ("Semantic Packing & Ideographic DNA"):** Transforming `field_notes/dna_semantic_packing_and_voice_vector_space.md` into structured paper AST (`PAPER-002_SEMANTIC_PACKING.json`) with round-trip Google Docs and publication views.
4. **Deferred Backlog Item ("Ossification" Remodeling Policy):** Automated/human card-fusion policy is explicitly deferred to future exploration per operator direction to ensure pure non-destructive exploration first.

---

## 🗺️ Sprint 85 Story Breakdown & Delegation Matrix

| Story | Title | Owner | Dispatch Mode | Key Deliverables & Target Files |
| :--- | :--- | :---: | :---: | :--- |
| **85.1** | DNA Connections Graph Data Engine (`FEAT-596`) | `[SWARM:CLOUD]` | Cloud Swarm / AGY Fallback | Foyer endpoint `/dna/connections_graph` compiling multi-domain vector neighbors and explicit links into graph JSON. |
| **85.2** | DNA Forge Interactive 2D Synapse View (`FEAT-596`) | `[AGY:PRIMARY]` | Local In-Session | Interactive force-directed SVG/Canvas visualizer in `Portfolio_Dev/field_notes/dna_forge.html` with click-to-center traversal and domain filtering. |
| **85.3** | Live Voice Vector Switcher in `writer.html` | `[AGY:PRIMARY]` | Local In-Session | Interactive multi-axis style slider / presets in `writer.html` dynamically projecting paragraphs across active voice, tense, and register. |
| **85.4** | Manuscript #2 AST Pipeline & Live Doc Exporter | `[AGY:PRIMARY]` | Local In-Session | Compile `PAPER-002_SEMANTIC_PACKING.json` and export to Google Docs and interactive reader. |
| **85.5** | Full Pytest Suite, Site Build & Live Certification (`BKM-024`) | `[AGY:PRIMARY]` | Local In-Session | Pytest verification across all graph & paper endpoints, `build_site.py` execution, and commit. |

---

## 📦 Backlog & Future Items
- **[BACKLOG-085] "Ossification" Remodeling Policy & Drawer:** Human-in-the-loop review drawer in `dna_forge.html` detecting duplicate/overlapping cards ($>0.88$ similarity) and executing 1-click fusion into canonical cards.
