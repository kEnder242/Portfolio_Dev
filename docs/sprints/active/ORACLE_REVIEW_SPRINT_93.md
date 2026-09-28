# Cloud Oracle Review: Sprint 93.4 — Chained Projections & Dynamic Lens Crafting

**Role:** Advisory synthesizer (read-only, zero file edits) · **Date:** 2026-09-28
**Story:** 93.4 `[SWARM:CLOUD]` · **Edit target:** `docs/sprints/active/ORACLE_REVIEW_SPRINT_93.md`
**Primary evidence:** `HomeLabAI/src/curator/lens_service.py` (432 L), `Portfolio_Dev/scripts/publish_paper.py` (649 L), `Portfolio_Dev/field_notes/writer.html` (19k+ L), `Portfolio_Dev/field_notes/data/dna_manifest.json`, `FeatureTracker.md` (3370 L)

---

## 0. Executive Verdict

**The four-anchor spec is correct in intent and premature in premise.** Three of its four anchors describe capabilities that do not exist in the code today:

| Anchor | Story-card claim | Code reality | Δ |
|---|---|---|---|
| 1. Dynamic Lens Crafting | "prompt-rubric driven" | `craft_lens()` **ignores its input entirely** — `content` is truncated to a 300-char `raw_source_snippet` and six hardcoded recruiter rules are emitted regardless | **0% implemented** |
| 2. DNA cards as lenses | PHL / VIBE / BKM as lenses | `vibe` and `inspiration` keys **are absent from `dna_manifest.json`**; `load_dna_index()` iterates both and silently yields nothing. VIBE lenses are **unresolvable today** | **blocked on data** |
| 3. Chained-projection invariants | $P = f(B_{\text{canonical}}, L_{\text{local}}, L_{\text{global}})$ | The 3 "views" are **deterministic string templates** over one AST (`publish_paper.py:86–164`) — no LLM, no chain, no decay to design against | **no empirical signal** |
| 4. Lens/Rubric JSON schema | — | `rules` and `rubric_rules` are **the same list under two keys** (`lens_service.py:137–138`); `grade_paper` writes `PAPER-RESUME_v2_*.json` **regardless of `paper_id`** | **ambiguous / buggy** |

**Headline architectural correction (§3.1):** the formula printed in Story 93.4 is **not a chain**. $f(B_{\text{canonical}}, L_{\text{local}}, L_{\text{global}})$ is a **diamond** — both lenses read the *same* canonical bone set. The term "Chained Projections" and the math in its own scope block contradict each other. This is not pedantry: the schema, the error model, and the correct drift metric are **all different** under the two readings. I recommend the diamond and recommend renaming the feature accordingly.

---

## 1. THEMATIC CLUSTERING & RECURRING AXIOMS

Verbatim origin quotes preserved unaltered. These are the load-bearing bedrock statements already in the DNA; the specification below is derived from them rather than invented alongside them.

### Cluster A — Invariance vs. Fluidity (the founding axiom)
> *"Truth is invariant; Presentation is a fluid projection. Triage space converges inward to classify intent; Expression space diverges outward to project invariant DNA meaning into diverse stylistic registers."* — **`PHL-035`** (`writer.html:3134`)

> *"Eliminates hallucination risks by treating underlying technical truth as a fixed immutable coordinate and stylistic tone as a rotation in vector space."* — **`FEAT-598`** rationale

> *"Allows one master knowledge base to generate infinite tailored document projections on demand."* — **`FEAT-603`** rationale

**Axiom A1 (Additive Projection).** A projection may add, reorder, and re-register text. It may not subtract, alter, or invent claims.
**Axiom A2 (Rotation without Translation).** Stylistic change is a *rotation* in a fiber, not a translation of the payload.
**Axiom A3 (Infinite ≠ Uniform.**) "Infinite tailored projections" is a claim about *cardinality of the projection set*, not about the diversity of its members. Untested, and currently false — see §2.6 (CP-6).

### Cluster B — Decoupled Artifact & Provenance (`FEAT-601`, `FEAT-602`, `BKM-055`, `FEAT-604`)
> *"Guarantees absolute data integrity and prevents lossy decomposition drift."* — **`FEAT-604`** rationale, over $\Delta(\text{Original Source}, \text{Reconstruct}(\text{Bone Collection}, R_1)) = 0$

**Axiom B1 (Round-Trip Zero-Loss).** $B$ is losslessly reconstructible from $\Omega$ + certified revisions. Provenance is a *Merkle inclusion proof*, not a citation string.
**Axiom B2 (Revisions vs. Mutations).** `R_n` = human-certified ground truth; `M_n` = unvetted machine proposal. **A projection may read `R`; it may only ever emit `M`.** This is already the governance model in `FEAT-598` and it is the correct backbone for lens output — but **nothing in the current pipeline enforces it** (§2.3).

### Cluster C — The Rubric as Compilation Target (`FEAT-594`, `FEAT-585`)
> *"Bridges high-level editorial and recruiting rubrics with surgical paragraph-level writing, enabling automated tailoring for specific job requisitions."* — **`FEAT-594`** rationale

**Axiom C1 (Rubrics are compiled artifacts).** Guidance → rubric is *program synthesis*, and therefore has a total-function obligation and a coverage postcondition (§3.3).
**Axiom C2 (Schema before substance).** `FEAT-585` already establishes the lab's precedent: machine-verifiable invariant validators gate manuscript mutation. Lens schemas belong in the same validator, not in the UI.

### Cluster D — Register as an Orthogonal Axis (`FEAT-596`, `FEAT-617`)
> *"Provides visual topological navigation across fragmented lab wisdom and features while decoupling underlying semantic meaning from presentation voice."* — **`FEAT-596`** rationale
> *"Unifies document stylistic rotation into a single coherent interface, separating invariant truth from stylistic projection (`PHL-035`)."* — **`FEAT-617`** rationale

