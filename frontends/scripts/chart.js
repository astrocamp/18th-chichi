import { Chart, registerables } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { BoxPlotController, BoxAndWiskers } from "@sgratzl/chartjs-chart-boxplot";

Chart.register(...registerables, ChartDataLabels, BoxPlotController, BoxAndWiskers);

function genderProportionChart() {
  return {
    canvas: null,
    slug: null,

    init() {
      this.canvas = this.$refs.canvas;
      this.slug = this.canvas.dataset.slug;

      this.canvas.width = 400;
      this.canvas.height = 400;

      this.fetchChartData();
    },

    async fetchChartData() {
      try {
        const response = await fetch(`/projects/${this.slug}/gender_proportion/`);
        const data = await response.json();
        this.renderChart(data);
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    },

    renderChart(data) {
      const ctx = this.canvas.getContext("2d");
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
    },
  };
}
window.genderProportionChart = genderProportionChart;

function dailySponsorshipChart() {
  return {
    canvas: null,
    slug: null,

    init() {
      this.canvas = this.$refs.canvas;
      this.slug = this.canvas.dataset.slug;

      this.canvas.width = 600;
      this.canvas.height = 400;

      this.fetchChartData();
    },

    async fetchChartData() {
      try {
        const response = await fetch(`/projects/${this.slug}/daily_sponsorship_amount/`);
        const data = await response.json();
        this.renderChart(data);
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    },

    renderChart(data) {
      const ctx = this.canvas.getContext("2d");
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
    },
  };
}
window.dailySponsorshipChart = dailySponsorshipChart;

function genderAmountBoxplotChart() {
  return {
    canvas: null,
    slug: null,

    init() {
      this.canvas = this.$refs.canvas;
      this.slug = this.canvas.dataset.slug;

      this.canvas.width = 400;
      this.canvas.height = 400;

      this.fetchChartData();
    },

    async fetchChartData() {
      try {
        const response = await fetch(`/projects/${this.slug}/gender_amount_boxplot/`);
        const data = await response.json();
        this.renderChart(data);
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    },

    renderChart(data) {
      const ctx = this.canvas.getContext("2d");

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
        });
      }
    },
  };
}
window.genderAmountBoxplotChart = genderAmountBoxplotChart;

function rewardGroupedBarChart() {
  return {
    canvas: null,
    slug: null,

    init() {
      this.canvas = this.$refs.canvas;
      this.slug = this.canvas.dataset.slug;

      this.canvas.width = 400;
      this.canvas.height = 400;

      this.fetchChartData();
    },

    async fetchChartData() {
      try {
        const response = await fetch(`/projects/${this.slug}/reward_grouped_bar_chart/`);
        const data = await response.json();
        this.renderChart(data);
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    },

    renderChart(data) {
      const ctx = this.canvas.getContext("2d");

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
    },
  };
}
window.rewardGroupedBarChart = rewardGroupedBarChart;
