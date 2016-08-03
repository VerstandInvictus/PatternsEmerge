var $overlay = $('<div class=overlay></div>')
var $listContainer = $('<div class=centeredList></div>')

$("#updatedwait").hide();

function chartgen (dataobj, bind, height) {
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
        axis: {
            x: {
                type: 'category',
                show: false
            }
        },
        legend: {
            show: false
        },
        size: {
            height: height
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

$("#updated").click(function() {
    $("#updated").hide();
    $("#updatedwait").show();
    $.getJSON(apiRoot + 'update/open12-6', function(data) {
        console.log(data);
        location.reload(true);
    });
});

$.getJSON(apiRoot + 'oapl/open12-6', function (data) {
    $('#oaplload').hide();
    oapldata = data
    oaplchart = chartgen(oapldata, "#oaplchart", 200)
});

$.getJSON(apiRoot + 'list/open12-6', function (data) {
    $('#tradesload').hide();
    tradesdata = data
    tradeschart = chartgen(tradesdata, "#tradeschart", 150)
});

$.getJSON(apiRoot + 'totals/open12-6', function (data) {
    var format = d3.format('$,');
    $.each(data, function(i) {
        $("#" + i).text(data[i][0]);
        $("#" + i).parent().css({backgroundColor:data[i][1]})
    })
    $(".pct").append("%")
    $(".dol").prepend("$")
});
