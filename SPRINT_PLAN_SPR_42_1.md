# Sprint 42.1 -- Interleaved System Logs: Declutter, Smart Expand Tiers, and Artifact Enrichment

> **Goal:** Transform the Interleaved System Logs from a flat, noisy, 454-entry wall of `[+]` widgets into a high-signal, tiered display where routine systemd chatter collapses into 6-hour time bands, the `[+]` expand indicator is reserved for events with *real* forensic payloads, and new artifact-backed expansion types are implemented.

---

## Forensic Analysis: Current State of the Logs

### Data Distribution (as of 2026-07-21)

| Category | Count | % of Total | Notes |
|---|---|---|---|
| `systemd` (service starts/stops) | 282 | 62% | Bulk noise. Repeating 5-minute cron cycles. |
| `tracker-miner-fs-3` (GLib warnings) | 131 | 29% | Identical GLib-GIO mountinfo errors every 5 min. |
| `tailscaled` (Tailscale health) | 30 | 7% | Periodic "netcheck" and health updates. |
| `MassScan` / `Foyer` / `RAG` / `Montana` / `MCTP` | 8 | 2% | The *interesting* entries. Buried in noise. |
| **Total** | **454** | | |

### The `[+]` Widget Problem

**Every single log entry** currently gets a `[+]` expand indicator. Of 454 entries:
- **0** have a recruiter brief to expand.
- **15** are RAG-eval entries (from `validation_ledger.jsonl`) with rich metric panels.
- **~8** match the "green" heuristic but are **false positives** (`apport-autoreport` matches substring `report`).
- **~431** expand to `Metadata: {"timestamp":"...","source":"systemd",...}` -- raw JSON of what is already in the one-liner.

---

## File Map (Reference for all Stories)

| File | Purpose | Key Line Ranges |
|---|---|---|
| `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/status.html` | Primary target. Contains all JS functions. | L1017-1104: `renderInterleavedTimeline()`, L1106-1170: `createAlertElement()`, L1172-1369: `expandAlertDetail()` |
| `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/style.css` | CSS for tree structure. | L69-116: `.tree-year`, `.year-label`, `.year-content` classes |
| `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/pager_activity.json` | 454-entry log JSON array. READ ONLY -- do not modify structure. | N/A |
| `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/validation_ledger.jsonl` | 15-entry RAG-eval JSONL. READ ONLY. | N/A |
| `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/bench_models.py` | Benchmark script. Story 11.3 adds `trigger_pager()` call here. | End of `main()` |
| `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/mass_scan.py` | Nightly scan script. Story 11.4 adds `trigger_pager()` call here. | End of `--once` path |

---

## Sprint Stories & Actionable Tasks

### Story 8: 6-Hour Time-Band Collapsing within Day Folders

*   **Why:** Today's day folder contains 317 entries in a flat list. Scrolling through 5-minute cron cycles to find a MassScan event is impractical. The original commit `74e032a` ("Priority-Interleaved Status Timeline") intended sub-day grouping but only implemented the day tier.
*   **Design:** Within each day folder, group entries into 6-hour time bands:
    - `00:00 - 05:59` (Overnight)
    - `06:00 - 11:59` (Morning)
    - `12:00 - 17:59` (Afternoon)
    - `18:00 - 23:59` (Evening)
    
    Each band is collapsible (reuse the `.tree-year` / `.year-content` CSS pattern). WARNING/CRITICAL events still break out above time bands at the day-folder root level.

*   **OpenAgent Delegation Plan (BKM-034):**
    - *Role:* `Frontend Developer`
    - *Target Dir:* `/home/jallred/Dev_Lab/Portfolio_Dev`
    - *Session Format:* `SESSION: Sprint 42.1 Story 8 -- 6-Hour Time-Band Collapsing in Interleaved System Logs`
    - *Exclusion:* Do NOT modify `expandAlertDetail()`, `createAlertElement()`, `pollPager()`, or any Python files. Scope is strictly `renderInterleavedTimeline()` (L1017-1104 of `status.html`) and CSS additions to `style.css`.