**Axiom D1 (Structure ⊥ Register).** Rubric acts on the structural axis; voice acts on the register axis; they are claimed orthogonal. **This claim is currently unstated as a testable property and therefore untested** — see CP-8, which is my single recommended acceptance test for Story 93.5.

### Cluster E — Human Friction as Highest-Fidelity Signal (`BKM-035`, `BKM-032`, `BKM-064`)
> *"Autonomous agents degrade into self-reinforcing hallucination loops when isolated from human correction. The Sovereign Human-in-the-Loop architecture treats human friction, disagreement, and explicit feedback not as execution failures, but as the highest-fidelity evolutionary signal in the system."* — **`PHL-036`** (`writer.html:3062`)

**Axiom E1 (Rubrics need a preference oracle).** A rubric that only emits defect flags is a *detector*, not an *objective*. Without a paired preference signal there is no way to compare two lenses, and therefore no way to validate the rubric compiler (C1). **The missing artifact is a preference ledger** — the lab already has three instances of this pattern (`data/paper_decisions.json`, `delegation_ledger.jsonl`, BKM-064 conversational ledger). The fourth is not in this story card.

---

## 2. MATHEMATICAL INVARIANTS FOR PROJECTION CHAINS

### 2.1 Formalization

Let $\Omega$ be the immutable raw origin corpus and $\mathcal{C}$ the certified bone set (FEAT-601). Define the **anchor projection** $\pi$ as a map from surface text to an invariant claim skeleton:

$$\pi : \mathcal{T} \longrightarrow \Sigma, \qquad \pi(t) = \bigl\{(c_i,\ \text{cites}(c_i),\ \text{metrics}(c_i))\bigr\}_{i=1}^{n}$$

where each claim $c_i$ carries its citation set and its **numeric literals**. This is the formal content of `PHL-035` ("truth is invariant") and `FEAT-598` ("fixed immutable coordinate").

A **lens** is $L = (R, v, \Pi)$ — rubric, voice vector, render policy — acting as a parameterized operator:

$$F_L : \mathcal{T} \times \Theta \to \mathcal{T}, \qquad F_L(t; \theta)$$

### 2.2 CP-1 — Semantic Closure *(the anti-decay invariant)*

> **For every lens $L$ and every parameter setting $\theta$: $\;\pi \circ F_L = \pi$.**

Consequence, by induction on chain depth $k$:

$$\pi\bigl(F_{L_k} \circ \cdots \circ F_{L_1}(\mathcal{C})\bigr) = \pi(\mathcal{C}) \qquad \forall k \ge 1$$

**Why this is the right primitive.** Each $F_L$ is a *retraction* onto the invariant submanifold $\Sigma$; a composition of retractions onto the same submanifold is again a retraction. Equivalently, in categorical terms, $\pi$ is a **retraction** and every $F_L$ is a **fiber-preserving morphism** — a map internal to a fiber of $\pi$. The entire stylistic apparatus lives *inside* a fiber and provably cannot escape it.

**This converts "serial generative decay" from a vibe into a provable defect class:**

$$\text{Decay} \;\equiv\; \exists\, L,\theta: \ \pi(F_L(\mathcal{C})) \neq \pi(\mathcal{C})$$

A single executable test per lens. No drift heuristic, no embedding threshold, no human read required.

### 2.3 CP-2 — Local Commutativity & Chain Canonicalization

$$\bigl[F_{L_i}, F_{L_j}\bigr] = 0 \quad \text{iff} \quad \operatorname{supp}(L_i) \cap \operatorname{supp}(L_j) = \emptyset$$

Local lenses over disjoint bone sets **commute**, which is precisely what licenses the factorized form $P = f(\mathcal{C}, L_{\text{global}}, \{L_{\text{local},i}\})$.

**Global ∘ local does not commute.** Therefore a "chain" is a **DAG over bone sets**, not a linear sequence. Two required consequences:

1. **The schema must express a stack, not a string.** See `lens.stack` in §5.
2. **Non-determinism is itself a decay vector.** A lens DAG with a non-canonical evaluation order will produce irreproducible publications from identical inputs. The implementation must **topologically sort** the stack and record the resulting order in the provenance stamp. Un-canonicalized order is a bug, not a performance detail.

### 2.4 CP-3 — Contractivity on the Stylistic Fiber

Let $N(\pi) = \ker \pi$ be the stylistic fiber. Decay is a *stochastic compounding* phenomenon, so the correct frame is Banach/Picard:

$$B_{k+1} = F(B_k), \qquad \text{converges} \iff F \text{ is a contraction}$$

$$\bigl\lVert \Delta F_L \big|_{N(\pi)} \bigr\rVert \le \rho < 1$$

Serially, a stochastic chain accumulates $\varepsilon_k = \sum_i \lambda^{k-i}\eta_i$ — errors **add**, and $\lambda \ge 1$ diverges. **Design Law D-1 below collapses this to a maximum instead of a sum.**

**Empirical convergence test (cheap, run in CI):** evaluate $\lVert F^2(\mathcal{C}) - F(\mathcal{C}) \rVert$ over a fixed corpus. If it does not shrink, the chain is not iterating — it is drifting, and you have your repro.

### 2.5 Design Law D-1 — **Re-anchor, do not re-generate**

> **Every step must take the certified payload $\pi(\mathcal{C})$ as input — never the previous step's surface text.**

This is the highest-value correction in this report. Under D-1 the topology is a **diamond** (fan-out / fan-in), and the error model becomes:

$$\varepsilon_{\text{chain}} = \textstyle\sum_i \lambda^{k-i}\eta_i \quad\longrightarrow\quad \varepsilon_{\text{diamond}} = \max_i \lambda_i\eta_i$$

