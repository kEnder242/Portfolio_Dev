class MissionControl extends HTMLElement {
    connectedCallback() {
        const currentPath = window.location.pathname;
        const activePage = currentPath.split('/').pop() || 'stories.html';

        console.log(`[MISSION CONTROL] Component connected. Active page: ${activePage}`);

        this.innerHTML = `
            <h1>The Field Manual</h1>
            <div class="subtitle">Jason Allred</div>
            <section id="mission-control">
                <h2>Mission Control</h2>
                <ul>
                    <li><a href="stories.html" class="mission-link ${activePage === 'stories.html' ? 'active' : ''}">Work Stories</a></li>
                    <li><a href="timeline.html" class="mission-link ${activePage === 'timeline.html' ? 'active' : ''}">Work Notes</a></li>
                    <li><a href="files.html" class="mission-link ${activePage === 'files.html' ? 'active' : ''}">Artifacts: Files</a></li>
                    <li><a href="status.html" class="mission-link ${activePage === 'status.html' ? 'active' : ''}">Lab Status</a></li>
                    <li><a href="intercom.html" class="mission-link ${activePage === 'intercom.html' ? 'active' : ''}">AI Lab Intercom</a></li>
                    <li><a href="research.html" class="mission-link ${activePage === 'research.html' ? 'active' : ''}">Research Pipeline</a></li>
                </ul>
                <div style="font-size: 0.6rem; color: #444; margin-top: 20px; border-top: 1px solid #222; padding-top: 5px;">
                    DEPLOYMENT: [MODULAR_V1.2]
                </div>
            </section>
        `;

        // Wait for DOM to be fully ready before attaching listeners
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initToggle());
        } else {
            this.initToggle();
        }
    }

    initToggle() {
        const menuToggle = document.getElementById('menu-toggle');
        const parentNav = document.getElementById('sidebar') || this.closest('nav');
        
        console.log("[MISSION CONTROL] Initializing toggle...");
        console.log("[MISSION CONTROL] Found menuToggle:", !!menuToggle);
        console.log("[MISSION CONTROL] Found parentNav:", !!parentNav);

        if (menuToggle && parentNav) {
            // Using addEventListener to avoid overwriting or being overwritten
            menuToggle.addEventListener('click', (e) => {
                console.log("[MISSION CONTROL] Toggle clicked via Component Listener.");
                parentNav.classList.toggle('active');
                e.stopPropagation();
            });

            // Global click handler to close sidebar on mobile
            document.addEventListener('click', (e) => {
                if (parentNav.classList.contains('active') && !parentNav.contains(e.target) && e.target !== menuToggle) {
                    console.log("[MISSION CONTROL] Closing sidebar via outside click.");
                    parentNav.classList.remove('active');
                }
            });
        } else {
            console.warn("[MISSION CONTROL] Required elements for hamburger NOT found.");
        }
    }
}

customElements.define('mission-control', MissionControl);