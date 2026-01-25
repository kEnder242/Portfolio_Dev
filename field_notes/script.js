document.addEventListener('DOMContentLoaded', () => {
    // 1. Quick Filter
    const searchInput = document.getElementById('nav-filter');
    // Select all list items in the nav, but exclude the Mission Control links if we want them to always stay visible,
    // or include them. Let's include all for now, but maybe we want to keep headers visible?
    // A simple approach: filter LI elements.
    const navLists = document.querySelectorAll('nav ul');
    
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        
        navLists.forEach(list => {
            const items = list.querySelectorAll('li');
            let hasVisibleItems = false;
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(term)) {
                    item.style.display = '';
                    hasVisibleItems = true;
                } else {
                    item.style.display = 'none';
                }
            });

            // Optional: Hide headers if no items are visible in that section
            // This requires the H2 to be associated with the UL. 
            // Given the HTML structure (H2 followed by UL), we can try:
            const prevHeader = list.previousElementSibling;
            if (prevHeader && prevHeader.tagName === 'H2') {
                prevHeader.style.display = hasVisibleItems || term === '' ? '' : 'none';
            }
        });
    });

    // 2. Permalink Anchors
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
            
            // Add click listener to smooth scroll (optional, default browser behavior is usually fine)
            // But we specifically want it to update URL
            
            heading.appendChild(anchor);
        }
    });
});