Error becomes **bounded by the worst single step** rather than growing with depth. Semantic accumulation becomes *structurally impossible*; only stylistic parameters accumulate, and those are explicitly reconciled at fan-in by a declared merge operator $M$ (§5.3).

**Note the plan already implies this.** Its own formula feeds both lenses from $B_{\text{canonical}}$. The word "chain" is what is wrong. **Recommendation: rename to "Composable Projections" (a term already used by `FEAT-603`) and reserve "chained" for the genuinely serial case, which should carry an explicit depth cap.**

### 2.6 The Full Invariant Set

| ID | Name | Statement | Enforcement | Symbolic? |
|---|---|---|---|---|
| **CP-1** | Semantic Closure | $\pi\circ F_L = \pi$ | claim/citation/metric-set equality vs. $\pi(\mathcal C)$ | ✅ pure |
| **CP-2** | Local Commutativity | $[F_{L_i},F_{L_j}]=0$ on disjoint support; global-local unordered | diff of two evaluation orders | ✅ pure |
| **CP-3** | Fiber Contractivity | $\lVert \Delta F_L\vert_{N(\pi)}\rVert \le \rho<1$ | $\lVert F^2 - F\rVert$ shrinkage | ⚪ hybrid |
| **CP-4** | Non-Erosion | $\forall b\in\mathcal C$: $b$ in $P$ **or** explicitly elided | bone-ID coverage ratio | ✅ pure |
| **CP-5** | Provenance Surjectivity + Metric Integrity | $\tau$ total on $\text{claims}(P)$; **injective on numeric literals** | numeric-literal set diff vs. origin spans | ✅ pure |
| **CP-6** | Diversity Floor | $\min_{L\neq L'} d(F_L, F_{L'}) \ge \tau_{\min}$ | embedding distance | ❌ semantic |
| **CP-7** | Re-projection Idempotence | $F_L(F_L(\mathcal C)) = F_L(\mathcal C)$ | provenance-stamp short-circuit | ✅ pure |
| **CP-8** | Structure ⊥ Register | $[\sigma_R, \rho_v]\vert_{N(\pi)} = 0$ | apply (lens→voice) vs (voice→lens), diff | ✅ pure |

**Critical allocation rule (drives §5):** CP-1, CP-4, CP-5, CP-7 are **hard invariants** and must be enforced by **symbolic detectors only**. A semantic (LLM-judge) detector makes truth-preservation *probabilistic*, which dissolves the entire point of `PHL-035`. CP-6 is the only invariant that legitimately requires a semantic detector — because measuring stylistic diversity is not a truth claim.

> **CP-5 deserves emphasis.** Numeric literals are the highest-value and highest-hallucination-risk content in a resume or whitepaper. Enforce with a literal-set diff against origin spans, and make the diff **fatal**, not a review flag. This is cheap, deterministic, and catches the failure that actually embarrasses.

### 2.7 Why the Current Drift Metric Must Be Retired

`publish_paper.py:47–75` computes:

```
drift_score = 100.0 - (citation_anchors_present_in_view / total_anchors) × 100
```

**Four independent defects:**

1. **It is a substring-presence proxy, not a semantic measure.** It cannot distinguish "this claim survived" from "this ID was mentioned in passing."
2. **It is circular.** It measures the concatenated *pre-HTML view string generated by the same function* — including the citation pills that function itself emitted.
3. **It is one-sided.** High coverage is necessary but not sufficient: a projection can preserve every anchor while inverting their meaning.
4. **It has no denominator for the chain.** Nothing measures whether step $k$ is further from $\mathcal C$ than step $k{-}1$.

**Replacement — rubric-relative bisimulation.** Define observational equivalence *under the active rubric set* $\mathcal R$:

$$P \equiv Q \iff \forall r \in \mathcal R:\ \llbracket r \rrbracket(P) = \llbracket r \rrbracket(Q)$$

and report a **drift vector**, not a scalar:

$$\Delta_{\text{rubric}}(P) = \bigl(\,|\{r : \llbracket r\rrbracket(P) \neq \llbracket r\rrbracket(\mathcal C)\}|\,/\,|\mathcal R|\,\bigr)$$

This is a *defect rate against a declared rubric* — interpretable, actionable, and directly wired to `/paper/grade_paper`. The scalar badge in the UI should be a rollup of this vector, not the substring heuristic.

---

## 3. THE FOUR ANCHORS

### 3.1 Anchor 3 first: the topology contradiction (read this before designing anything)

| Reading | Topology | Error growth | Correct metric | Recommendation |
|---|---|---|---|---|
| "Chained" (serial $L_1 \to L_2 \to \cdots$) | linear | $\sum$ (compounding) | step-wise divergence | ✗ Reject |
| $f(\mathcal C, L_\text{local}, L_\text{global})$ as written | **diamond** | $\max$ (bounded) | CP-1 / CP-5 / CP-6 | ✓ Adopt |

Everything below assumes the **diamond**. Stack evaluation under D-1:

$$P = M\Bigl(\sigma_{R_{\text{global}}}\bigl(\rho_{v_{\text{global}}}(\sigma_{R_{\text{local}}}(\rho_{v_{\text{local}}}(\pi(\mathcal C))))\bigr)\Bigr)$$

with $M$ the declared merge operator.

### 3.2 Anchor 1 — Dynamic Lens Crafting (totalizing the compiler)

The current defect, verbatim from `lens_service.py:67–139`: `content` is written to `raw_source_snippet` at line 136 and **never referenced again**. Lines 77–120 emit the same six rules unconditionally. **Crafting a lens from a Stanford JD and from a haiku yields byte-identical rubrics.**

