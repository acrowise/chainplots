////////////////
////////////////
// FUNCTIONS
////////////////
////////////////
function printPixelChain(data) {
    var pixels = data.split("\n").map(Number);
    var canv = document.getElementById("mycanvas");
    var ctx = canv.getContext("2d");
    ctx.font = "12px Sans";
    ctx.fillStyle = "grey";
    ctx.strokeStyle="grey";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(39, 0);
    ctx.lineTo(39, 1000);
    ctx.stroke();
    // ctx.strokeRect(39,0,544,1000);
    ctx.fillText("500k",0,12);
    ctx.moveTo(33, 8);
    ctx.lineTo(39, 8);
    ctx.stroke();
    ctx.fillText("450k",0,111);
    ctx.moveTo(33, 107);
    ctx.lineTo(39, 107);
    ctx.stroke();
    ctx.fillText("400k",0,206);
    ctx.moveTo(33, 204);
    ctx.lineTo(39, 204);
    ctx.stroke();
    ctx.fillText("350k",0,306);
    ctx.moveTo(33, 302);
    ctx.lineTo(39, 302);
    ctx.stroke();
    ctx.fillText("300k",0,405);
    ctx.moveTo(33, 401);
    ctx.lineTo(39, 401);
    ctx.stroke();
    ctx.fillText("250k",0,504);
    ctx.rotate(-Math.PI/2);
    ctx.fillText("Block heigh",-485,10);
    ctx.rotate(Math.PI/2);
    ctx.moveTo(33, 500);
    ctx.lineTo(39, 500);
    ctx.stroke();
    ctx.fillText("200k",0,603);
    ctx.moveTo(33, 599);
    ctx.lineTo(39, 599);
    ctx.stroke();
    ctx.fillText("150k",0,703);
    ctx.moveTo(33, 699);
    ctx.lineTo(39, 699);
    ctx.stroke();
    ctx.fillText("100k",0,802);
    ctx.moveTo(33, 798);
    ctx.lineTo(39, 798);
    ctx.stroke();
    ctx.fillText("50k",7,901);
    ctx.moveTo(33, 897);
    ctx.lineTo(39, 897);
    ctx.stroke();
    for (var i = 0; i < pixels.length; i++) {

        var row = 999 - Math.floor(i / 504); // Start from the bottom
        var col = 40 + Math.floor(i % 504);
        var value = String(pixels[i] / django_range_max);

        var app_color = "43, 144, 143";
        var nice_color = "rgba(" + app_color + ", " + value + ")";
        ctx.fillStyle = nice_color;
        ctx.fillRect(col, row, 1, 1);
    }
    $('#spinner').hide();
    $('#mycanvas').show();
}

function printMultipixelChain(data) {

    var canv = document.getElementById("mycanvas");
    var ctx = canv.getContext("2d");
    ctx.font = "12px Sans";
    ctx.fillStyle = "grey";
    ctx.strokeStyle="grey";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(39, 0);
    ctx.lineTo(39, 1000);
    ctx.stroke();
    // ctx.strokeRect(39,0,544,1000);
    ctx.fillText("500k",0,12);
    ctx.moveTo(33, 8);
    ctx.lineTo(39, 8);
    ctx.stroke();
    ctx.fillText("450k",0,111);
    ctx.moveTo(33, 107);
    ctx.lineTo(39, 107);
    ctx.stroke();
    ctx.fillText("400k",0,206);
    ctx.moveTo(33, 204);
    ctx.lineTo(39, 204);
    ctx.stroke();
    ctx.fillText("350k",0,306);
    ctx.moveTo(33, 302);
    ctx.lineTo(39, 302);
    ctx.stroke();
    ctx.fillText("300k",0,405);
    ctx.moveTo(33, 401);
    ctx.lineTo(39, 401);
    ctx.stroke();
    ctx.fillText("250k",0,504);
    ctx.moveTo(33, 500);
    ctx.lineTo(39, 500);
    ctx.stroke();
    ctx.fillText("200k",0,603);
    ctx.moveTo(33, 599);
    ctx.lineTo(39, 599);
    ctx.stroke();
    ctx.fillText("150k",0,703);
    ctx.moveTo(33, 699);
    ctx.lineTo(39, 699);
    ctx.stroke();
    ctx.fillText("100k",0,802);
    ctx.moveTo(33, 798);
    ctx.lineTo(39, 798);
    ctx.stroke();
    ctx.fillText("50k",7,901);
    ctx.moveTo(33, 897);
    ctx.lineTo(39, 897);
    ctx.stroke();

    // Aquí generamos una array de arrays. 2d. Cada línea es un bloque.
    var data_array = data.split("\n").map(function f(item){return item.split(" ")});
    console.log(data_array);
    var app_data = [];
    var value = 0;
    var app_labels = [
        'Ascribe', 'Stampery', 'Factom', 'Open Assets', 'Blockstack',
        'Colu', 'Omni Layer', 'Unknown', 'Counterparty'
    ];

    var app_colors = [
            "43, 144, 143",
            "144, 238, 126",
            "244, 91, 91",
            "119, 152, 191",
            "170, 238, 238",
            "255, 0, 102",
            "238, 170, 238",
            "85, 191, 59"
        ];

    for (var i = 0; i < data_array.length; i++) {
        var data_line = data_array[i];
        var value = 0;
        var app_code = 0;
        for (var j = 0; j < 9; j++) {
            var data_value = data_line[j];
            if (data_value > value) {
                value = String(data_value / django_range_max);
                app_code = j;
            }
        }

        var row = 999 - Math.floor(i / 504); // Start from the bottom
        var col = 40 + Math.floor(i % 504);

        var nice_color = "rgba(" + app_colors[app_code] + ", " + value + ")";
        ctx.fillStyle = nice_color;
        ctx.fillRect(col, row, 1, 1);
    }
    $('#spinner').hide();
    $('#mycanvas').show();
}

