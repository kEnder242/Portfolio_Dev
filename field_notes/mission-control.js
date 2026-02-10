class MissionControl extends HTMLElement {
    connectedCallback() {
        const currentPath = window.location.pathname;
        const activePage = currentPath.split('/').pop() || 'stories.html';

        // --- DEBUG FLAIR: IDENTIFY GHOST SIDEBARS ---
        // If there is a <nav id="sidebar"> that DOES NOT contain this element,
        // it's an old hardcoded sidebar. Turn it RED.
        const allSidebars = document.querySelectorAll('#sidebar');
        allSidebars.forEach(sb => {
            if (!sb.contains(this)) {
                sb.style.border = "5px solid #ff3b30";
                sb.style.boxShadow = "0 0 20px #ff3b30";
                const debugTag = document.createElement('div');
                debugTag.style.cssText = "background: #ff3b30; color: white; padding: 5px; font-weight: bold; position: absolute; top: 0; left: 0; z-index: 9999;";
                debugTag.textContent = "[!] OLD HARDCODED SIDEBAR DETECTED";
                sb.appendChild(debugTag);
            }
        });

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
                    DEPLOYMENT: [MODULAR_V1.1]
                </div>
            </section>
        `;

        // Mobile menu logic: reach out to the parent nav
        const menuToggle = document.getElementById('menu-toggle');
        const parentNav = document.getElementById('sidebar') || this.closest('nav');
        
        if (menuToggle && parentNav) {
            menuToggle.onclick = (e) => { 
                console.log("[DEBUG] Hamburger clicked. Toggling sidebar.");
                parentNav.classList.toggle('active'); 
                e.stopPropagation(); 
            };
            
            // Close sidebar when clicking outside on mobile
            document.addEventListener('click', (e) => {
                if (parentNav.classList.contains('active') && !parentNav.contains(e.target) && e.target !== menuToggle) {
                    parentNav.classList.remove('active');
                }
            });
        }
    }
}

customElements.define('mission-control', MissionControl);