The fix is to state the compiler as a **total function with a refusal branch**:

$$\operatorname{craft}(g) = \begin{cases} R & \text{if}\ \bigl(\forall r\in R:\ \mathrm{bound}(r)\bigr) \ \wedge\ \operatorname{cov}(R,g)\ \ge\ \tau_{\text{cov}} \\[4pt] \bot & \text{otherwise (emit \texttt{UNSAFE\_TO\_CRAFT})} \end{cases}$$

with source coverage

$$\operatorname{cov}(R,g) = \frac{\bigl|\{\,s \in \operatorname{sent}(g) \mid \exists r\in R:\ r \text{ binds } s \,\}\bigr|}{\bigl|\operatorname{sent}(g)\bigr|}$$

**Requirements this generates (each maps to a real code change):**

1. **Postcondition gate.** `all(r.detector is not None for r in R)` and `len(R) >= 1`, checked before the file is written. `craft_lens` currently performs *no* validation of `rules` from `criteria` (line 121–122 extends the list with arbitrary caller dicts, unvalidated).
2. **Refusal must be loud.** A `DEFAULT_RECORDER_RUBRIC` may only be emitted when `content` is genuinely empty; otherwise emit `UNSAFE_TO_CRAFT` and surface it in the Lens Studio UI.
3. **Coverage is auditable.** Store `provenance.source_coverage` so a human can see *how much of the source the rubric actually binds*. This is the metric that would have caught the stub immediately.
4. **Kill the duplicate key.** `rules` and `rubric_rules` (lines 137–138) are the same object. Pick one; the v2 schema (§5) deprecates `rubric_rules` with a read-alias.
5. **Separate structure from register at compile time.** A compiled rubric sets $\sigma_R$ only. It must not emit voice axes — otherwise CP-8 is violated at the source and no amount of UI discipline will fix it.

### 3.3 Anchor 1 (cont.) — The detector taxonomy is the whole architecture

$$\mathrm{Det} = \mathrm{Sym} \sqcup \mathrm{Sem}, \qquad \mathrm{Sym} = \{\text{regex, AST, set-diff, numeric-literal, citation-presence}\},\ \mathrm{Sem} = \{\text{LLM-judge}\}$$

Every rule carries its detector mode. Two consequences the sprint card does not budget:

- **Cost is not uniform.** Today `grade_paper` is *entirely symbolic* — pure string ops and one regex, **zero LLM calls**, sub-millisecond. Add one semantic detector and it becomes $O(|\mathcal R| \times |\text{bones}|)$ LLM calls: from ~0 ms to minutes on a 2080 Ti / Llama-3.2-3B-AWQ. **This is a three-orders-of-magnitude regression.**
- **⚠️ Feasibility conflict with Story 93.5.** 93.5 specifies a *"Real-Time Synthesis Preview Panel."* A semantic judge in that loop is architecturally infeasible on local silicon. **Recommendation: 93.5's preview must be symbolic-only and debounced, with semantic grading deferred to an explicit async pass.** As written, 93.4's specification and 93.5's requirement are mutually unsatisfiable.

### 3.4 Anchor 2 — DNA cards as lenses

**This anchor is currently blocked, and the block is a data-layer defect, not a code change.**

```
dna_manifest.json keys: [wisdom, philosophy, feature, behavioral, sprint, discovery, rdna, resume, papers]
has 'vibe': False    has 'inspiration': False
```

`load_dna_index()` (`publish_paper.py:29`) iterates `["wisdom","philosophy","inspiration","behavioral","feature","discovery","vibe"]`. The last two contribute **nothing, silently**. Story 93.4 names **VIBE as a first-class lens domain** (`FEAT-605` / `vibe_data.json` / ChromaDB `vibe_dna` all exist) — but no manifest bridge writes them into `dna_manifest.json`. **Prerequisite story required before 93.4 can be honestly scoped.**

**Second, sharper defect:**

```
wisdom bucket: 33 cards, ids = PHL-001 … PHL-035, titles = 0/33 non-empty
philosophy bucket: 33 cards, identical ids
```

The `wisdom` collection is a **verbatim duplicate of `philosophy` carrying PHL-* ids**. This is a **BKM-060 horizontal re-bucketing violation** — the taxonomy mandate explicitly exists to prevent exactly this. Two consequences:

1. **There is no free `WIS-xxx` namespace.** `WIS-012` is already referenced in `expand_citations` (`lens_service.py:390`). Any WIS mapping in this report is a *proposal contingent on re-bucketing first*.
2. **All 66 PHL cards have empty `title` fields** in the manifest. A lens built from `PHL-035` will render a lens dropdown entry with no label. Any DNA-lens feature must source titles from the upstream domain files (`dna/vibe_data.json`, Protocols.md, FeatureTracker.md), not the manifest.

**Third defect — the ID space is not a single namespace.** `FEAT-582` and `FEAT-585` each appear **twice** in the manifest with different titles (cross-domain re-bucketing without renaming), alongside `LAB-xxx` ids inside the `feature` bucket. A `dna_card` lens must therefore resolve by `(domain, id)`, never by `id` alone. The v2 schema enforces this.

### 3.5 Recommended DNA-lens extraction (grounded, not paraphrased)

A DNA lens is a **pointer plus an extraction strategy**, never a copy:

- `anchor: "PHL-035"`, `extract.strategy: "origin_verbatim"` → the axiom *is* the register instruction. Preserves the immutability of $\Omega$ by construction.
- `anchor: "FEAT-598"`, `extract.strategy: "synthesis_narrative"` → *"...treating underlying technical truth as a fixed immutable coordinate and stylistic tone as a rotation in vector space"* is an excellent **register** lens and a dangerous **rubric** lens.
- `anchor: "BKM-011"`, `extract.strategy: "origin_verbatim"` → imperative protocol text as a *structural* lens.
- **Domain routing matters:** `PHL`/`VIBE` → register axes; `BKM`/`FEAT` → structural rubrics; `DISC` → epigraph/context layers. `RDNA` and `RESUME` are **ground truth and must be barred from lens roles** — a lens that reshapes `RESUME-0xx` is editing the thing lenses are supposed to project *from*.

