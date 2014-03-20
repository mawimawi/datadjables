var resizetimer = null;
var calcDataTableHeight = function(dt) {
    return window.innerHeight - $('.django-datadjable').offset().top - 105;
};

var adjust_to_screen = function() {
    $(".django-datadjable").each( function() {
        oTable = $("#" + $(this).data('id')).dataTable();
        var oSettings = oTable.fnSettings();
        oSettings.oScroll.sY = calcDataTableHeight(oTable);
        oTable.fnDraw();
    });
};

$(window).resize(function () {
    if (resizetimer !== null) { window.clearTimeout(resizetimer); }
    // it is necessary to wait a bit until the browser has finished redrawing...
    resizetimer = window.setTimeout("adjust_to_screen()", 300);
});

function init_datatable(dt, dt_aoColumns, dt_aaSorting, dt_columnfilter){
    $.datepicker.regional[""].dateFormat = 'yy-mm-dd';
    $.datepicker.setDefaults($.datepicker.regional['']);
    $.datepicker.setDefaults({
      changeMonth: true,
      changeYear: true,
      yearRange: "-50:+50"});

    var oTable = $('#' + dt.data("id")).dataTable({
//      'sPaginationType': 'full_numbers',
    'iDisplayLength': 50,
    "bServerSide": true,
//    "bScrollInfinite": true,
//    "bScrollCollapse": true,
    "sScrollY": calcDataTableHeight(dt),
    "sAjaxSource": "",
    "sDom": "tSi",
    "oScroller": {
      "loadingIndicator": false
    },
//    "bDeferRender": true,
//    "aoColumns": dt_aoColumns,
//    'aaSorting': dt_aaSorting,
    "oLanguage": {
      "sProcessing":   "Bitte warten...",
      "sLengthMenu":   "_MENU_ Einträge anzeigen",
      "sZeroRecords":  "Keine Einträge vorhanden.",
      "sInfo":         "_START_ bis _END_ von _TOTAL_ Einträgen",
      "sInfoEmpty":    "0 bis 0 von 0 Einträgen",
      "sInfoFiltered": "(gefiltert von _MAX_  Einträgen)",
      "sSearch":       "Suchen"
    }
  }).columnFilter({aoColumns: dt_columnfilter});
    dt.addClass('initialized');
}

function dt_init() {
    $(".django-datadjable").each( function() {
        var dt_id = this.id;
        var dt = $('#' + dt_id);
        if(!dt.hasClass('initialized')){ // prevent multiple inits via history.back
            init_datatable(dt, dt.data('columns'), dt.data('sorting'), dt.data('columnfilter'));
        }
    });
}

$(document).ready( function() {
  dt_init();
});
