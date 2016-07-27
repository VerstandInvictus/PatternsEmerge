var $overlay = $('<div class=overlay></div>')
var $listContainer = $('<div class=centeredList></div>')


function chartgen (dataobj, bind) {
    c3.generate({
        bindto: bind,
        data: {
            json: dataobj,
            type: 'bar',
            xFormat: "%mm %m",
            keys: {
                x: 'date',
                value: ['total'],
            },
            color: function (color, d) {
                if(d.value > 50) {
                    return "#ff0000";
                } else {
                return "#00ff00";
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
                type: 'timeseries'
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

$.getJSON(apiRoot + 'list/open12-6', function (data) {
    $('#oaplload').hide();
    oapldata = data
    oaplchart = chartgen(oapldata, "#oaplchart")
});
