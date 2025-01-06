import { Chart, registerables } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { BoxPlotController, BoxAndWiskers } from "@sgratzl/chartjs-chart-boxplot";

Chart.register(...registerables, ChartDataLabels, BoxPlotController, BoxAndWiskers);

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("gender_proportion");
  canvas.width = 400;
  canvas.height = 400;

  const slug = canvas.dataset.slug;

  fetch(`/projects/${slug}/gender_proportion/`)
    .then((response) => response.json())
    .then((data) => {
      const ctx = canvas.getContext("2d");
      if (ctx) {
        const total = data.datasets[0].data.reduce((a, b) => a + b, 0);

        new Chart(ctx, {
          type: "pie",
          data: data,
          options: {
            responsive: false,
            plugins: {
              legend: {
                display: true,
              },
              title: {
                display: true,
                text: `贊助者性別比例（總人數: ${total}人）`,
                font: {
                  size: 16,
                  weight: "bold",
                },
              },
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => {
                    const dataset = tooltipItem.dataset;
                    const currentValue = dataset.data[tooltipItem.dataIndex];
                    const total = dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = ((currentValue / total) * 100).toFixed(2);
                    return `${tooltipItem.label}: ${currentValue}人 (${percentage}%)`;
                  },
                },
              },
              datalabels: {
                display: true,
                color: "#000",
                font: {
                  size: 12,
                  weight: "bold",
                },
                formatter: (value, context) => {
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(2);
                  return `${value}人 (${percentage}%)`;
                },
              },
            },
          },
        });
      }
    })
    .catch((error) => console.error("Error fetching chart data:", error));
});

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("daily_sponsorship_amount");
  canvas.width = 600;
  canvas.height = 400;

  const slug = canvas.dataset.slug;

  fetch(`/projects/${slug}/daily_sponsorship_amount/`)
    .then((response) => response.json())
    .then((data) => {
      const ctx = canvas.getContext("2d");
      if (ctx) {
        const maxAmount = Math.max(...data.datasets[0].data);

        new Chart(ctx, {
          type: "line",
          data: data,
          options: {
            responsive: false,
            plugins: {
              legend: {
                display: true,
              },
              title: {
                display: true,
                text: "累積贊助金額趨勢分析",
                font: {
                  size: 16,
                  weight: "bold",
                },
              },
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => {
                    const dataset = tooltipItem.dataset;
                    const currentValue = dataset.data[tooltipItem.dataIndex];
                    return `日期: ${tooltipItem.label} - 金額: $${currentValue}`;
                  },
                },
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "日期",
                  font: {
                    size: 14,
                    weight: "bold",
                  },
                },
              },
              y: {
                title: {
                  display: true,
                  text: "累積金額 ($)",
                  font: {
                    size: 14,
                    weight: "bold",
                  },
                },
                suggestedMax: maxAmount + 1000,
                beginAtZero: true,
              },
            },
          },
        });
      }
    })
    .catch((error) => console.error("Error fetching chart data:", error));
});

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("gender_amount_boxplot");
  canvas.width = 400;
  canvas.height = 400;

  const slug = canvas.dataset.slug;

  fetch(`/projects/${slug}/gender_amount_boxplot/`)
    .then((response) => response.json())
    .then((data) => {
      const ctx = canvas.getContext("2d");

      if (ctx) {
        new Chart(ctx, {
          type: "boxplot",
          data: {
            labels: data.labels,
            datasets: [
              {
                label: data.datasets[0].label,
                data: data.datasets[0].data.map((box) => ({
                  min: box.min,
                  q1: box.q1,
                  median: box.median,
                  q3: box.q3,
                  max: box.max,
                  outliers: box.outliers,
                })),
                backgroundColor: data.datasets[0].backgroundColor,
                borderColor: data.datasets[0].borderColor,
                borderWidth: data.datasets[0].borderWidth,
              },
            ],
          },
          options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true,
              },
              title: {
                display: true,
                text: "贊助金額性別分布箱型圖",
                font: {
                  size: 16,
                  weight: "bold",
                },
              },
              tooltip: {
                enabled: false,
              },
              datalabels: {
                display: false,
              },
            },
            scales: {
              y: {
                title: {
                  display: true,
                  text: "金額 (單位: 元)",
                },
              },
            },
          },
          plugins: [],
        });
      }
    })
    .catch((error) => console.error("Error fetching chart data:", error));
});

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("reward_grouped_bar_chart");
  canvas.width = 400;
  canvas.height = 400;

  const slug = canvas.dataset.slug;

  fetch(`/projects/${slug}/reward_grouped_bar_chart/`)
    .then((response) => response.json())
    .then((data) => {
      const ctx = canvas.getContext("2d");

      if (ctx) {
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: data.labels,
            datasets: data.datasets,
          },
          options: {
            responsive: false,
            plugins: {
              legend: {
                display: true,
              },
              title: {
                display: true,
                text: "熱門回饋方案",
              },
              tooltip: {
                enabled: true,
                callbacks: {
                  label: (tooltipItem) => {
                    return `人數: ${tooltipItem.raw}`;
                  },
                },
              },
              datalabels: {
                display: false,
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "回饋方案",
                },
              },
              y: {
                title: {
                  display: true,
                  text: "贊助人數",
                },
                ticks: {
                  stepSize: 1,
                  callback: (value) => {
                    if (Number.isInteger(value)) return value;
                    return null;
                  },
                },
                suggestedMax: Math.max(...data.datasets.flatMap((dataset) => dataset.data)) + 2,
              },
            },
          },
        });
      }
    })
    .catch((error) => console.error("Error fetching chart data:", error));
});
