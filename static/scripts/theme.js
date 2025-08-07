var setTheme = localStorage.getItem('theme');

if (setTheme == null) {
    loadMode('light');
} else {
    loadMode(setTheme);
}

function loadMode(theme) {
    var names = ['style', 'header', 'navbar', 'table', 'form', 'settings'];
    var location = '/static/css/' + theme + '/';
    for (var name in names) {
        document.getElementById('css_' + names[name]).href = location + names[name] + '.css';
    }
}

function switchMode() {
    var currentTheme = localStorage.getItem('theme');
    var new_theme;

    if (currentTheme === 'light') {
        new_theme = 'dark';
    } else {
        new_theme = 'light';
    }

    var names = ['style', 'header', 'navbar', 'table', 'form', 'settings'];
    var location = '/static/css/' + new_theme + '/';
    for (var name in names) {
        document.getElementById('css_' + names[name]).href = location + names[name] + '.css';
    }
    localStorage.setItem('theme', new_theme);
}