*   **Task Checkboxes:**
    - [ ] **Task 8.1 (Time-Band Grouper in `renderInterleavedTimeline`):** Refactor the `sortedAlerts.forEach` loop at **L1039-1056** of `status.html`. Currently it tracks only `currentDayFolder`. Add a second pointer `currentTimeBand` that groups entries into 6-hour segments within each day folder.
      
      **Current loop structure (L1039-1056):**
      ```javascript
      sortedAlerts.forEach(alert => {
          // ... severity check ...
          if (severity === 'critical' || severity === 'warning') {
              nodes.push({ type: 'priority', data: alert });
              currentDayFolder = null;
          } else {
              if (!currentDayFolder || currentDayFolder.day !== day) {
                  currentDayFolder = { type: 'folder', day: day, items: [] };
                  nodes.push(currentDayFolder);
              }
              currentDayFolder.items.push(alert);
          }
      });
      ```
      
      **Target structure:** Each day folder's `items` array becomes an array of `{ band: '06:00-11:59', label: 'Morning', items: [] }` objects. Derive band from hour: `const hour = new Date(ts).getHours(); const bandIdx = Math.floor(hour / 6);` mapping to labels `['Overnight','Morning','Afternoon','Evening']`.

    - [ ] **Task 8.2 (Time-Band DOM Renderer):** Refactor the DOM builder at **L1070-1102** of `status.html`. Currently it iterates `node.items.forEach(a => ...)` and appends directly to `list`. Instead, iterate over time bands, creating a collapsible sub-folder for each band using the same `.tree-year` / `.year-label` / `.year-content` CSS pattern (or a new `.tree-band` class if differentiation is needed). Auto-expand the most recent band on initial load.

    - [ ] **Task 8.3 (CSS for Time Bands):** Add `.tree-band` styles to `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/style.css` after L116. Model after `.tree-year` but with subtle differentiation:
      ```css
      .tree-band { margin-bottom: 3px; }
      .band-label { cursor: pointer; color: #8b949e; padding: 3px 0; user-select: none; font-size: 0.85em; }
      .band-label:hover { color: var(--accent-color); }
      .band-label::after { content: '[+]'; display: inline-block; width: 30px; color: #555; margin-right: 5px; font-size: 0.8em; }
      .tree-band.open .band-label::after { content: '[-]'; color: var(--accent-color); }
      .band-content { display: none; margin-left: 10px; border-left: 1px dashed #333; padding-left: 15px; }
      .tree-band.open .band-content { display: block; }
      ```

*   **Scars & Failures to Avoid:**
    *   **The Flat-Loop Refactor Scar:** Keep the same running-pointer pattern (`currentDayFolder` + `currentTimeBand`). Do NOT attempt a recursive tree-builder rewrite.
    *   **Open-State Preservation:** The existing `openNodes` Set (L1020-1021) preserves day-folder open state across polls. Extend this to also track `.tree-band.open` elements by ID (e.g., `band-2026-07-21-1` for the Morning band).
