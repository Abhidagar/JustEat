// Filter Tabs JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Filter tabs script loaded'); // Debug log
    
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.filter-tab-btn');
    const tabContents = document.querySelectorAll('.filter-tab-content');
    
    console.log('Found tab buttons:', tabButtons.length); // Debug log
    console.log('Found tab contents:', tabContents.length); // Debug log
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
    
    // Filter option selection
    const filterOptions = document.querySelectorAll('.filter-option');
    filterOptions.forEach(option => {
        option.addEventListener('click', function() {
            const checkbox = this.querySelector('input[type="checkbox"]');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
                this.classList.toggle('selected', checkbox.checked);
                updateFilterCount();
            }
        });
        
        // Prevent double-toggle when clicking checkbox directly
        const checkbox = option.querySelector('input[type="checkbox"]');
        if (checkbox) {
            checkbox.addEventListener('click', function(e) {
                e.stopPropagation();
                option.classList.toggle('selected', this.checked);
                updateFilterCount();
            });
        }
    });
    
    // Price range inputs
    const priceInputs = document.querySelectorAll('.price-range-input input');
    priceInputs.forEach(input => {
        input.addEventListener('input', updateFilterCount);
    });
    
    // Apply filters button
    const applyFiltersBtn = document.getElementById('apply-filters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            applyFilters();
        });
    }
    
    // Clear filters button
    const clearFiltersBtn = document.getElementById('clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            clearAllFilters();
        });
    }
    
    // Toggle filter visibility
    const filterToggle = document.getElementById('filter-toggle');
    const filterTabs = document.getElementById('filter-tabs');
    
    if (filterToggle && filterTabs) {
        filterToggle.addEventListener('click', function() {
            if (filterTabs.style.display === 'none') {
                filterTabs.style.display = 'block';
                this.innerHTML = '<i class="bi bi-funnel"></i> Hide Filters <span id="filter-count-badge" class="badge bg-danger ms-1" style="display: none;">0</span>';
            } else {
                filterTabs.style.display = 'none';  
                this.innerHTML = '<i class="bi bi-funnel"></i> Show Filters <span id="filter-count-badge" class="badge bg-danger ms-1" style="display: none;">0</span>';
            }
        });
    }
    
    function updateFilterCount() {
        const selectedCuisines = document.querySelectorAll('input[name="cuisine"]:checked').length;
        const selectedRestaurants = document.querySelectorAll('input[name="restaurant"]:checked').length;
        const priceMin = document.getElementById('price-min')?.value;
        const priceMax = document.getElementById('price-max')?.value;
        
        let totalFilters = selectedCuisines + selectedRestaurants;
        if (priceMin || priceMax) totalFilters++;
        
        const badge = document.getElementById('filter-count-badge');
        if (badge) {
            badge.textContent = totalFilters;
            badge.style.display = totalFilters > 0 ? 'inline-block' : 'none';
        }
        
        console.log('Filter count updated:', totalFilters); // Debug log
    }
    
    function applyFilters() {
        const form = document.getElementById('filter-form');
        if (!form) return;
        
        const formData = new FormData(form);
        const params = new URLSearchParams();
        
        // Add search query if it exists
        const searchQuery = document.querySelector('input[name="q"]')?.value;
        if (searchQuery) {
            params.append('q', searchQuery);
        }
        
        // Add selected filters
        for (let [key, value] of formData.entries()) {
            if (value) {
                params.append(key, value);
            }
        }
        
        // Navigate to search with filters
        window.location.href = `/search?${params.toString()}`;
    }
    
    function clearAllFilters() {
        // Clear all checkboxes
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Clear price inputs
        document.querySelectorAll('.price-range-input input').forEach(input => {
            input.value = '';
        });
        
        // Remove selected classes
        document.querySelectorAll('.filter-option.selected').forEach(option => {
            option.classList.remove('selected');
        });
        
        updateFilterCount();
        
        // Navigate to search without filters
        const searchQuery = document.querySelector('input[name="q"]')?.value;
        const queryParam = searchQuery ? `?q=${encodeURIComponent(searchQuery)}` : '';
        window.location.href = `/search${queryParam}`;
    }
    
    // Initialize filter count on page load
    updateFilterCount();
    
    // Price range validation
    const priceMinInput = document.getElementById('price-min');
    const priceMaxInput = document.getElementById('price-max');
    
    function validatePriceRange() {
        if (!priceMinInput || !priceMaxInput) return;
        
        const minValue = parseFloat(priceMinInput.value) || 0;
        const maxValue = parseFloat(priceMaxInput.value) || Infinity;
        
        if (minValue > maxValue && maxValue !== Infinity) {
            priceMaxInput.setCustomValidity('Maximum price must be greater than minimum price');
        } else {
            priceMaxInput.setCustomValidity('');
        }
    }
    
    if (priceMinInput && priceMaxInput) {
        priceMinInput.addEventListener('input', validatePriceRange);
        priceMaxInput.addEventListener('input', validatePriceRange);
    }
});
