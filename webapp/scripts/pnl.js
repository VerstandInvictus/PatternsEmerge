var $overlay = $('<div class=overlay></div>')
var $listContainer = $('<div class=centeredList></div>')


function chartgen (dataobj, bind) {
    c3.generate({
        bindto: bind,
        data: {
            json: dataobj,
            type: 'bar',
            xFormat: null,
            keys: {
                x: 'date',
                value: ['total'],
            },
            color: function (color, d) {
                if(d.value > 0 ) {
                    return "#009933";
                } else {
                    return "#990000";
                }
            }
        },
        legend: {
            position: 'bottom',
            item: {
                onmouseover: function (d) {
                    var d2 = d.replace(/ /g, '-')
                    var whatlabel = ".c3-texts-" + d2 + ' text';
                    $(whatlabel).css("display", "inline")
                },
                onmouseout: function (d) {
                    var d2 = d.replace(/ /g, '-')
                    var whatlabel = ".c3-texts-" + d2 + ' text';
                    $(whatlabel).css("display", "none")
                }
            }
        },
        axis: {
            x: {
                type: 'category'
            }
        }
    })
    console.log('generated')
};

$.ajaxSetup({
    xhrFields: {
        withCredentials: true
    },
    dataType: "json"
});

$.getJSON(apiRoot + 'oapl/open12-6', function (data) {
    $('#oaplload').hide();
    oapldata = data
    oaplchart = chartgen(oapldata, "#oaplchart")
});