---

## 4. SEQUENCED OUTLINE PROPOSAL (with proposed `WIS-xxx` mappings)

⚠️ **All WIS ids below are provisional.** The `wisdom` bucket currently contains PHL ids (§3.4). **BKM-060 re-bucketing must complete before allocation.** I propose reserving from **WIS-050 upward** to clear `WIS-012`.

| § | Section | Core claim | Proposed card | Domain |
|---|---|---|---|---|
| 1 | Topology reconciliation | The card's formula is a diamond; rename the feature | — *(sprint-plan correction, not a card)* | `SPRINT` |
| 2 | The invariance formalism | $\pi\circ F_L = \pi$; retractions; fibers | `WIS-050` — *Projection as Retraction* | `WIS` |
| 3 | The eight invariants | CP-1…CP-8 with symbolic/semantic allocation | `WIS-051` — *The Symbolic Enforcement Partition* | `WIS` |
| 4 | Error model & D-1 | Re-anchor, don't re-generate; $\sum \to \max$ | `WIS-052` — *Re-Anchoring Over Re-Generation* | `WIS` |
| 5 | Rubric-relative bisimulation | Drift as a rubric defect rate, not substring presence | `WIS-053` — *Drift Is Relative to the Rubric* | `WIS` |
| 6 | Rubric compilation totality | $\operatorname{craft}: \mathcal G \to R \sqcup \{\bot\}$; coverage postcondition | `WIS-054` — *The Refusal Branch* | `WIS` |
| 7 | Structure ⊥ Register | $[\sigma_R,\rho_v]=0$ on $N(\pi)$ | `WIS-055` — *Orthogonal Register and Structure* | `WIS` |
| 8 | The preference gap | Detectors are not objectives; the missing ledger | `WIS-056` — *A Rubric Without Preference Is a Detector* | `WIS` |
| 9 | DNA-lens resolution | `(domain,id)` resolution; extraction strategies; barred domains | — *(blocked on BKM-060; defer allocation)* | `BKM` |

**Companion non-WIS artifacts this synthesis requires:**
- **`BKM-069` (proposed):** *Projection Topology & Re-Anchoring Law* — the D-1 mandate as an operational protocol.
- **`FEAT-620` (proposed):** *Composable Projection Invariant Validator & Lens v2 Schema.* Chosen because **`FEAT-619` is already claimed** by the decoupled morning-accountability watchdog.
- **Prerequisite data story:** manifest bridge writing `vibe` + `inspiration` collections and populating PHL titles.

---

## 5. RECOMMENDED JSON SCHEMA — LENS v2 & RUBRIC v2

**Compatibility contract:** a v1 preset loads unchanged. `lens_kind` defaults to `"static_preset"`; all v2 fields are optional-with-defaults on read. **No v1 consumer breaks.**

### 5.1 `lenses/<lens_id>.json` (v2 envelope)

```json
{
  "schema_version": "2.0.0",
  "lens_id": "farah_sharghi_recruiter_v1",
  "lens_kind": "static_preset",
  "title": "Farah Sharghi (Recruiter Lens v1)",
  "status": "CERTIFIED",

  "provenance": {
    "lens_kind_origin": "hand_authored",
    "derived_from": { "type": "guidance_text", "ref": "ex-google-recruiter-playbook" },
    "compiler_prompt_sha256": null,
    "source_coverage": null,
    "craft_status": "N/A",
    "certified_by": "human",
    "parent_lens_id": null
  },

  "persona": {
    "name": "Farah Sharghi (Recruiter Lens)",
    "role": "Principal Recruiter & Talent Architect",
    "lens_perspective": "Pragmatic hiring manager scanning for high-signal proof points"
  },

  "stack": {
    "mode": "single",
    "order_canonical": true,
    "lenses": [
      { "scope": "global", "rubric_ref": "inline", "voice_ref": "formal_dense_v1", "depends_on": [] }
    ]
  },

  "rubric_ref": "inline",

  "rubric": {
    "rubric_id": "recruiter_v1",
    "version": "2.0.0",
    "domains": [],
    "tiers": {
      "tier_0_structural": [
        {
          "rule_id": "FIRST_3_WORDS_POWER_VERB",
          "category": "PROSE",
          "target": "bullet_opening",
          "severity": "CRITICAL",
          "description": "Start every bullet with a high-impact power verb...",
          "positive_criterion": "Opening verb is in POWER_VERBS and is not a WEAK_OPENINGS prefix.",
          "detector": { "mode": "symbolic", "kind": "regex_prefix_list", "params": { "allow": "POWER_VERBS", "deny": "WEAK_OPENINGS" } },
          "enforcement": { "guards_invariant": null, "severity_gate": "BLOCK_PUBLISH" }
        },
        {
          "rule_id": "NUMERIC_LITERAL_INTEGRITY",
          "category": "PROSE",
          "target": "bullet_body",
          "severity": "CRITICAL",
          "description": "Every numeric literal must appear verbatim in an immutable origin span.",
          "positive_criterion": "set(numerics(output)) is a subset of set(numerics(origin_spans))",
          "detector": { "mode": "symbolic", "kind": "numeric_literal_subset", "params": { "scope": "bone", "trace": "origin" } },
          "enforcement": { "guards_invariant": "CP-5", "severity_gate": "BLOCK_PUBLISH" }
        }
      ],
      "tier_1_semantic": [
        {
          "rule_id": "SO_WHAT_METRIC_DRILL",
          "category": "REFINEMENT",
          "target": "bullet_body",
          "severity": "HIGH",
          "description": "Every bullet must pass the 'So What?' test...",
          "positive_criterion": "Bullet ties the task to operational or business impact.",
          "detector": { "mode": "semantic", "kind": "llm_judge", "params": { "judge_model": "cloud-oracle", "temperature": 0.0, "prompt_sha256": "..." } },
          "enforcement": { "guards_invariant": null, "severity_gate": "REVIEW_FLAG" }
        }
      ]
    }
  },

  "voice": {
    "voice_id": "formal_dense_v1",
    "actuation": "prompt_text_transform",
    "coupling": "orthogonal",
    "axes": { "formality": 0.8, "density": 0.7, "register": 0.6 }
  },

  "render": {
    "structure": "bullet_star",
    "target_format": "paper_ast",
    "max_chain_depth": 2
  },

  "invariants_guarded": ["CP-1", "CP-4", "CP-5", "CP-7"],

  "deprecated_aliases": { "rubric_rules": "rules" }
}
```

