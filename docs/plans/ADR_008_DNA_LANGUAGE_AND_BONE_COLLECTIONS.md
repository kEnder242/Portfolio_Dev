# ADR-008: Federated DNA Meta-Language, 1:1 Source Bone Collections, and Round-Trip Projection Architecture

**Status:** APPROVED  
**Date:** 2026-09-22  
**Domain:** `PHL-036` / `BKM-061` / `VIBE-001` / `FEAT-601` - `FEAT-605`  
**Authors:** Jason Allred & Antigravity (Pair Architecture)

---

## 1. Context & Motivation

As agentic workflows, long context windows, and large knowledge bases grow, two competing failure modes emerge:
1. **Agentic Mania / Context Bloat:** Stuffing static context, long system prompts, passive rules, and raw document dumps into the KV cache leads to non-linear model degradation where passive constraints are ignored and tokens are wasted.
2. **Atomization / Loose Bones:** Decomposing documents into purely atomic DNA cards (`WIS`, `PHL`, `FEAT`, `BKM`) destroys the sequential narrative, context, and connective tissue of the original source if there is no structural blueprint to bind them back together.

To solve this, we formalize the **Bone Collection Architecture**: treating **Bones as the 1:1 transitory scratchpad between original sources and the database**, and **DNA as an architectural meta-language** that decouples semantic meaning from presentation.

---

## 2. Core Architectural Model

### 2.1 The 1:1 Source-to-Bone Mapping
Every original source document (e.g. `stories.html`, a Google Doc, an engineering journal, a resume draft) has an authoritative, 1:1 companion **Bone Collection File** (e.g., `stories_bones.json`, `notes_2026_09_22_bones.json`).

```
[Original Source File] (e.g. stories.html / notes.md / Google Doc)
         │
         ▼ (Import & Decompose)
[Bone Collection File (*_bones.json)] ───► 1:1 Companion Scratchpad
         │                                 - Sequence / Spine Order
         │                                 - Local Revisions (R1..Rn)
         │                                 - Recommended Mutations (M1..Mn)
         ▼ (Promote)
[Sovereign Central DNA DB] ──────────────► ChromaDB (:8001) / Portfolio_Dev/dna/*.json
```

- **Bones are the intermediary DB archives:** They track the exact order, local revisions ($R1 \dots Rn$), and proposed model mutations ($M1 \dots Mn$) for that document without modifying or dirtying the raw original source.
- **Decomposition is Importing:** Ingesting a new source creates a new 1:1 `*_bones.json` file and syncs corresponding cards to the central DNA DB.

---

### 2.2 Granularity & Definitions

| Concept | Definition | Scope |
| :--- | :--- | :--- |
| **Original Source** | The raw document (Markdown, HTML, Google Doc, Resume). | External / User |
| **Bone Collection** | 1:1 scratchpad file tracking the sequence and revisions of a source. | Intermediary File |
| **Bone (Atom)** | An atomic semantic idea (a thought, a bullet list, or a logical paragraph). | Local to Collection |
| **DNA Card** | The sovereign, indexed knowledge pearl in ChromaDB / Central DNA. | Global DB |
| **Revision ($R_n$)** | Codified, accepted alternate readings/presentations of the *same idea*. | Certified Ground Truth |
| **Mutation ($M_n$)** | Candidate lens/voice variations proposed by models before certification. | Uncertified Candidate |
| **Spine** | The ordered 1-indexed vertebrae sequence defining narrative flow. | Structural Spine |
| **Lens** | The stylistic/operational transform applied to the words during projection. | Projection Operator |
| **Paper** | The compiled, self-contained Markdown/LaTeX artifact resulting from a projection. | Rendered Artifact |

---

### 2.3 Words-First Prose & Citation Anchor Syntax

Papers are saved as standard, clean Markdown documents containing **natural human prose first**, accompanied by compact **DNA Citation Anchors**. No database connection is required to read, edit, or render a paper.

#### Words-First Prose & Citation Syntax:
```markdown
# Dog Paper

"I walked the dog" [PHL-231] R1 style=Heading

It was a crisp morning with cold fog rolling over the grass. [WIS-102] R1

> "Invert the memory problem: do not stretch the context window, optimize the retrieval index." [PHL-037] M1 lens=Executive style=callout
```

#### Syntax Breakdown:
- **Prose First:** The natural language words exist directly in the markdown stream. Words are never hidden or escaped inside container attributes like `text="..."`.
- **`[ID]` / `[ID:Rn]`:** The DNA card identifier and active certified revision pointer (e.g. `[PHL-231] R1` or `[PHL-231:R1]`).
- **`lens=<name>`:** (Optional) Dynamic lens transform for that specific vertebra.
- **`style=<type>`:** (Optional) Formatting intention (`Heading`, `paragraph`, `bullet`, `callout`, `epigraph`).
- **Standard Markdown Rendering:** Any standard markdown viewer displays the document naturally. The citation tag acts as an inline provenance anchor and lens-switching handle.


---

### 2.4 Multi-Source Composable Papers & Re-Projection

```
[stories_bones.json]         [notes_jitc_bones.json]         [resume_bones.json]
        │                              │                              │
        └──────────────────────┬───────┴──────────────────────────────┘
                               │
                               ▼ (Compose Spine)
                    [Active Composable Paper]
                               │
            ┌──────────────────┴──────────────────┐
            ▼ (Project with Lens: Academic)       ▼ (Re-Project with Lens: Executive STAR)
    [Paper: Academic Whitepaper]          [Paper: Executive Briefing]
```

1. **Multi-Source Composition:** A paper can select bones from across multiple bone collections to assemble a new composite spine.
2. **Re-Projection Invariant:** A paper can be dynamically re-projected through a new Lens (e.g. from "Academic" to "Executive STAR"), preserving the multi-collection spine while updating wording to matching mutations/revisions.

---

## 3. Invariant & Test Specifications

### 3.1 Bi-Directional Round-Trip Consistency Invariant
$$\Delta\left(\text{Original Source},\; \text{Reconstruct}\big(\text{Bone Collection},\; R_1\big)\right) = 0$$

- **Test Suite:** `HomeLabAI/src/tests/test_dna_roundtrip_consistency.py`
- **Validation Mandate:** 
  1. Ingest a multi-paragraph source text.
  2. Emit the 1:1 `*_bones.json` and DNA cards with $R1 = \text{verbatim origin}$.
  3. Reconstruct the document from the bone collection using $R1$.
  4. Assert exact character-for-character equality with the input source.
  5. Apply an LLM grading pass to verify that any higher revision ($R2 \dots Rn$) preserves semantic fidelity with the underlying DNA card.

---

## 4. Consequences & Benefits

- **Zero DB Lockout:** Papers remain standard Markdown files, completely readable by humans, linters, and external tools without requiring ChromaDB.
- **Immutable Provenance:** Original sources are never dirty-written or mutated without explicit author consent; all variations live in the 1:1 bone scratchpad.
- **Extreme KV Compression:** Agent sessions can load lightweight bone skeletons (`[DNA-xxx:Rn]`) instead of thousands of repetitive tokens, eliminating agent manic behavior.
