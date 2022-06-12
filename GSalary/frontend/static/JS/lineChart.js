//Reference: https://www.youtube.com/watch?v=JkAZJAYAxmY

function createLineChart(urlSalary) {
  fetch(urlSalary)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let labels = ["0k"];
      let datatest = [0];

      data["by_range"].forEach((element) => {
        let salaryKey = Object.keys(element)[0];
        let countValue = element[Object.keys(element)[1]];
        labels.push(salaryKey);
        datatest.push(countValue);
      });
      insertData(labels, datatest);
      const loader3 = document.querySelector(".loader3");
      loader3.style.display = "none";
      const myChart = document.querySelector("#myChart");
      myChart.style.display = "block";
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : insertDataToBars()"
      );
    });
}

// ====================================
function insertData(labels, datatest) {
  let finalData = {
    labels: labels,
    datasets: [
      {
        label: "The number of job posts",
        backgroundColor: (context) => {
          // object destructuring
          const chart = context.chart;
          const { ctx, chartArea, scales } = chart;
          if (!chartArea) return null; // this is to avoid the animation isn't working during loading time.
          return bgGradient(ctx, chartArea, scales);
        },
        borderColor: "rgb(255, 99, 132, 1)",
        pointStyle: "star",
        pointRadius: 12,
        pointHoverRadius: 10,
        tension: 0.1,
        fill: true,
        data: datatest,
      },
    ],
  };
  const config = {
    type: "line",
    data: finalData,
    options: {
      scales: {
        x: {
          ticks: { font: { size: 15 } },
          title: { display: true, text: "Annual Salary", font: { size: 20 } },
        },
        y: {
          ticks: { font: { size: 18 } },
          title: {
            display: true,
            text: "Counts",
            font: { size: 20 },
          },
        },
      },
      plugins: {
        legend: { labels: { font: { size: 19 } } },
      },
    },
  };

  const myChart = new Chart(document.getElementById("myChart"), config);
}

// this function is to set up gradientBackground color.
function bgGradient(ctx, chartArea, scales) {
  const { left, right, top, bottom, width, height } = chartArea;
  const { x, y } = scales;
  const gradientBackground = ctx.createLinearGradient(0, top, 0, bottom);
  gradientBackground.addColorStop(0, "rgb(75, 192, 192, 1)");
  gradientBackground.addColorStop(1, "rgb(75, 192, 192, 0)");
  return gradientBackground;
}

urlSalary = "/api/salary";
createLineChart(urlSalary);
