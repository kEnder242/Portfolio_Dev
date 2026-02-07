# SESSION BKM - FEB 07
**Goal:** Website Rebranding, UI Evolution, and Automated Cache-Busting

## 🏗️ State of the Union
- **Stories Entry:** `index.html` renamed to `stories.html`. Transparent redirect in place.
- **Sidebar Rebrand:** Icon-free, high-density labels standardized across all pages.
- **Timeline v2.5:** Typewriter speed increased by 5x (5 chars/tick). Live telemetry grid added (Events, Last Scan, Load).
- **Build System:** `build_site.py` created to automate MD5-based cache-busting.

## 🚀 Technical Wins: The Build Protocol
To ensure CSS/JS changes propagate instantly to mobile and desktop browsers, we now use a "Hash-on-Build" strategy.

**The One-Liner:** 
```bash
python3 field_notes/build_site.py
```

**The Core Logic:** 
Calculates MD5 hashes of `style.css`, `script.js`, and `intercom_v2.js`, then updates the `?v=` query strings in all HTML files (`stories.html`, `timeline.html`, `files.html`, `pager.html`, `intercom/index.html`).

**The Trigger:** 
Must be run after any modification to CSS or JS files before deployment.

**The Scars:** 
Manual versioning (`?v=10.3`) is prone to human error and browser caching stalls. Automated hashing is the only way to guarantee cache-clearing on mobile.

## 🛠️ Updated Sidebar Order
1. Stories
2. Notes: Logs
3. Artifacts: Files
4. Pager: Alerting
5. Intercom
6. Graphana: Observability
7. VS Code (Remote) [Bottom]

## 🎯 Next Session Goals
- **Liger-Kernel Bench-test:** Measure VRAM reduction on the 2080 Ti.
- **TTT-Discover Integration:** Explore active discovery paths for silicon failures.
- **Intercom Sidebar:** Add the "Report Writer" synthesis UI.
