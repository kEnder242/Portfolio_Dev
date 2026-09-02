# 🗺️ Context & Memory Flow Diagram Map
**Architecture Anchor:** `[LAB-523]` / `[BKM-050]`  
**Domain:** Bicameral Cognitive Hub, Context Scoping & Multi-Tier Memory RAG  

---

## 1. Global Memory Hierarchy

```mermaid
flowchart TD
    subgraph S1["Tier 1: Distant Wisdom (Static / Epochal)"]
        GEMS["18-Year Gems Archive\n(Diamond Artifacts, BKM Library)"]
        CLARA_WISDOM["ChromaDB: long_term_wisdom\n(Architectural Decisions, Historical Scars)"]
    end

    subgraph S2["Tier 2: Episodic & Behavioral Memory (Dynamic / Multi-Session)"]
        CLARA_BEHAVE["ChromaDB: behavioral_dna\n(Operational BKMs, Swarm Laws)"]
        CLARA_FEAT["ChromaDB: feature_dna\n(System Feature Specs)"]
        BLACKBOARD_DNA["ChromaDB: blackboard_ledger_dna\n{turn, topic, timestamp, distillation, consensus}"]
    end

    subgraph S3["Tier 3: Active Turn Context (In-Flight Working Memory)"]
        USER_DISPATCH["User Prompt (t=0)"]
        TRIAGE_SCOPE["ContextScope.TURN\n(Isolated: Query Only)"]
        MICE_LONG["ContextScope.LONG\n(Mice: Blackboard + 1 Prior Turn)"]
        DEEP_SCOPE["ContextScope.TURN\n(Deep Thought: Turn Deliberation)"]
    end

    USER_DISPATCH --> TRIAGE_SCOPE
    TRIAGE_SCOPE -->|Routing Decision| MICE_LONG
    BLACKBOARD_DNA -.->|Semantic + Time-Decay Retrieval| MICE_LONG
    CLARA_BEHAVE -.->|Protocol Fast-Path| MICE_LONG
    GEMS -.->|Grounded Citations| MICE_LONG
    MICE_LONG -->|Turn Debate Transcript| DEEP_SCOPE
    DEEP_SCOPE -->|Consensus Synthesis| MICE_LONG
```

---

## 2. The Interest Cycle: Rise, Deliberation & Distillation

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Impatient User
    participant Foyer as 🚪 Foyer Router
    participant Triage as 🧭 Speculative Triage<br/>(ContextScope.TURN)
    participant Pinky as 🐭 Pinky (Intuition / Take)<br/>(ContextScope.LONG)
    participant Brain as 🧠 Brain (Technical Stance)<br/>(ContextScope.LONG)
    participant Deep as 🔮 Deep Thought (Oracle)<br/>(ContextScope.TURN)
    participant Board as 📋 Blackboard Ledger<br/>(Episodic State)

    User->>Foyer: "Analyze PCIe bus error bursts"
    Foyer->>Triage: Dispatch (Query Only, 0 Memory)
    Triage-->>Foyer: Triage Result {addressed_to: PINKY, vibe: TECHNICAL}
    
    Note over Pinky,Board: [Rise of the Round Table: Context Ingestion]
    Board-->>Pinky: Inject Blackboard (Consensus + 1 Prior Turn)
    Foyer->>Pinky: Pinky Leg: Initial Stance & Reactive Intuition
    Pinky-->>Foyer: Pinky Take ("Narf! Sounds like a PCIe link training glitch!")

    opt Interest > 0.5 (Brain Interjection)
        Board-->>Brain: Inject Blackboard + Pinky Take
        Foyer->>Brain: Brain Leg: Architectural Deep-Dive
        Brain-->>Foyer: Brain Stance ("PCIe Gen5 eye margin failure at root complex")
        Brain->>Board: ✍️ Writes Distillation Bullets & Technical Anchors
    end

    opt High Intrigue / Speculation
        Foyer->>Deep: Package Current Turn Debate (Pinky + Brain)
        Deep-->>Foyer: Deep Thought Synthesis (Oracle Verdict)
    end

    Note over Pinky,Board: [Fall of the Round Table: Compression & Distillation]
    Foyer->>Pinky: Pinky Leg: Final Summary & Critique
    Pinky-->>User: Spoken Response Delivered
    Pinky->>Board: 🏁 Closes Turn: Writes 1-Line Consensus & Turn Ledger
    Board->>Board: Commit to blackboard_ledger_dna in ChromaDB
```

---

## 3. Scoping & Memory Contract Matrix

| Actor / Component | Context Scope | Ingested Memory | Generated Output | Write Target |
| :--- | :--- | :--- | :--- | :--- |
| **Triage** | `ContextScope.TURN` | Fresh Query Only ($< 200$ tokens). Zero previous debate. | Routing JSON (`vibe`, `addressed_to`, `importance`). | Foyer Router |
| **Pinky (Initial)** | `ContextScope.LONG` | Blackboard (Consensus summary) + Last 1 Turn. | Reactive intuition / fast-path answer. | Foyer UI Stream |
| **Brain** | `ContextScope.LONG` | Blackboard + Pinky Initial Take + ChromaDB Gems/Wisdom. | Technical analysis + Distillation bullets. | **Blackboard Ledger** |
| **Deep Thought** | `ContextScope.TURN` | Current Turn Package only (User query + Pinky take + Brain stance). | Speculative synthesis / oracle verdict. | Foyer UI Stream |
| **Pinky (Judge)** | `ContextScope.LONG` | Brain Stance + Deep Thought Verdict + User Query. | Final spoken dialogue + 1-line consensus. | **ChromaDB Blackboard DNA** |

---

## 4. Blackboard Ledger DNA Schema

Stored in ChromaDB collection `blackboard_ledger_dna`:
```json
{
  "turn_number": 42,
  "timestamp": 1788373200,
  "iso_time": "2026-09-02T13:15:00-07:00",
  "topic": "PCIe Gen5 Link Degradation",
  "actors_involved": ["pinky", "brain", "deep_thought"],
  "distillation_bullets": [
    "Eye margin reduction on Lane 4 during thermal burst",
    "Root complex bifurcation set to x8/x8",
    "Retimer firmware re-flash recommended"
  ],
  "consensus_1liner": "Link retraining instability caused by marginal signal-to-noise ratio at 32 GT/s."
}
```
