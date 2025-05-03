function showTab(region) {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    contents.forEach(content => content.classList.remove('active'));

    // Add 'active' class to the selected tab button and its content
    document.getElementById(`${region}-tab`).classList.add('active');
    document.getElementById(region).classList.add('active');
}

// Set default tab content to be visible on load
window.onload = function() {
    // Dynamically select the first tab and show it
    const firstTab = document.querySelector('.tab');
    if (firstTab) {
        const region = firstTab.id.replace('-tab', '');
        showTab(region);
    }
};
