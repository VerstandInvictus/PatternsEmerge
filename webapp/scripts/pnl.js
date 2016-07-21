var $overlay = $('<div class=overlay></div>')
var $listContainer = $('<div class=centeredList></div>')


function chartgenrfc (dataobj, bind) {
    c3.generate({
        bindto: bind,
        data: {
            rows: dataobj.rows,
            type: 'bar',
            groups: [dataobj.groups],
            order: null,
            labels: true,
            onmouseover: function () {
                $(".c3-bar").css("fill-opacity", 0.5);
                $(".c3-bar._expanded_").css("fill-opacity", 1);
            },
            onmouseout: function () {
                $('.c3-bar').css("fill-opacity", 1);
            },
        },
        color: {
            pattern: colors
        },
        axis: {
            rotated: false,
            x: {
                type: 'category',
                categories: dataobj.categories
            },
            y: {
                show: false
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
        }
    })
};

$.ajaxSetup({
    xhrFields: {
        withCredentials: true
    },
    dataType: "json"
});

$.getJSON(apiRoot + 'reports/oapl', function
(data) {
    $('#sfcload').hide();
    oapldata = data
    oaplchart = chartgen(oapldata, "oapl", "#oaplchart")
});