*   **Verification Gate:**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python -c "
    import asyncio
    from playwright.async_api import async_playwright
    async def check():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page()
            await page.goto('http://localhost:9001/status.html', wait_until='networkidle')
            await asyncio.sleep(4)
            bands = await page.query_selector_all('.tree-band')
            print(f'Time bands found: {len(bands)}')
            assert len(bands) > 0, 'No time bands rendered'
            # Verify band labels contain expected text
            label = await bands[0].inner_text()
            print(f'First band label: {label}')
            await b.close()
    asyncio.run(check())
    "
    ```

---

### Story 9: Three-Tier Expand Classification (Kill the Useless `[+]`)

*   **Why:** 431 of 454 entries (95%) expand to a raw `JSON.stringify(alert)` dump. The `[+]` widget trains the user to ignore all expansions, hiding the 15 RAG-eval entries with real forensic panels.
*   **Design:** Classify each alert at creation time in `createAlertElement()` (**L1106-1170** of `status.html`):
    *   **Tier 1 (`expandable-rich`):** `[+]` in accent blue. These have real forensic payloads.
    *   **Tier 2 (`expandable-inline`):** `[>]` in muted grey. 1-2 extra detail lines, no full terminal panel.
    *   **Tier 3 (`no-expand`):** No widget, no onclick handler. The one-liner IS the information.

*   **OpenAgent Delegation Plan (BKM-034):**
    - *Role:* `Frontend Developer`
    - *Target Dir:* `/home/jallred/Dev_Lab/Portfolio_Dev`
    - *Session Format:* `SESSION: Sprint 42.1 Story 9 -- Three-Tier Expand Classification`
    - *Exclusion:* Do NOT modify `renderInterleavedTimeline()` or `pollPager()`. Scope is strictly `createAlertElement()` (L1106-1170) and the top of `expandAlertDetail()` (L1172+). Do NOT change `expandAlertDetail()` internal logic for recruiter/RAG-eval/crash -- only add the tier classification gate at entry.

*   **Task Checkboxes:**
    - [ ] **Task 9.1 (Tier Classification Function):** Add a new function `classifyExpandTier(alert)` above `createAlertElement()` at ~L1105. Returns `'rich'`, `'inline'`, or `'none'`.
      ```javascript
      function classifyExpandTier(alert) {
          const src = (alert.source || '').toLowerCase();
          const msg = (alert.message || '').toLowerCase();
          
          // Tier 1: Rich expand -- real forensic payloads
          if (alert.is_rag_eval) return 'rich';
          if (src === 'recruiter') return 'rich';
          if (src === 'massscan') return 'rich';
          if (src === 'benchmark') return 'rich';
          if (['foyer','ignition','labattendant','montana'].includes(src)) return 'rich';
          if (msg.includes('crash_') && msg.includes('.log')) return 'rich';
          if (msg.includes('gem refined') || msg.includes('distilled')) return 'rich';
          if (msg.includes('nightly-dialogue')) return 'rich';
          
          // Tier 2: Inline detail -- moderate context
          if (src === 'tailscaled') return 'inline';
          if (src === 'cloudflared') return 'inline';
          if (src === 'mctp') return 'inline';
          
          // Tier 3: No expand -- routine noise
          return 'none';
      }
      ```

    - [ ] **Task 9.2 (Conditional Widget in `createAlertElement`):** At **L1147-1154** of `status.html`, the `div.innerHTML` template currently always renders `<span class="expand-indicator">[+]</span>`. Replace with tier-conditional rendering:
      
      **Current (L1147-1154):**
      ```javascript
      div.innerHTML = `
          <div class="alert-header">
              <span class="expand-indicator" style="...">[+]</span>
              <span class="alert-meta">[${timeStr}]</span> 
              <span style="...">${alert.source}:</span> ${alert.message}
          </div>
          <div class="inline-terminal"></div>
      `;
      ```
      
      **Target:** Call `const tier = classifyExpandTier(alert);` before the innerHTML assignment. Add `tier` as a CSS class on the div (`expandable-rich`, `expandable-inline`, or `no-expand`). For Tier 1: render `[+]`. For Tier 2: render `[>]` in `#666`. For Tier 3: render no indicator span at all and omit the `<div class="inline-terminal">`.

    - [ ] **Task 9.3 (Conditional onclick in `createAlertElement`):** At **L1159-1169**, the `header.onclick` handler currently always calls `expandAlertDetail()`. For Tier 3, do NOT attach an onclick handler at all. For Tier 2, attach a handler that toggles a single `.inline-detail` line (not the full `.inline-terminal` panel).

    - [ ] **Task 9.4 (Fix False-Positive Green Heuristic):** At **L1116-1125**, the `hasArtifact` check uses `msg.includes('report')` which falsely matches `apport-autoreport`. Replace with a tighter check:
      
      **Current (L1122):**
      ```javascript
      msg.includes('report') ||
      ```
      **Target:**
      ```javascript
      msg.match(/\breport[: ]/) ||
      ```
      This matches `report:` or `report ` but NOT `autoreport`.

*   **Scars & Failures to Avoid:**
    *   **The `report` Substring Scar:** `apport-autoreport` contains `report`. The word-boundary regex prevents this false positive.
    *   **Tier Leakage:** Ensure `classifyExpandTier` is called ONCE per alert and the result is used consistently for CSS class, indicator rendering, AND onclick binding.
