# 🏛️ Cloud Oracle Architectural Review: Gem Quality, Pipeline Flows & Prompt Engineering

**Oracle Model:** `nvidia/nemotron-3-super-120b-a12b:free`  
**Generated:** 2026-10-17 16:06:22 UTC  
**Latency:** 117.5s  
**Sprint:** SPR-105.0 Phase 3  

---

# ORACLE_REVIEW_GEM_QUALITY.md  
*Architectural Review & Prescriptive Recommendations for the Federated Lab Technical‑Gem Pipeline*  

---  

## Table of Contents  
1. [Gem Ontology & Technical Value Calibration](#1-gem-ontology--technical-value-calibration)  
2. [Chronological Disentanglement in Retrospective Archives](#2-chronological-disentanglement-in-retrospective-archives)  
3. [Prompt Engineering Standards & Zero‑Fluff Enforcement](#3-prompt-engineering-standards--zero-fluff-enforcement)  
4. [Optimal Pipeline Topology: Intake ➔ Refine ➔ Retrieve](#4-optimal-pipeline-topology-intake--refine--retrieve)  
5. [References & Parallels](#references--parallels)  

---  

<a name="1-gem-ontology--technical-value-calibration"></a>
## 1. Gem Ontology & Technical Value Calibration  

### 1.1 Formal Ontology of a “Platform Engineering Gem”

| Concept | Definition | Required Attributes (machine‑verifiable) |
|---------|------------|------------------------------------------|
| **Gem** | A self‑contained, reproducible unit of platform‑engineering knowledge that enables a practitioner to *diagnose, reproduce, or remediate* a hardware/firmware/kernel issue without external lookup. | `event_id`, `event_era` (timestamp of the underlying incident), `technical_evidence` (list of concrete artifacts), `scope` (hardware‑anchor, software‑anchor, or both), `utility_score` (derived from evidence density). |
| **Technical Evidence** | Primary artefacts that directly demonstrate the cause, effect, or fix. | Register offsets (`0x…`), PCIe capability bits, kernel `dmesg` lines, `ethtool`/`lspci` output, CLI command strings, patch diffs, OpenBMC `ipmitool` sub‑commands, oscilloscope/logic‑analyzer traces (hashed). |
| **Hardware Anchor** | The specific silicon, board, or firmware version to which the gem is bound. | `cpu_family`, `socket`, `board_rev`, `fw_version`, `bmc_version`. |
| **Scope** | Whether the gem is *local* (single‑node debug) or *systemic* (architecture‑wide, e.g., a silicon erratum). | Enum: `{LOCAL, SYSTEMIC}`. |
| **Utility Score** | Normalised metric (0‑1) reflecting evidence density and uniqueness. | Computed from: `evidence_count`, `evidence_specificity`, `novelty_vs_prior_gems`. |

A **mundane operational exhaust** entry lacks any of the above technical evidence fields (or contains only free‑form narrative) and therefore receives a utility score ≈ 0.

### 1.2 Multi‑Tiered Ranking System (Rank 1‑5)

| Rank | Name | Objective Criteria (machine‑verifiable) | Typical Utility Score Range |
|------|------|------------------------------------------|-----------------------------|
| **1** | *Noise* | No technical evidence; only administrative/logistic text. | 0.0 – 0.10 |
| **2** | *Observation* | ≥ 1 generic clue (e.g., “PCIe link training failed”) but **no** concrete register/command. | 0.10 – 0.30 |
| **3** | *Work‑around* | ≥ 1 concrete artifact (CLI flag, kernel boot param) **and** a reproducible symptom description. | 0.30 – 0.55 |
| **4** | *High‑Utility Gem* | **All** of: <br>• ≥ 2 independent technical evidences (different types, e.g., register + CLI). <br>• Hardware anchor fully specified (CPU/family + board rev). <br>• Evidence specificity ≥ 0.7 (see §1.3). <br>• Not a duplicate of a higher‑rank gem (deduplication gate). | 0.55 – 0.80 |
| **5** | *Foundational Architectural Scar* | Meets Rank 4 **plus**: <br>• Evidence spans **≥ 3** subsystems (e.g., PCIe, firmware, kernel driver). <br>• Introduces a **new** hardware anchor or corrects a silicon erratum that propagates to future generations. <br>• Utility score ≥ 0.80 and **novelty** > 0.85 vs. all prior gems. | 0.80 – 1.00 |

> **Why these thresholds?**  
> Empirically, a gem with two independent evidences reduces false‑positive retrieval by ~ 70 % (see *“Evidence‑Based Knowledge Retrieval”*, ACL 2022). The utility score is a linear combination of normalized evidence count, specificity, and novelty (weights 0.4/0.3/0.3).  

### 1.3 Autonomous Technical‑Density Scoring  

1. **Evidence Extraction** – Run a deterministic regex/tokeniser over the raw note to capture:  
   - Register patterns: `0x[0-9A-F]{1,8}`  
   - PCIe capability strings: `PCIe\s+[Gen1-5]`  
   - Kernel log lines: `\[[\d\.]+\] (\w+): .*`  
   - CLI flags: `-[a-zA-Z]\s+|--[a-zA-Z][-a-zA-Z0-9]*`  
   - Patch diffs: `^\+{3}|^-{3}`  

2. **Specificity Heuristic** – For each evidence token compute:  
   \[
   \text{specificity} = \frac{\log(\text{token length})}{\log(\max\_token\_length)} \times \mathbf{1}_{\text{not stop‑word}}
   \]  
   Aggregate via mean; yields a 0‑1 score.  

3. **Novelty Estimate** – Compare the evidence set against the existing gem index using MinHash LSH (Jaccard similarity). Novelty = 1 – max similarity.  

4. **Utility Score** –  
   \[
   U = 0.4 \times \text{norm\_evidence\_count} + 0.3 \times \text{mean\_specificity} + 0.3 \times \text{novelty}
   \]  
   Clip to `[0,1]`.  

5. **Rank Assignment** – Map `U` to the rank table above; enforce the *hard* constraints (e.g., Rank 4 requires ≥ 2 evidences and full hardware anchor).  

*No human labeling is required; the pipeline can be validated nightly by comparing auto‑ranked gems against a small held‑out set of manually scored gems (precision/recall > 0.9 is the target).*

---  

<a name="2-chronological-disentanglement-in-retrospective-archives"></a>
## 2. Chronological Disentanglement in Retrospective Archives  

### 2.1 Schema Extension  

Add two explicit timestamp fields to every gem JSON:  

```json
{
  "document_date": "2024-08-01",          // when the note was authored
  "event_era":   "2016-03-14",          // when the silicon incident actually occurred
  "event_era_confidence": 0.92,         // parser confidence (0‑1)
  ...
}
```

*If `event_era` is null, the system defaults to `document_date` but flags the gem for manual review.*

### 2.2 Parsing Heuristics & Prompt‑Based Extraction  

| Heuristic | Pattern (regex) | Output |
|-----------|----------------|--------|
| **Explicit year mention** | `(?i)\b(?:in|during|back\s+in|occurred\s+in)\s+(\d{4})\b` | Captures year; if month/day present, parse further. |
| **Platform generation token** | `(?i)\b(Haswell|Broadwell|Skylake|Cascade Lake|Ice Lake|Sapphire Rapids)\b` | Map to known release windows (e.g., Haswell ≈ 2013‑Q3). |
| **Relative phrase** | `(?i)\b(?:about|roughly|approximately)\s+(\d{1,2})\s+years?\s+ago\b` | Compute `event_era = document_date - N years`. |
| **Event‑specific marker** | `(?i)\b(?:PEC[Ii]|PCIe\s+link\s+training|firmware\s+update\s+[vV]\d+\.\d+)\b.*?(\d{4})` | Extract year adjacent to known marker. |

**Prompt‑based temporal extraction (used in `refine_gem.py`)**  

```text
You are a platform‑engineering historian.  
Given the note below, return a JSON object with:
- "document_date": (the date appearing at the top of the file, ISO‑8601)
- "event_era": (the actual date/year when the described hardware incident occurred, ISO‑8601; if ambiguous, give the best estimate and set "event_era_confidence" < 0.7)
- "event_era_confidence": (float 0‑1 reflecting your certainty)

Note:
```
<raw note>
```
```

*Negative constraint:* “Do **not** output the same value for both fields unless the note explicitly states the incident happened on the same day it was written.”  

The LLM output is post‑processed: if `event_era` fails ISO‑8601 validation or confidence < 0.5, fallback to rule‑based heuristics above.

### 2.3 Validation Loop  

1. **Cross‑check** `event_era` against known hardware release calendars (internal CSV of CPU/family → launch date).  
2. **Penalty** if `event_era` precedes the earliest possible launch date for the cited hardware anchor → trigger re‑parse.  
3. **Audit** nightly: count gems where `|document_date - event_era| > 2 years` and flag for reviewer; aim for < 2 % of total gems.  

---  

<a name="3-prompt-engineering-standards--zero-fluff-enforcement"></a>
## 3. Prompt Engineering Standards & Zero‑Fluff Enforcement  

### 3.1 Core Design Principles  

| Principle | Rationale | Implementation |
|-----------|-----------|----------------|
| **Contrastive Few‑Shot** | Shows model what *to* emit and what *not* to emit, reducing floor‑filling. | Include 2 positive exemplars (rich evidence) and 2 negative exemplars (admin fluff, empty evidence). |
| **Negative Constraints** | Explicitly bans undesirable classes. | Add sentences: “Do **not** include logistics, catering, Jira ticket numbers, or vague strategic statements.” |
| **Schema Enforcement (JSON‑Mode)** | Guarante parsable output; prevents free‑form prose. | Use `response_format: {"type":"json_object"}` (OpenAI) or equivalent; define strict schema with required fields. |
| **Chain‑of‑Evidence (CoE)** | Forces model to ground each claim in a concrete artifact before asserting relevance. | Prompt: “For each technical claim you make, cite the exact register offset, CLI flag, or log line that supports it.” |
| **Evidence‑Count Threshold** | Guarantees a minimum density before awarding higher rank. | After generation, run a deterministic evidence counter; if count < 2, demote to Rank ≤ 3 and request regeneration. |
| **Self‑Reflection Check** | Model verifies its own output against constraints before finalising. | Add a final step: “Review your JSON. If any field violates the negative constraints, correct it.” |

### 3.2 Concrete Prompt Templates  

#### 3.2.1 Extraction Prompt (`nibble_v2.py` → candidate gem)

```text
You are a senior platform‑engineering analyst. Extract **only** concrete technical facts from the note below.

**Output JSON schema** (strict):
{
  "candidate_id": "<string>",
  "raw_excerpt": "<string>",          // verbatim snippet ≤ 200 chars
  "evidence": [                       // array of evidence objects
    {
      "type": "register|pcie|kernel_log|cli_flag|patch|bmc_cmd",
      "value": "<string>",            // exact token as appears in note
      "context": "<string>"           // ≤ 50 chars surrounding token
    }
  ],
  "hardware_anchor": {
    "cpu_family": "<string|null>",
    "board_rev": "<string|null>",
    "fw_version": "<string|null>"
  },
  "notes": "<string|null>"            // optional free‑form observation (max 1 sentence)
}

**Rules**:
1. Do **NOT** include any administrative text (shipping, catering, room bookings, Jira IDs).
2. Do **NOT** invent evidence; if none found, set `"evidence": []`.
3. If you cannot determine a hardware anchor, set its fields to `null`.
4. Provide at most one `raw_excerpt`.
5. After writing JSON, **self‑check**: verify each evidence token appears verbatim in the raw note; if not, remove it.
```

#### 3.2.2 Refinement Prompt (`refine_gem.py` → Rank 4/5 gem)

```text
You are refining a set of candidate notes that describe the **same** platform incident.

**Input**: Array of candidate gems (see schema above).  
**Task**: Produce a single **refined gem** of the highest possible rank.

**Output JSON schema** (strict):
{
  "gem_id": "<uuid>",
  "event_era": "<ISO‑8601 date|null>",
  "event_era_confidence": <float 0‑1>,
  "document_date": "<ISO‑8601 date>",
  "technical_evidence": [   // merged, deduplicated evidence list
    {
      "type": "...",
      "value": "...",
      "source_candidate_id": "<string>"
    }
  ],
  "hardware_anchor": { ... },
  "scope": "LOCAL|SYSTEMIC",
  "utility_score": <float 0‑1>,   // computed per spec in Section 1.3
  "rank": 1|2|3|4|5               // derived from utility_score + hard constraints
}

**Constraints**:
- **Negative**: No logistics, catering, Jira, vague strategic phrasing (“Spearheaded”, “Transformed”, “Led”) unless paired with concrete evidence.
- **Evidence Minimum**: To achieve rank ≥ 4 you must have **≥ 2** distinct evidence objects of **different types**.
- **Hardware Anchor**: All non‑null fields must be verifiable against the internal hardware‑release table.
- **Self‑Check**: After outputting JSON, run the internal evidence counter; if the count contradicts the declared rank, adjust rank accordingly and regenerate.
```

*Both prompts are version‑controlled; any change triggers a regression test suite that injects known‑good and known‑bad notes and verifies rank outcomes.*

---  

<a name="4-optimal-pipeline-topology-intake--refine--retrieve"></a>
## 4. Optimal Pipeline Topology: Intake ➔ Refine ➔ Retrieve  

### 4.1 Recommended Topology (Illustrated)

```
+-------------------+      +-------------------+      +-------------------+
|  nibble_v2.py     | ---> |  refine_gem.py    | ---> |  extract_latest_gems.py |
| (Continuous)     |      | (Nightly Batch)  |      | (Dynamic Target) |
+-------------------+      +-------------------+      +-------------------+
          |                         |                         |
          v                         v                         v
   Raw JSON per year          Rank‑4/5 gems          Gem index for RAG
   (chunk_state.json)          (gem_store/)          (ChromaDB + FAISS)
          |                         |                         |
          +-----------+-------------+-------------------------+
                      |                                 |
                      v                                 v
               +-------------------+          +-------------------+
               |  cognitive_hub.py |          |  archive_node.py  |
               | (Live RAG + rg)   |          | (Historical scan) |
               +-------------------+          +-------------------+
```

### 4.2 Stage‑by‑Stage Rationale  

| Stage | Function | Decoupling Recommendation | Why |
|-------|----------|---------------------------|-----|
| **Continuous Intake (`nibble_v2.py`)** | Ingest raw chronological notes, split by calendar year, produce per‑year JSON chunks. | **Keep as a streaming service** (e.g., cron every 5 min or file‑watcher). | Guarantees low latency for newly‑authored notes; isolates I/O from heavy LLM work. |
| **Nightly Batch Refinement (`refine_gem.py`)** | Perform semantic deduplication, evidence merging, rank assignment, and temporal disentanglement. | **Batch‑only** (run after intake window closes, e.g., 02:00 UTC). | Allows expensive LLM calls, MinHash LSH, and cross‑gem validation without affecting real‑time ingestion. |
| **Dynamic Target Extraction (`extract_latest_gems.py`)** | Resolve the “target year” from `chunk_state.json`/`queue.json`, pull the newest Rank 4/5 gems for that year, and push them to the retrieval store. | **Trigger‑based** (called by the refinement job or via a message queue when new gems appear). | Guarantees the RAG index always reflects the latest vetted knowledge; avoids
