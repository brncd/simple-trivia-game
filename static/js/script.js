document.addEventListener('DOMContentLoaded', function () {
    // Reload page on refresh
    if (performance.navigation.type === 1) {
        window.location.replace('/');
    }

    // Reload page on back button
    if (performance.navigation.type === 2) {
        window.location.replace('/');
    }
});