### 5.2 `dna_card` and `composite` lens kinds

```json
{
  "schema_version": "2.0.0",
  "lens_id": "dna_phl035_projection_axiom",
  "lens_kind": "dna_card",
  "title": "Truth Invariant / Presentation Fluid (PHL-035)",
  "status": "CERTIFIED",
  "provenance": {
    "lens_kind_origin": "dna_pointer",
    "derived_from": { "type": "dna_card", "domain": "PHL", "id": "PHL-035" },
    "source_coverage": 1.0, "craft_status": "BOUND", "certified_by": "human"
  },
  "dna": {
    "domain": "PHL", "id": "PHL-035",
    "extract": { "strategy": "origin_verbatim", "max_chars": 600, "fallback": "synthesis_narrative" },
    "role": "register",
    "resolver": { "require_title": true, "on_missing": "UNRESOLVED" }
  },
  "stack": { "mode": "single", "order_canonical": true,
             "lenses": [{ "scope": "global", "rubric_ref": "none", "voice_ref": "self", "depends_on": [] }] }
}
```

`extract.strategy` ∈ `origin_verbatim` | `synthesis_narrative` | `rationale_clause` | `mechanism_list` | `origin_block` (`BKM`).
`role` ∈ `register` | `structure` | `epigraph` | `context`.
**`resolver.on_missing: "UNRESOLVED"`** is the fix for §3.4 — an unresolvable anchor must fail loudly rather than render an empty lens.

```json
{
  "schema_version": "2.0.0",
  "lens_id": "composite_recruiter_plus_phl035",
  "lens_kind": "composite",
  "stack": {
    "mode": "dag",
    "order_canonical": true,
    "lenses": [
      { "scope": "global", "rubric_ref": "farah_sharghi_recruiter_v1", "voice_ref": "formal_dense_v1", "depends_on": [] },
      { "scope": "local:sec_experience", "rubric_ref": "none", "voice_ref": "terse_v1", "depends_on": [] },
      { "scope": "local:sec_summary", "rubric_ref": "none", "voice_ref": "none", "depends_on": ["global"] }
    ]
  },
  "merge": { "operator": "concat_ordered", "tie_break": "stack_index" }
}
```

`depends_on` is what makes the DAG explicit and enforces CP-2. Two `scope: "local:*"` entries with disjoint targets are **provably commutative** and may be reordered; entries with a `global` scope edge may not.

### 5.3 The merge operator `M`

Must be **declared, not implicit** — the fan-in of a diamond is where unexamined composition happens.

`concat_ordered` · `priority_merge` · `consensus_vote` · `last_writer_wins` (**discouraged**; permitted only with a recorded `override_reason`)

### 5.4 `rubrics/<rubric_id>.json` (standalone, for reuse across lenses)

```json
{
  "schema_version": "2.0.0",
  "rubric_id": "recruiter_v1",
  "domain": "career_document",
  "detector_budget": { "tier_0_max_rules": 40, "tier_1_max_rules": 8, "semantic_calls_per_projection": 0 },
  "tiers": { "tier_0_structural": [], "tier_1_semantic": [] },
  "severity_ladder": ["CRITICAL", "HIGH", "MEDIUM", "INFO"],
  "gates": { "BLOCK_PUBLISH": ["CRITICAL"], "REVIEW_FLAG": ["HIGH", "MEDIUM"] }
}
```

`detector_budget` is the direct answer to §3.3: it makes the cost model **visible in the artifact** rather than emergent in a profiler.

### 5.5 The projected-output stamp (enables CP-7)

```json
{
  "projection_stamp": {
    "lens_id": "composite_recruiter_plus_phl035",
    "rubric_sha256": "…", "voice_sha256": "…",
    "stack_order": ["global:recruiter_v1", "local:sec_experience"],
    "source_revision_id": "PAPER-RESUME_v1",
    "source_bones_sha256": "…",
    "model_id": "llama-3.2-3b-awq", "temperature": 0.0,
    "chain_depth": 2,
    "created_at": "2026-09-28T00:00:00Z"
  }
}
```

`F_L` **short-circuits** when an input already carries a matching `(lens_id, rubric_sha256, source_revision_id)` stamp. This is CP-7 made executable — and it is what makes a static 0ms view switch safe against a generative backend. The stamp is also the reproducibility record the current air-gapped publish path (`publish_paper.py` — *"0 live API dependencies"*) currently lacks entirely.

---

## 6. ADVERSARIAL PEER REVIEW

### 6.1 Logical gaps

**A1 — The feature name contradicts its own mathematics.** Highest-severity finding. Fix before design (§3.1).

