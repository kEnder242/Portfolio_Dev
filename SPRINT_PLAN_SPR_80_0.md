# 🚀 Sprint 80 Plan: The Water-Level DNA Palette & Option C Hybrid Wordsmithing Studio

**Sprint ID:** `SPR_80_0`  
**Focus:** Fluid Human Wordsmithing, Dual-Tier Discard Engine, and Context-Aware Water-Level DNA Palette  
**Target File:** [`Portfolio_Dev/field_notes/writer.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/writer.html)  
**Features Implemented:** **FEAT-587** *(Unified Hybrid Action Gutter & Reversion Engine)*, **FEAT-588** *(Context-Aware Water-Level DNA Palette & Micro-Surface Controller)*  
**Governance:** BKM-004 (QQ Protocol), BKM-006 / BKM-030 (Autonomy Gate), BKM-049 (Owner Tag Mandate), BKM-040 (Virtualenv / Local Git Discipline)

---

## 🎯 Executive Summary & Architectural Vision

Sprint 80 completes the transition of `writer.html` into a distraction-free, professional sovereign wordsmithing environment:
1. **Option C Hybrid Gutter (`FEAT-587`):** Replaces static button clutter with sleek, semi-translucent floating action pills that fade in on hover (`:hover`), allowing immediate access to `[✨ Review Consistency]`, `[🔍 Discover References]`, and `[🛠️ Toolbox]` without interrupting the reading flow.
2. **Dual-Tier Discard Engine (`FEAT-587`):** Adds paragraph-level revert (clears dirty flags, empties pending citations, and rolls back prose draft to disk baseline) and paper-level global rollback (`[↩️ Revert to Disk]`).
3. **Context-Aware Water-Level DNA Palette (`FEAT-588`):** Eliminates cross-screen drag fatigue by binding the right-hand Palette to whichever AST node is selected in the Outliner or Writing View. Citations are surfaced `[+]` or submerged `[✖]` across an interactive horizontal waterline in single-click or micro-drag gestures.

```
  Tree Outliner / Writing Canvas              DNA Palette (Context: PAR-001)
 ┌─────────────────────────────┐             ┌────────────────────────────────────────┐
 │ Section 1                   │             │ 🎯 TARGET CONTEXT: PAR-001             │
 │   PAR-001 [FOCUSED] ──────► │ ──────────► │ 📌 ATTACHED CITATIONS (Above Water)    │
 │   PAR-002                   │             │  [🟣 PHL-001 ✖]  [🟢 BKM-046 ✖]        │
 │                             │             │                                        │
 │ Hover on Paragraph:         │             │ ~ ~ ~ ~ ~ ~ ~ WATER LEVEL ~ ~ ~ ~ ~ ~  │
 │  [✨ Review | ↩️ Discard | 🔍]│             │                                        │
 │  “LLMs are a prefrontal...” │             │ 💡 SUGGESTIONS & DISCOVERIES (Below)   │
 │                             │             │  [+ 🟣 PHL-002] "Hippocampus Model"    │
 └─────────────────────────────┘             └────────────────────────────────────────┘
```

---

## 📋 Story Breakdown & Delegation Matrix (BKM-049)

### **Story 80.1: Writing View Option C Hybrid Gutter & Hover Triggers**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-587**
* **Deliverables:**
  1. Remove static `[🛠️ Toolbox]` buttons from `.paper-title-block`, section headers, and paragraph wrappers.
  2. Implement floating semi-translucent action pills (`.hover-action-pill`) that fade in smoothly on hover (`opacity: 0` $\rightarrow$ `opacity: 1`, `0.15s` ease).
  3. Wire click targets for citation epigraphs (`.manuscript-epigraph`) to open the Citation Inspector.
  4. Wire section header badges and paragraph sequence pills to toggle tier-level toolboxes.

---

### **Story 80.2: Two-Tier Discard & Rollback Engine**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-587**
* **Deliverables:**
  1. **Paragraph Revert (`[↩️ Discard Changes]`):**
     - Add discard trigger to `.hover-action-pill` (visible only when node is `dirty`) and inside the Wordsmithing Review Drawer (`#review-drawer`).
     - Clears `par.dirty = false`, empties `par.pending_citations = []`, reverts wordsmithing textarea to original `par.text`, and restores baseline citations.
  2. **Global Paper Revert (`[↩️ Revert to Disk]`):**
     - Add button in Top Header next to `[💾 Save Paper]`.
     - Re-fetches unmodified JSON via Foyer `/paper/load?file=...`, clearing all in-memory dirty flags and re-rendering all views.

---

### **Story 80.3: Context-Aware Water-Level DNA Palette & Micro-Surface Controller**
* **Assigned Owner:** `[SWARM:CLOUD]` via `delegate.py` on REST `:4097`
* **Feature Anchor:** **FEAT-588**
* **Deliverables:**
  1. **Active Context Binding:** When clicking any node in Tree Outliner or Writing View, set `STATE.activeContext = { tier, id }` and highlight the focused node with `.context-focused`.
  2. **Dual-Zone Palette Layout:**
     - **Above Water Zone (`#palette-attached-zone`):** Displays citations currently attached to the active node with single-click `[✖]` to submerge/detach.
     - **Waterline Divider (`#palette-waterline`):** Styled interactive horizontal separator with live attached vs. suggested counts.
     - **Below Water Zone (`#palette-suggested-zone`):** Displays smart suggestions and filtered search results with single-click `[+]` to surface/attach.
  3. **Micro-Drag Handlers:** Support dragging chips across the waterline (drag up = surface/attach; drag down = submerge/detach).

---

### **Story 80.4: Dynamic Context Switching & ChromaDB Live Discover Binding**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-586** / **FEAT-588**
* **Deliverables:**
  1. Wire Foyer `/paper/discover_citations` to automatically query ChromaDB Port 8001 when a new context node is selected.
  2. Populate Below-Water suggestions with highest-scoring DNA items for that specific paragraph or section prose.
  3. Log context switches and vector query latencies to `#sys-console` in real time.

---

### **Story 80.5: Schema Invariants, LaTeX Sync, and Site Compilation**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-585** – **FEAT-588**
* **Deliverables:**
  1. Verify `Portfolio_Dev/scripts/validate_paper_schema.py` passes 100% on `paper_jitc_intuition.json`.
  2. Run `scripts/build_writer.py` and `field_notes/build_site.py` to confirm zero link drift and complete LaTeX/BibTeX synchronization.
  3. Verify `#sys-console` logs clean startup and 0 JavaScript runtime errors.
