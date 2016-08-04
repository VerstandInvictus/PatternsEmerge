var $overlay = $('<div class=overlay></div>')
var $listContainer = $('<div class=centeredList></div>')

var themes = {
  "sunburst": {
      "charts": {
        "background": "#11111b",
        "text": "white",
        "tooltipheader": "linear-gradient(to right, #8400ea 0%,#ce16c8 51%,#fc5c00 100%)"
      },
      "page": {
        "background": "#333340",
        "header": "linear-gradient(to right, #8400ea 0%,#ce16c8 51%,#fc5c00 100%)",
        "headertext": "#ddd",
        "subheader": "#ddd",
        "button": "#8d0e36"
      }
  },
  "deepblue": {
      "charts": {
        "background": "#11111b",
        "text": "white",
        "tooltipheader": "linear-gradient(to right, #8400ea 0%,#137cb5 53%,#17b8d8 100%)"
      },
      "page": {
        "background": "#333340",
        "header": "linear-gradient(to right, #8400ea 0%,#137cb5 53%,#17b8d8 100%)",
        "headertext": "#ddd",
        "subheader": "#ddd",
        "button": "#148abd"
      }
  },
  "hprographics": {
      "charts": {
        "background": "#f2f6f8",
        "text": "black",
        "tooltipheader": "#5c0029"
      },
      "page": {
        "background": "#383f51",
        "header": "#5c0029",
        "headertext": "#ddd",
        "subheader": "#e2d4b7",
        "button": "#00b300"
      }
  }
}

function updatePageColors (theme) {
    $("body").css("background", theme.page.background);
    $(".chartHeader").css("background", theme.page.header);
    $(".logoHeader").css("background", theme.page.header);
    $("p .instructions").css("background", theme.page.subheader);
    $(".submit").css("background", theme.page.button);
};

function updateChartColors (theme) {
    $(".barChart").css("background", theme.charts.background);
    $(".tick text").css("fill", theme.charts.text);
    $(document.head).append('<style>.c3-tooltip-container th{background: ' + theme.charts.tooltipheader +  ';}</style>')
    loadData();
}


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
        loadData(gradient);
        $("#updated").show();
        $("#updatedwait").hide();
    });
});

function loadData () {
    $.getJSON(apiRoot + 'oapl/open12-6/' + gradient, function (data) {
        $('#oaplload').hide();
        oapldata = data
        oaplchart = chartgen(oapldata, "#oaplchart", 200)
    });

    $.getJSON(apiRoot + 'list/open12-6/' + gradient, function (data) {
        $('#tradesload').hide();
        tradesdata = data
        tradeschart = chartgen(tradesdata, "#tradeschart", 150)
    });

    $.getJSON(apiRoot + 'totals/open12-6/' + gradient, function (data) {
        var format = d3.format('$,');
        $.each(data, function(i) {
            $("#" + i).text(data[i][0]);
            $("#" + i).parent().css({backgroundColor:data[i][1]})
        })
        $(".pct").append("%")
        $(".dol").prepend("$")
    });
}

gradient = 'hprographics']
updatePageColors(themes[gradient]);
updateChartColors(themes[gradient]);