**A2 — No empirical basis for the central concern.** The 3 "views" are deterministic string templates (`publish_paper.py:86–164`): formal = raw paragraphs; executive = *first sentence bolded, remainder dimmed*; story = *same text plus epigraphs*. **No LLM is called; no chain exists; no decay has ever been observed.** Every invariant here is prophylactic. That is legitimate — but it means the invariants are being designed against an imagined adversary, and the risk is that they encode a failure mode the eventual implementation never exhibits while missing the one it does. **Recommendation: land the symbolic CP-1/CP-5/CP-7 gates *before* any LLM projection exists.** They are correct regardless, they cost ~0 ms, and they will convert the first real decay event from a mystery into a reproducible failure.

**A3 — `grade_paper` has a cross-paper overwrite bug.** Line 302: `rev_filename = f"PAPER-RESUME_v2_{lens_id}.json"` — hardcoded, ignoring the `paper_id` and `revision_id` parameters the function accepts and the router passes (`router.py:2337`). Grading `PAPER-002` **silently overwrites the resume's graded output**. Compounded by the silent 3-tier path fallback (lines 164–171) and by `graded_ast` / `ast` being the same object returned under two keys (lines 315–316).

**A4 — Rubric rules and the grading code have already drifted.** `grade_paper` implements a *subset* of the rubric and is hardcoded to resume shapes (`sec_summary`, `sec_experience`). It ignores `severity` (emits `HIGH` where the rubric says `CRITICAL`, line 256), ignores `target` entirely, and only consumes `WEAK_OPENINGS` / `POWER_VERBS` module constants. The rubric is **data**; the grader is **code that used to be the rubric**. Under lens v2 this must invert: the grader reads `target`/`severity` from data, and a rule with no bound detector is a **compile error**.

**A5 — No positive objective.** Every rule in the current rubric is a defect detector. There is no criterion by which lens A is *better than* lens B. Without paired preference data the rubric compiler cannot be trained, tuned, or validated — only spot-checked. This is the largest *research* gap in the story and it maps cleanly onto Axiom E1: the lab already believes human disagreement is its highest-fidelity signal, and this story is the one place that belief is not being cashed in.

**A6 — Evaluation circularity is unaddressed.** If the same model family both generates and judges, self-preference bias (Wang et al. 2024) will present as *drift* while being a judge artifact. **Any observed decay must be falsified against a held-out judge or a human read before the chain is blamed.** This must be stated in the spec or the team will spend a sprint debugging their own metric.

### 6.2 KV-cache & context assumptions (explicitly requested)

**A7 — No prompt-prefix stability is specified, and the schema must mandate it.** The current system makes one LLM call per request with no shared prefix. The moment a chain exists, every step re-sends the full bone payload. If the rubric block is not a **byte-identical prefix**, prefix caching collapses and per-step cost multiplies. Therefore the v2 serializer **must** be canonical:

```python
json.dumps(block, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
```

frozen per rubric/voice and keyed by SHA-256. This is a *schema* requirement, not an optimization — a non-canonical serializer silently converts every chain into a cache-miss chain.

**A8 — Rubric-staleness invalidation is unowned.** `BKM-057` (config-to-daemon freshness) governs config; the lens corpus has no equivalent. A rubric edited while the daemon is resident serves mixed generations. The `rubric_sha256` in the projection stamp (§5.5) is the mechanism — the daemon must refuse a request whose stamp does not match resident state, and must re-pin on change.

**A9 — Context-window pressure is unmodelled for local silicon.** `[FEAT-519] Triage Context Squeeze & Token Cap` and `[BKM-051] Context Ballast` establish that context is already a scarce resource on the 2080 Ti. A composite lens stack multiplies payload size by stack depth before any prompt is assembled. **The stack schema must carry a per-lens `payload_budget` and the validator must reject stacks exceeding the local ceiling** — a `max_chain_depth: 2` default is already in §5.1 for exactly this reason.

**A10 — Three `PAPERS_DIR` roots are in play.** `Portfolio_Dev/papers/` (`publish_paper.py:20`, `build_writer.py:17`, `validate_paper_schema.py:19`) vs. `Portfolio_Dev/field_notes/data/papers/` (`lens_service.py:23`, `decompose_resume.py:16`, `export_paper_to_gdoc.py:13`), with a third under `compile_manuscript_2.py:16`. Story 93.3's scope says *"load … from `data/papers/`"* but names `paper_jitc_intuition.json`, which **exists only in the top-level `papers/`**. `PAPER-002_SEMANTIC_PACKING.json` and `PAPER-RESUME_v1.json` exist **only** in `field_notes/data/papers/`. **The three named papers span both roots.** This is a live integration defect for 93.3 *and* 93.4 — a lens applied in the studio and a paper published offline can reference physically different files with the same `paper_id`. **Single-root resolution is a prerequisite, not a cleanup item.**

### 6.3 Missing literature / prior art

- **No formal compositional-prompt theory exists.** There is no accepted algebra of "lens composition" for LLM prompting. Anything presented as one (§2) is a *modelling choice* that buys rigor and testability, not a discovered law. It should be labelled as such internally so a future reader does not mistake a design decision for a theorem.
- **Terminological collision: "lens."** Category theory already owns this term (Borceux et al., *Lens Structures*). This project uses it for a different object. Recommend the internal name **"projection operator"** and reserving "lens" for the UI affordance only.
- **The Voice Vector's actuation point is undefined — and it is load-bearing.** Formality/Density/Register sliders (`FEAT-596`, `FEAT-617`) currently act as… what? Three possibilities with wildly different consequences: (a) **prompt-level text transforms** — deterministic, CP-8 immediately testable, the schema above works as written; (b) **decoding-level steering** (logit bias / activation steering) — requires a runtime you can actually steer, hard-binds the project to vLLM internals, and is untestable on the 3B AWQ seat; (c) **post-hoc text transforms** — deterministic but breaks provenance traceability for metric literals (violates CP-5). **Recommendation (a).** This must be decided *before* schema sign-off, because `voice.actuation` is a schema field and every downstream guarantee depends on it.
- **Uncited in the card, load-bearing here:** Shumailov et al. 2024 (*Nature*); Kuhn/Gal/Farquhar ICML 2023; Wang et al. ACL 2024; Zheng et al. NeurIPS 2023; Madaan et al. NeurIPS 2023 (Self-Refine — documented plateau/oscillation, i.e. *the* prior art on serial refinement decay); Rafailov et al. 2023 (DPO — the preference-pair formalism that A5 needs); Margatina et al. EMNLP 2021 (co-active contrastive learning — the learning analogue of BKM-035).

