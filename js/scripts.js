function showTab(region) {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    contents.forEach(content => content.classList.remove('active'));
    document.getElementById(region).classList.add('active');
    document.getElementById(`${region}-tab`).classList.add('active');
}
