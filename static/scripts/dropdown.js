var idSet = new Set();

function dropdownFunction(elementId) {
    document.getElementById(elementId).classList.toggle('show');
    idSet.add(elementId);
    let tempSet = new Set(idSet)
    tempSet.delete(elementId)
    tempSet.forEach(closeMenu)
}

function closeMenu(elementId) {
    let myDropdown = document.getElementById(elementId);
        if (myDropdown.classList.contains('show')) {
            myDropdown.classList.remove('show');
        }
}

window.onclick = function(e) {
    if (!e.target.matches('.dropbtn')) {
        idSet.forEach(closeMenu)
    }
}

//var idSet = new Set();
//var listOfMenus = ['main_dropdown', 'users_menu', 'timetable_menu', 'approve_changes_menu', 'pump_menu']
//
//function dropdownFunction(elementId) {
//    document.getElementById(elementId).classList.toggle('show');
//    idSet.add(elementId);
//    var tempSet = new Set(idSet);
//    tempSet.delete(elementId);
//    tempSet.forEach(closeMenu);
//}
//
//function closeMenu(elementId) {
//    var dropwdown = document.getElementById(elementId);
//    if (dropwdown.classList.contains('show')) {
//        dropwdown.classList.remove('show');
//    }
//}
//
//window.onclick = function(event) {
//    for (var dropdownId in listOfMenus) {
//        var dropdownMenu = document.getElementById(dropdownId);
//        if (event.target.contains(dropdownMenu) && event.target !== dropdownMenu) {
//            idSet.forEach(closeMenu)
//        }
//    }
//}