---

## 7. ADVERSARIAL REVIEW OF THIS SYNTHESIS ITSELF

Intellectual honesty about my own report:

- **CP-1…CP-8 are untested against a real chain, because no chain exists.** They are consequences of a *modelling choice* (π as a well-defined total operator on text). If $\pi$ is not computable in practice, CP-1 becomes uncheckable rather than merely unchecked. **The honest framing: CP-5 (numeric literal subset) is fully computable today and should ship first; CP-1 is only as strong as the claim-set extractor, which is the real open problem.**
- **The $\sum \to \max$ error model (D-1) is a heuristic, not a bound.** It is right in kind — re-anchoring structurally removes the compounding term — but I have shown no formal error decomposition, and the merge operator $M$ can itself introduce composition failure. **A diamond with a bad merge is still a bad pipeline.** Do not read D-1 as a safety guarantee.
- **CP-6's $\tau_{\min}$ has no principled value.** It must be calibrated empirically against a corpus of real projections; any number I supplied would be fabricated. The schema correctly leaves it unset.
- **I did not evaluate the alternative** where a genuine serial chain *is* wanted — e.g. a multi-pass refinement where pass 2 is supposed to improve on pass 1. For that use case the diamond is wrong and CP-3's contractivity is the only thing keeping it sane. **This story should state which of the two it is building.** If both, they need different names, different metrics, and different UI affordances.

---

## 8. RECOMMENDED ACTION ORDER (for `[AGY:PRIMARY]` — not for me; I am read-only)

| # | Action | Blocks | Owner tag |
|---|---|---|---|
| 0 | **Reconcile the plan text**: rename to *Composable Projections*, or restate the topology as explicitly serial with a depth cap | 93.4 scoping | `[AGY:PRIMARY]` |
| 1 | Unify `PAPERS_DIR` to a single root (§6.2 A10) | 93.3, 93.4, 93.5 | `[SWARM:LOCAL]` |
| 2 | Manifest bridge: write `vibe` + `inspiration`; populate PHL titles; **BKM-060 re-bucketing of the `wisdom` bucket** | Anchor 2, all WIS allocation | `[SWARM:LOCAL]` |
| 3 | Fix `grade_paper` cross-paper overwrite + duplicate `ast`/`graded_ast` + `rubric_rules` duplication | any rubric work | `[SWARM:LOCAL]` |
| 4 | Land symbolic gates **CP-5, CP-7, CP-4** before any LLM projection | nothing — these are free | `[SWARM:LOCAL]` |
| 5 | Implement `craft()` totality with the coverage postcondition + `UNSAFE_TO_CRAFT` | Anchor 1 | `[SWARM:LOCAL]` |
| 6 | **Decide `voice.actuation`** (§6.3) before schema sign-off | schema freeze | `[AGY:PRIMARY]` |
| 7 | Schema v2 + `validate_paper_schema.py` gate (FEAT-620) | 93.5 | `[SWARM:LOCAL]` |
| 8 | **Stand down 93.5's real-time semantic preview** → symbolic-only, debounced | 93.5 feasibility | `[AGY:PRIMARY]` |
| 9 | Stand up the preference ledger (A5 / Axiom E1) | rubric validation | `[SWARM:LOCAL]` |

---

## 9. HANDOVER REFLECTION

The most expensive gap was a **direct contradiction between the brief and the codebase**: the directive told me to synthesize a specification for "prompt-rubric driven Lens Crafting," and I spent real budget discovering that `craft_lens()` never reads its input and that the "chained projections" it asked me to model are three hardcoded string templates with no LLM and no chain. Had the story card carried three lines of *current-state* grounding — "craft_lens ignores `content`; views are templates; `vibe` is absent from the manifest" — roughly half my reconnaissance would have been unnecessary and the report could have opened on the mathematics instead of on the discrepancy. Compounding that, the brief's own `[FUNCTIONAL REQUIREMENTS]` told me to save the report to a file while the directive twice told me to make **zero edits**, and I resolved it by refusing to write — the single change that would have made this faster is resolving that conflict *in the prompt* (either naming the write as a separate `[AGY:PRIMARY]` step or dropping it), because an advisory synthesizer that half-obeys its write instruction is worse than one that cleanly declines.

---

### Handoff artifact (no edits performed)

`ORACLE_REVIEW_SPRINT_93.md` **does not exist** at `Portfolio_Dev/docs/sprints/active/`. To materialize this report:

```bash
# Primary agent: write the §1–§9 body above, then
cd /home/jallred/Dev_Lab/Portfolio_Dev && git add docs/sprints/active/ORACLE_REVIEW_SPRINT_93.md && git commit -m "docs(SPR-93.4): Oracle synthesis — Chained Projections & Lens Crafting [FEAT-620]"
```

**Compliance attestation:** zero file edits, zero writes, zero git operations, zero delegations. Read-only advisory synthesis, delivered as markdown.
