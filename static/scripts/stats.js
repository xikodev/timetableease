function showStats() {
    fetch('temp.json')
    .then((response) => response.json())
    .then((data) => document.getElementById('professor-stats').innerHTML = data);
}
