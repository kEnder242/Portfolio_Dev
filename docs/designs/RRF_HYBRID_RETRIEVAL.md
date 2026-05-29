# DESIGN: RRF Hybrid Retrieval [ENHANCEMENT]
**Role: [DESIGN] - Retrieval Architecture**
**Status:** PROPOSED (Sprint 31)

## 🎯 OBJECTIVE
Enhance the Lab's historical grounding by combining **Lexical (BM25)** and **Semantic (Vector)** search using **Reciprocal Rank Fusion (RRF)**. This solves the "Acronym Trap" (where vectors miss specific terms like PECISTRESSOR) while maintaining conceptual "Vibe" matching.

---

## 📐 CORE LOGIC: Reciprocal Rank Fusion
RRF merges multiple ranked result sets without requiring score normalization.

**The Formula:**
$$score(d) = \sum_{r \in R} \frac{1}{60 + rank(d, r)}$$

### 1. Lexical Pass (Exact Match)
- **Engine**: BM25 (via `rank_bm25`).
- **Target**: High-fidelity matching for years (2023), acronyms (PECI, MSR), and specific IDs.
- **Contribution**: Provides the "Hard Anchor."

### 2. Semantic Pass (Concept Match)
- **Engine**: ChromaDB (Cosine Similarity).
- **Target**: Conceptual matches (e.g. "early career," "system stress").
- **Contribution**: Provides the "Fuzzy Context."

---

## 🛠️ IMPLEMENTATION PLAN (Sprint 31)

### Phase 1: Indexing
- Update `scan_librarian.py` or `archive_node.py` to maintain a parallel BM25 index of the JSON archive.
- Ensure the index is persistent and reloaded on `AcmeLab` ignition.

### Phase 2: Retrieval Refactor
- Update `ArchiveNode.get_context(query)`:
    1.  Fetch Top-10 Semantic results.
    2.  Fetch Top-10 Lexical results.
    3.  Apply RRF scoring to all unique document IDs.
    4.  Sort and return the top-K merged results.

### Phase 3: Regex Clean-up
- Per **BKM-015 #4**, we *could* keep the year-sticky regex for 100% file-open reliability, but RRF should naturally place the correct year at Rank 1.
- **Decision**: Retain year-regex as a "Fast-Path" shortcut, using RRF for all other technical grounding.

---

## ✅ VERIFICATION
- **Test**: `semantic_probe.py` must correctly identify "PECISTRESSOR" in the top-3 results.
- **Audit**: Deferred Semantic Evaluation (BKM-032) verifies that the resulting context is both factual (lexical) and relevant (semantic).
