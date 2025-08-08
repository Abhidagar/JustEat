// Filter Sidebar Functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Filter sidebar script loaded');
    
    const filterToggleBtn = document.getElementById('filter-toggle-btn');
    const filterSidebar = document.getElementById('filter-sidebar');
    const filterOverlay = document.getElementById('filter-sidebar-overlay');
    const filterCloseBtn = document.getElementById('filter-close-btn');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const clearFiltersBtn = document.getElementById('clear-filters');
    const filterForm = document.getElementById('filter-form');
    const filterCountBadge = document.getElementById('filter-count-badge');

    // Open sidebar
    if (filterToggleBtn) {
        filterToggleBtn.addEventListener('click', function() {
            console.log('Filter toggle clicked');
            openFilterSidebar();
        });
    }

    // Close sidebar
    if (filterCloseBtn) {
        filterCloseBtn.addEventListener('click', closeFilterSidebar);
    }
    
    if (filterOverlay) {
        filterOverlay.addEventListener('click', closeFilterSidebar);
    }

    // Apply filters
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            console.log('Apply filters clicked');
            applyFilters();
        });
    }

    // Clear filters
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            console.log('Clear filters clicked');
            clearAllFilters();
        });
    }

    // Update filter count and option states
    if (filterForm) {
        filterForm.addEventListener('change', function() {
            updateFilterCount();
            updateFilterOptionStates();
        });
    }

    // Handle filter option clicks
    document.addEventListener('click', function(e) {
        if (e.target.closest('.filter-option')) {
            const option = e.target.closest('.filter-option');
            const checkbox = option.querySelector('input[type="checkbox"]');
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
                updateFilterOptionStates();
                updateFilterCount();
            }
        }
    });

    // Initialize
    updateFilterCount();
    updateFilterOptionStates();

    function openFilterSidebar() {
        if (filterSidebar && filterOverlay) {
            filterSidebar.classList.add('active');
            filterOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeFilterSidebar() {
        if (filterSidebar && filterOverlay) {
            filterSidebar.classList.remove('active');
            filterOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    function applyFilters() {
        if (!filterForm) return;

        const formData = new FormData(filterForm);
        const params = new URLSearchParams();

        // Add cuisine filters
        const cuisines = formData.getAll('cuisine');
        cuisines.forEach(cuisine => params.append('cuisine', cuisine));

        // Add restaurant filters
        const restaurants = formData.getAll('restaurant');
        restaurants.forEach(restaurant => params.append('restaurant', restaurant));

        // Add price filters
        const priceMin = formData.get('price_min');
        const priceMax = formData.get('price_max');
        if (priceMin) params.append('price_min', priceMin);
        if (priceMax) params.append('price_max', priceMax);

        // Navigate to home page with filters
        const currentUrl = new URL(window.location);
        currentUrl.search = params.toString();
        
        console.log('Applying filters:', params.toString());
        window.location.href = currentUrl.toString();
    }

    function clearAllFilters() {
        if (!filterForm) return;

        // Clear all checkboxes
        const checkboxes = filterForm.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

        // Clear price inputs
        const priceInputs = filterForm.querySelectorAll('input[type="number"]');
        priceInputs.forEach(input => {
            input.value = '';
        });

        updateFilterCount();
        updateFilterOptionStates();

        // Navigate to home page without filters
        window.location.href = window.location.pathname;
    }

    function updateFilterCount() {
        if (!filterForm || !filterCountBadge) return;

        let count = 0;

        // Count checked checkboxes
        const checkedBoxes = filterForm.querySelectorAll('input[type="checkbox"]:checked');
        count += checkedBoxes.length;

        // Count price filters
        const priceMin = filterForm.querySelector('input[name="price_min"]');
        const priceMax = filterForm.querySelector('input[name="price_max"]');
        if (priceMin && priceMin.value) count++;
        if (priceMax && priceMax.value) count++;

        if (count > 0) {
            filterCountBadge.textContent = count;
            filterCountBadge.style.display = 'inline';
        } else {
            filterCountBadge.style.display = 'none';
        }
    }

    function updateFilterOptionStates() {
        const options = document.querySelectorAll('.filter-option');
        options.forEach(option => {
            const checkbox = option.querySelector('input[type="checkbox"]');
            if (checkbox) {
                if (checkbox.checked) {
                    option.classList.add('selected');
                } else {
                    option.classList.remove('selected');
                }
            }
        });
    }

    // Close sidebar on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeFilterSidebar();
        }
    });
});
