(function () {
  "use strict";
  $.ajax({
    url: '/update',
    success: function (data) {
      var labels = data.time;
      createChart('#temp-chart', 'Температура', labels, data.temp, '#0fad32');
      createChart('#humidity-chart', 'Влажность', labels, data.humidity, '#4d83ff');
      createChart('#smoke-chart', 'Концентрация газов', labels, data.smoke, '#ffc100');
      createChart('#co-chart', 'Концентрация C02', labels, data.co, '#ff4747')
    }
  });
})(jQuery);

function createChart(chart, label, labels, data, color) {
  if ($(chart).length) {
    var ctx = $(chart).get(0).getContext("2d");
    var data = {
      labels: labels,
      datasets: [
        {
          label: label,
          data: data,
          borderColor: [
            color
          ],
          borderWidth: 2,
          fill: false,
          pointBackgroundColor: "#fff"
        }
      ]
    };
    var options = {
      scales: {
        yAxes: [{
          display: true,
          gridLines: {
            drawBorder: false,
            lineWidth: 1,
            color: "#e9e9e9",
            zeroLineColor: "#e9e9e9",
          },
          ticks: {
            min: 0,
            max: 100,
            stepSize: 20,
            fontColor: "#6c7383",
            fontSize: 16,
            fontStyle: 300,
            padding: 15
          }
        }],
        xAxes: [{
          display: true,
          gridLines: {
            drawBorder: false,
            lineWidth: 1,
            color: "#e9e9e9",
          },
          ticks: {
            fontColor: "#6c7383",
            fontSize: 16,
            fontStyle: 300,
            padding: 15
          }
        }]
      },
      legend: {
        display: false
      },
      elements: {
        point: {
          radius: 3
        },
        line: {
          tension: 0
        }
      },
      stepsize: 1,
      layout: {
        padding: {
          top: 0,
          bottom: -10,
          left: -10,
          right: 0
        }
      }
    };
    var cashDeposits = new Chart(ctx, {
      type: 'line',
      data: data,
      options: options
    });
  }
};