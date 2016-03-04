//var tables = document.getElementsByTagName('table');
//
//for (var i = 0; i < tables.length; i++) {
//  tables[i].className += ' tablesorter';
//}
$('table').addClass('tablesorter');

$(document).ready(function(){
    $('.user-list').DataTable();
});
