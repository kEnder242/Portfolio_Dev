document.addEventListener('DOMContentLoaded', () => {
    // 1. Load Search Index
    let searchIndex = {};
    fetch('search_index.json?v=3.0')
        .then(response => response.json())
        .then(data => {
            searchIndex = data;
            console.log("Search Index Loaded:", Object.keys(data).length, "keys");
        })
        .catch(err => console.error('Error loading search index:', err));

    // 2. Quick Filter
    const searchInput = document.getElementById('nav-filter');
    const searchableContainer = document.getElementById('searchable-content');
    
    if (searchInput && searchableContainer) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase().trim();
            
            // Find ID matches from the index AND story bodies
            let matchedIds = new Set();
            
            if (term) {
                // A. Check Search Index
                Object.keys(searchIndex).forEach(key => {
                    if (key.includes(term)) {
                        searchIndex[key].forEach(id => matchedIds.add(id));
                    }
                });

                // B. Check Article Bodies (The "Surgical" Search)
                document.querySelectorAll('article').forEach(art => {
                    if (art.textContent.toLowerCase().includes(term)) {
                        matchedIds.add(art.id);
                    }
                });
            }
            
            // Filter Sidebar Lists
            const sections = searchableContainer.querySelectorAll('ul');
            sections.forEach(list => {
                const items = list.querySelectorAll('li');
                let hasVisibleItems = false;
                
                items.forEach(item => {
                    const link = item.querySelector('a');
                    const text = item.textContent.toLowerCase();
                    const href = link ? link.getAttribute('href') : '';
                    const id = href.startsWith('#') ? href.substring(1) : '';

                    const isVisible = (term === '' || text.includes(term) || matchedIds.has(id));
                    item.style.display = isVisible ? '' : 'none';
                    if (isVisible) hasVisibleItems = true;
                });

                // Hide the preceding header (H2) if no items match
                const header = list.previousElementSibling;
                if (header && header.tagName === 'H2') {
                    header.style.display = hasVisibleItems ? '' : 'none';
                }
            });
        });
    }

    // 3. Permalink Anchors
    const articles = document.querySelectorAll('article');
    articles.forEach(article => {
        const id = article.id;
        const heading = article.querySelector('h3');
        if (id && heading) {
            const anchor = document.createElement('a');
            anchor.href = '#' + id;
            anchor.className = 'permalink';
            anchor.textContent = '#';
            anchor.ariaLabel = 'Permalink to this section';
            heading.appendChild(anchor);
        }
    });

    // 4. Mobile Menu Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const nav = document.getElementById('sidebar');

    if (menuToggle && nav) {
        menuToggle.addEventListener('click', () => {
            nav.classList.toggle('active');
        });

        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    nav.classList.remove('active');
                }
            });
        });

        document.querySelector('main').addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                nav.classList.remove('active');
            }
        });
    }
});