*   **Verification Gate:**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python -c "
    import asyncio
    from playwright.async_api import async_playwright
    async def check():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page()
            await page.goto('http://localhost:9001/status.html', wait_until='networkidle')
            await asyncio.sleep(4)
            rich = await page.query_selector_all('.expandable-rich')
            inline_els = await page.query_selector_all('.expandable-inline')
            none = await page.query_selector_all('.no-expand')
            total = len(rich) + len(inline_els) + len(none)
            print(f'Tier 1 (rich): {len(rich)}, Tier 2 (inline): {len(inline_els)}, Tier 3 (none): {len(none)}, Total: {total}')
            assert len(none) > len(rich), f'Expected Tier 3 majority, got rich={len(rich)} none={len(none)}'
            # Verify no [+] on Tier 3 items
            for el in none[:3]:
                indicator = await el.query_selector('.expand-indicator')
                assert indicator is None, 'Tier 3 item should not have expand indicator'
            await b.close()
    asyncio.run(check())
    "
    ```

---

### Story 10: Source-Based Deduplication & Count Badges

*   **Why:** `tracker-miner-fs-3` produces an identical GLib-GIO WARNING every 5 minutes (131 entries, 29% of all logs). `media-master-sync.service` starts every 5 minutes. These are the same event repeated.
*   **Design:** Within each time band, consecutive entries with identical `source` AND normalized `message` collapse into a single entry with a `(x23)` count badge.

*   **OpenAgent Delegation Plan (BKM-034):**
    - *Role:* `Frontend Developer`
    - *Target Dir:* `/home/jallred/Dev_Lab/Portfolio_Dev`
    - *Session Format:* `SESSION: Sprint 42.1 Story 10 -- Source-Based Deduplication & Count Badges`
    - *Dependency:* Requires Story 8 (time bands) to be merged first. Dedup operates within time bands.
    - *Exclusion:* Do NOT modify `expandAlertDetail()`, `createAlertElement()`, or any Python files. Scope is strictly the item-append loop inside `renderInterleavedTimeline()` and CSS additions.

*   **Task Checkboxes:**
    - [ ] **Task 10.1 (Message Normalizer):** Add function `normalizeMessage(msg)` that strips:
      - Embedded timestamps: `HH:MM:SS.mmm` patterns
      - PIDs: `(process-name:12345)` patterns  
      - Trailing whitespace
      
      Returns a stable dedup key string.

    - [ ] **Task 10.2 (Dedup Accumulator):** In the time-band item-append loop (created in Story 8), track a running dedup key (`prevKey = source + '|' + normalizeMessage(msg)`). If consecutive entries match, increment a counter. When the streak breaks or the band ends, emit the representative entry. Pass the count to `createAlertElement()` via `alert._dedupCount = N`.

    - [ ] **Task 10.3 (Count Badge Rendering):** In `createAlertElement()`, if `alert._dedupCount > 1`, append `<span class="dedup-badge">(x${alert._dedupCount})</span>` after the message text.
      ```css
      .dedup-badge { color: #666; font-size: 0.8em; margin-left: 6px; font-style: italic; }
      ```

*   **Verification Gate:**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python -c "
    import asyncio
    from playwright.async_api import async_playwright
    async def check():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page()
            await page.goto('http://localhost:9001/status.html', wait_until='networkidle')
            await asyncio.sleep(4)
            badges = await page.query_selector_all('.dedup-badge')
            print(f'Dedup badges found: {len(badges)}')
            items = await page.query_selector_all('.alert-item')
            print(f'Total visible items: {len(items)}')
            assert len(items) < 300, f'Expected significant dedup reduction, got {len(items)} items'
            await b.close()
    asyncio.run(check())
    "
    ```

---

### Story 11: Artifact Enrichment -- New Expansion Types

*   **Why:** Only 15 RAG-eval entries currently have rich expansion panels. The `[+]` expand panel is the most visually impressive feature of the status page but is starved for content. This story adds new data sources.
*   **Dependency:** Requires Story 9 (tier system) to be merged first, so new events are classified as Tier 1.

*   **OpenAgent Delegation Plan (BKM-034):**
    - *Role:* `Full-Stack Developer`
    - *Target Dir:* `/home/jallred/Dev_Lab/Portfolio_Dev`
    - *Session Format:* `SESSION: Sprint 42.1 Story 11 -- Artifact Enrichment & New Expansion Types`
    - *Exclusion:* Do NOT modify the RAG-eval expansion logic or recruiter brief logic inside `expandAlertDetail()`. Only ADD new expansion branches. Do NOT run benchmarks (KENDER GPU contention risk).

*   **New Expandable Event Types (7 total, prioritized):**

    | Priority | Event Type | Source Field | Data Source | Expansion Panel Content |
    |---|---|---|---|---|
    | P0 | MassScan Progress | `MassScan` | Parse message text | Epoch, step, files processed, gems refined, rank upgrades, mini progress bar |
    | P0 | Lab State Transition | `Foyer` / `ignition` / `labattendant` | `data/status.json` | Previous state -> new state (color badges), trigger, VRAM, resident list |
    | P1 | Gem Refinement Diff | `nibble` / `refiner` | Monthly JSONs (`data/2024_06.json`) | Gem ID, old rank vs new rank (color arrow), synopsis diff |
    | P1 | Benchmark Completion | `benchmark` (new) | New pager entries from `bench_models.py` | Model name, cold/warm TTFT, throughput, power, $/1M tokens |
    | P2 | Nightly Dialogue | `nightly-dialogue` (new) | `data/nightly_dialogue.json` | Dream/debate summary with typewriter effect |
    | P2 | Privacy Audit | `privacy-audit` (new) | `data/privacy_audit.jsonl` | Files scanned, PII detections, pass/fail verdict |
    | P3 | Cloudflare Login | `cloudflared` | Parse message fields | Email, policy matched, source geo |

*   **Task Checkboxes:**
    - [ ] **Task 11.1 (MassScan Rich Panel):** Add `if (src === 'massscan')` branch inside `expandAlertDetail()` (after the RAG-eval block, before the recruiter block). Parse message for patterns like `Step N`, `Epoch N`, `gems refined`, `Rank N`. Render a structured panel with epoch progress, file count, and rank upgrade indicators.
    - [ ] **Task 11.2 (Lab State Transition Panel):** Add `if (['foyer','ignition','labattendant'].includes(src))` branch. Fetch `data/status.json` to get current state. Parse message for state keywords (`ONLINE`, `OFFLINE`, `HIBERNATING`, `IGNITING`). Render state badge transition with color coding (green=ONLINE, orange=HIBERNATING, red=OFFLINE, blue=IGNITING).
    - [ ] **Task 11.3 (Pager Emitter for Benchmarks):** At the end of `main()` in `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/bench_models.py`, add a `trigger_pager()` call emitting a single entry with `source: 'benchmark'` and message containing model name + key metrics. Import `trigger_pager` from the existing utility (check `field_notes/scan_pinky.py` or `field_notes/utils.py` for the existing function).
    - [ ] **Task 11.4 (Pager Emitter for Nightly Dialogue):** At the end of the `--once` path in `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/mass_scan.py`, add a `trigger_pager()` call emitting a summary event with `source: 'nightly-dialogue'`.
    - [ ] **Task 11.5 (Nightly Dialogue Expansion Panel):** Add `if (src === 'nightly-dialogue')` branch in `expandAlertDetail()`. Fetch `data/nightly_dialogue.json` and render content with the existing `simulateTyping()` function.

*   **Verification Gate:**
    ```bash
    # Verify MassScan entries now have Tier 1 expand with structured panel
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python -c "
    import asyncio
    from playwright.async_api import async_playwright
    async def check():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page()
            page.on('console', lambda msg: print(f'[CONSOLE] {msg.type}: {msg.text}'))
            page.on('pageerror', lambda err: print(f'[ERROR] {err}'))
            await page.goto('http://localhost:9001/status.html', wait_until='networkidle')
            await asyncio.sleep(4)
            # Verify zero JS errors
            await b.close()
    asyncio.run(check())
    "
    ```

---

## Global Constraints for OpenAgent

1. **Build After Each Story:** Run `python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/build_site.py` after completing each story to recompile asset hashes and deploy to airlock.
2. **Git Commit Per Story:** Stage and commit changes in `/home/jallred/Dev_Lab/Portfolio_Dev` after each story. Do NOT push. Commit message format: `feat(status): <story description>`.
3. **No Benchmark Execution:** Do NOT run `bench_models.py` or any GPU-intensive process. KENDER may be in use.
4. **Playwright Path:** Always use `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python` for Playwright tests.
5. **FEAT-417 Safety Net:** The global error trap in `script.js` (FEAT-417) will catch any uncaught JS errors and route them to `#sys-console`. Use this as a verification signal -- zero red entries in sys-console after each story.

---

## Acceptance Criteria

1. Day folders contain 6-hour time-band sub-folders (Overnight/Morning/Afternoon/Evening). Most recent band auto-expands.
2. WARNING/CRITICAL events still break out at day-folder root level above time bands.
3. `[+]` widget appears ONLY on Tier 1 events with real forensic payloads. Routine systemd entries have no expand widget.
4. Identical consecutive events within a time band collapse to a single entry with `(xN)` count badge.
5. `apport-autoreport.service` no longer falsely tagged as green/artifact.
6. At least 2 new rich expansion types (MassScan panels, Lab State panels) are implemented.
7. Zero JS errors in `#sys-console` (FEAT-417 safety net).
8. All changes committed per-story in `Portfolio_Dev`. Site rebuilt via `build_site.py`.

---

## Dependency Graph & Execution Order

```
Story 8 (Time Bands) ──┐
                        ├──> Story 10 (Dedup within bands)
Story 9 (Tier System) ──┤
                        └──> Story 11 (Enrichment)
```

**Recommended execution order:** Story 9 first (smallest diff, highest UX impact), then Story 8, then Story 10, then Story 11. Stories 8 and 9 have no cross-dependencies and can be parallelized if using separate OpenAgent sessions on branched workspaces.
