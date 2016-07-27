var $overlay = $('<div class=overlay></div>')
var $listContainer = $('<div class=centeredList></div>')


function chartgen (dataobj, bind, type) {
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
                return d.id ? dataobj[d.index]['color'] : color;
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
        },
        legend: {
            show: false
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
    oaplchart = chartgen(oapldata, "#oaplchart", 'area')
});

$.getJSON(apiRoot + 'list/open12-6', function (data) {
    $('#tradesload').hide();
    tradesdata = data
    tradeschart = chartgen(tradesdata, "#tradeschart", 'bar')
});
