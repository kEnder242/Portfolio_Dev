class MissionControl extends HTMLElement {
    connectedCallback() {
        const currentPath = window.location.pathname;
        const activePage = currentPath.split('/').pop() || 'stories.html';

        console.log(`[MISSION CONTROL] Component connected (v1.3). Active page: ${activePage}`);

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
                    <li><a href="intercom.html" class="mission-link ${activePage === 'intercom.html' ? 'active' : ''}">AI Lab: Intercom</a></li>
                    <li><a href="research.html" class="mission-link ${activePage === 'research.html' ? 'active' : ''}">Research Pipeline</a></li>
                </ul>
                <div style="font-size: 0.6rem; color: #444; margin-top: 20px; border-top: 1px solid #222; padding-top: 5px;">
                    DEPLOYMENT: [MODULAR_V1.3]
                </div>
            </section>
        `;

        // Strategy: Use a tiny timeout + observer to ensure the rest of the DOM is ready
        // especially for pages where script is loaded in <head> or middle
        setTimeout(() => this.initToggle(), 50);
    }

    initToggle() {
        const menuToggle = document.getElementById('menu-toggle');
        const parentNav = document.getElementById('sidebar') || this.closest('nav');
        
        console.log("[MISSION CONTROL] Attempting toggle init...");

        if (menuToggle && parentNav) {
            console.log("[MISSION CONTROL] Elements found. Attaching listener.");
            // Remove any existing listeners by cloning (extreme measure for "authority")
            const newToggle = menuToggle.cloneNode(true);
            menuToggle.parentNode.replaceChild(newToggle, menuToggle);

            newToggle.addEventListener('click', (e) => {
                console.log("[MISSION CONTROL] Hamburger Clicked.");
                parentNav.classList.toggle('active');
                e.stopPropagation();
            });

            // Global click handler to close sidebar on mobile
            document.addEventListener('click', (e) => {
                if (parentNav.classList.contains('active') && !parentNav.contains(e.target) && e.target !== newToggle) {
                    parentNav.classList.remove('active');
                }
            });
        } else {
            console.warn("[MISSION CONTROL] Failed to find toggle or sidebar. Retrying...");
            // One-time retry
            if (!this._retried) {
                this._retried = true;
                setTimeout(() => this.initToggle(), 500);
            }
        }
    }
}

customElements.define('mission-control', MissionControl);
