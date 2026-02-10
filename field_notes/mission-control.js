class MissionControl extends HTMLElement {
    connectedCallback() {
        const currentPath = window.location.pathname;
        const activePage = currentPath.split('/').pop() || 'stories.html';

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
                    
                    <li><a href="https://code.jason-lab.dev" target="_blank" class="mission-link">VS Code (Remote)</a></li>
                </ul>
            </section>
        `;

        // Mobile menu logic: reach out to the parent nav
        const menuToggle = document.getElementById('menu-toggle');
        const parentNav = this.closest('nav') || document.getElementById('sidebar');
        
        if (menuToggle && parentNav) {
            menuToggle.onclick = (e) => { 
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