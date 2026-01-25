document.addEventListener('DOMContentLoaded', () => {
    // 1. Load Search Index
    let searchIndex = {};
    fetch('search_index.json')
        .then(response => response.json())
        .then(data => {
            searchIndex = data;
        })
        .catch(err => console.error('Error loading search index:', err));

    // 2. Quick Filter
    const searchInput = document.getElementById('nav-filter');
    const navLists = document.querySelectorAll('nav ul');
    
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase().trim();
        
        // Find ID matches from the index
        let matchedIds = new Set();
        if (term && searchIndex[term]) {
            searchIndex[term].forEach(id => matchedIds.add(id));
        }

        // Also check if the term partially matches any index keys (fuzzy-ish)
        if (term) {
            Object.keys(searchIndex).forEach(key => {
                if (key.includes(term)) {
                    searchIndex[key].forEach(id => matchedIds.add(id));
                }
            });
        }
        
        navLists.forEach(list => {
            const items = list.querySelectorAll('li');
            let hasVisibleItems = false;
            
            items.forEach(item => {
                const link = item.querySelector('a');
                const text = item.textContent.toLowerCase();
                const href = link ? link.getAttribute('href') : '';
                const id = href.startsWith('#') ? href.substring(1) : '';

                // Visible if:
                // 1. Text matches term
                // 2. ID is in the matched set from JSON index
                if (text.includes(term) || matchedIds.has(id)) {
                    item.style.display = '';
                    hasVisibleItems = true;
                } else {
                    item.style.display = 'none';
                }
            });

            // Hide headers if no items are visible in that section
            const prevHeader = list.previousElementSibling;
            if (prevHeader && (prevHeader.tagName === 'H2')) {
                prevHeader.style.display = hasVisibleItems || term === '' ? '' : 'none';
            }
        });
    });

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

        // Close menu when clicking a link (optional UX improvement)
        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    nav.classList.remove('active');
                }
            });
        });

        // Close when clicking outside (on main content)
        document.querySelector('main').addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                nav.classList.remove('active');
            }
        });
    }
});
