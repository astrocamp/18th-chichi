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
                display: true, // 顯示圖例
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
                enabled: true, // 滑動時顯示數據
                callbacks: {
                  label: (context) => {
                    const value = context.raw;
                    const label = context.label;
                    return `日期: ${label} - 金額: $${value}`;
                  },
                },
              },
              datalabels: {
                display: false, // 禁止數據標籤的預設顯示
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
            elements: {
              line: {
                borderColor: "rgba(75, 192, 192, 1)", // 線條顏色
                borderWidth: 2, // 線條寬度
                fill: false, // 禁止塗色
              },
              point: {
                radius: 0, // 禁止預設顯示數據點
                hoverRadius: 5, // 滑動時顯示的數據點大小
              },
            },
          },
        });
      }
    },
  };
}
window.dailySponsorshipChart = dailySponsorshipChart;

function genderAmountScatterChart() {
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
        const response = await fetch(`/projects/${this.slug}/gender_amount_scatter/`);
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
          type: "scatter",
          data: {
            labels: data.labels,
            datasets: [
              // 男性點狀數據
              {
                label: "男",
                data: this.jitterPoints(data.scatter_datasets[0].data, "男"),
                backgroundColor: "#F8AFAF",
                pointRadius: 4,
              },
              // 女性點狀數據
              {
                label: "女",
                data: this.jitterPoints(data.scatter_datasets[1].data, "女"),
                backgroundColor: "#A8D3F0",
                pointRadius: 4,
              },
              // 其他性別點狀數據
              {
                label: "其他",
                data: this.jitterPoints(data.scatter_datasets[2].data, "其他"),
                backgroundColor: "#FFE69B",
                pointRadius: 4,
              },
              // 中位數顯示為獨立點
              {
                label: "中位數",
                data: data.median_data,
                type: "scatter",
                backgroundColor: "#CACACA",
                borderColor: "#CACACA",
                borderWidth: 2,
                pointRadius: 8, // 中位數顯示為更大的點
              },
            ],
          },
          options: {
            plugins: {
              legend: {
                display: true,
                position: "top",
              },
              tooltip: {
                enabled: true,
                callbacks: {
                  label: (context) => {
                    if (context.dataset.label === "中位數") {
                      return `中位數: ${context.raw.y} 元`;
                    }
                    return `金額: ${context.raw.y} 元`;
                  },
                },
              },
              datalabels: {
                display: false,
              },
            },
            scales: {
              x: {
                type: "category",
                title: {
                  display: true,
                  text: "性別",
                },
                ticks: {
                  autoSkip: false,
                  padding: 20,
                },
                offset: true, // 增加左右留白
              },
              y: {
                title: {
                  display: true,
                  text: "金額 (元)",
                },
                beginAtZero: true,
              },
            },
          },
        });
      }
    },

    jitterPoints(points, category) {
      const jitterAmount = 0.2; // 控制水平偏移的範圍
      return points.map((amount) => ({
        x: category,
        y: amount,
        _jitterX: Math.random() * jitterAmount - jitterAmount / 2, // 隨機水平偏移
      }));
    },
  };
}

window.genderAmountScatterChart = genderAmountScatterChart;
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