function printLineGraph(data) {

    var points = data.split("\n").map(Number);

    Highcharts.chart('mychart', {
        chart: {
            type: 'area',
            inverted: true
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            reversed: false,
            title: {
                text: 'Block heigh'
            },
            allowDecimals: false,
            labels: {
                formatter: function () {
                    return this.value + 'K';
                }
            }
        },
        yAxis: {
            title: {
                text: django_line_param
            },
            labels: {
                formatter: function () {
                    return this.value + ' ' + django_units;
                }
            }
        },
        tooltip: {
            pointFormat: 'Point value: <b>{point.y:,.0f}</b>'
        },
        plotOptions: {
            area: {
                pointStart: 1,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [{
            name: django_line_param,
            data: points
        }]
    });
 
    $('#spinner').hide();
    $('#mychart').show();
}

function printMultilineGraph(data) {

    var lines_of_data = data.split("\n");
    var app_data = [];
    var app_labels = [
        'Ascribe', 'Stampery', 'Factom', 'Open Assets', 'Blockstack',
        'Colu', 'Omni Layer', 'Unknown', 'Counterparty'
    ];
    for (var i = 0; i < 9; i++) {
        var one_data = lines_of_data.map(
                function separador(item) {return Number(item.split(" ")[i])}
            )
        app_data.push(one_data);
    }

    Highcharts.chart('mychart', {
        chart: {
            type: 'area',
            inverted: true
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            reversed: false,
            title: {
                text: 'Block heigh'
            },
            allowDecimals: false,
            labels: {
                formatter: function () {
                    return this.value + 'K';
                }
            }
        },
        yAxis: {
            title: {
                text: app_labels[0],
                text: app_labels[1],
                text: app_labels[2],
                text: app_labels[3],
                text: app_labels[4],
                text: app_labels[5],
                text: app_labels[6],
                text: app_labels[7],
                text: app_labels[8],
            },
            labels: {
                formatter: function () {
                    return this.value + ' TX/s';
                }
            }
        },
        tooltip: {
            pointFormat: 'The throughput of the network was <b>{point.y:,.0f}</b> TX/s'
        },
        plotOptions: {
            area: {
                pointStart: 1,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [{
            name: app_labels[0],
            data: app_data[0]
        },{
            name: app_labels[1],
            data: app_data[1]
        },{
            name: app_labels[2],
            data: app_data[2]
        },{
            name: app_labels[3],
            data: app_data[3]
        },{
            name: app_labels[4],
            data: app_data[4]
        },{
            name: app_labels[5],
            data: app_data[5]
        },{
            name: app_labels[6],
            data: app_data[6]
        },{
            name: app_labels[7],
            data: app_data[7]
        },{
            name: app_labels[8],
            data: app_data[8]
        }]
    });
 
    $('#spinner').hide();
    $('#mychart').show();

}


///////////////
// HANDLERS 
///////////////
console.log($('#graphswitch').val());
var pixels_done = false;
var line_done = false;
$('#graphswitch').change(function(){
    $('#mycanvas').hide();
    $('#mychart').hide();
    $('#pixelinfo').hide();
    $('#lineinfo').hide();
    $('#spinner').show();

    var selection = $('input[name=options]:checked').val();

    if (selection == "line"){
        if(!line_done){
            $.get("/static/data/" + django_plot + "_1000", function(data, status) {
                console.log("Plot: " + django_plot + ". Status: " + status);
                if(django_plot == 'plot10'){
                    printMultilineGraph(data);
                } else {
                    printLineGraph(data);
                }
                line_done = true;
            });
        } else {
            $('#spinner').hide();
            $('#mychart').show();
        }
        $('#pixelinfo').hide();
        $('#lineinfo').show();
    } else if (selection == "pixels") {
        if(!pixels_done){
            $.get("/static/data/" + django_plot, function(data, status) {
                if(django_plot == 'plot10'){
                    printMultipixelChain(data);
                } else {
                    printPixelChain(data);
                }
                pixels_done = true;
            });
        } else {
            $('#spinner').hide();
            $('#mycanvas').show();
        }
        $('#pixelinfo').show();
        $('#lineinfo').hide();
    } else {
        alert("AN ERROR AT SWITCH!")
    }
});


////////////////
// STARTER
////////////////

$('#graphswitch').change();