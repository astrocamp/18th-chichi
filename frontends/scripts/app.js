import Alpine from "alpinejs";
import htmx from "htmx.org";
import Sortable from "sortablejs";
import { library, dom } from '@fortawesome/fontawesome-svg-core'
import "@fortawesome/fontawesome-svg-core/styles.css";
import { 
  faBookmark, 
  faClock, 
  faComments,
  faQuestionCircle,
  faNewspaper,
  faGift,
  faRocket,
  faStopCircle,
  faHandHoldingHeart,
  faArrowLeft,
  faSave,
  faUserEdit,
  faUserPlus,
  faProjectDiagram,
  faUser,
  faTrash,
  faPlus,
  faPlusCircle,
  faUndo,
  faBox,
  faCheck,
  faEdit,
  faFileAlt,
  faShippingFast,
  faMapMarkerAlt,
  faInfoCircle,
  faCalendarAlt,
  faMagnifyingGlass,
  faSignInAlt,
  faSignOutAlt,
  faPaperPlane,
  faSpinner,
  faHouse,
  faHeart,
  faArrowRight
} from "@fortawesome/free-solid-svg-icons";

window.Alpine = Alpine
window.htmx = htmx

export function formHandler() {
  return {
    products: [{ name: '' }],
    options: [{ name: '', price: 0 }],
    addProduct() {
      this.products.push({ name: '' })
    },
    removeProduct(index) {
      this.products.splice(index, 1)
    },
    addOption() {
      this.options.push({ name: '', price: 0 })
    },
    removeOption(index) {
      this.options.splice(index, 1)
    },
  }
}

function rewardForm(basePrice) {
  return {
    basePrice: parseFloat(basePrice),
    totalPrice: parseFloat(basePrice),
    updateTotal(event) {
      const price = parseFloat(event.target.dataset.price)
      if (event.target.checked) {
        this.totalPrice += price
      } else {
        this.totalPrice -= price
      }
    },
  }
}

window.rewardForm = rewardForm
window.formHandler = formHandler

Alpine.start()

// 添加圖示到庫中
library.add(
  faBookmark,
  faClock,
  faComments,
  faQuestionCircle,
  faNewspaper,
  faGift,
  faRocket,
  faStopCircle,
  faHandHoldingHeart,
  faArrowLeft,
  faSave,
  faUserEdit,
  faUserPlus,
  faProjectDiagram,
  faUser,
  faTrash,
  faPlus,
  faPlusCircle,
  faUndo,
  faBox,
  faCheck,
  faEdit,
  faFileAlt,
  faShippingFast,
  faMapMarkerAlt,
  faInfoCircle,
  faCalendarAlt,
  faMagnifyingGlass,
  faSignInAlt,
  faSignOutAlt,
  faPaperPlane,
  faSpinner,
  faHouse,
  faHeart,
  faArrowRight
);

// 自動掃描 DOM 並渲染圖標
dom.watch();

document.addEventListener("DOMContentLoaded", function () {
  var element = document.getElementById("faq-list");
  if (element) {
    var sortable = Sortable.create(element, {
      animation: 150,
      onEnd: function () {
        var order = sortable.toArray();
        fetch("/faqs/updated-faq-position/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: JSON.stringify({ position: order })
        })
        .then(response => response.json())
        .then(data => {
          console.log("Success:", data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
      }
    });
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

document.addEventListener("DOMContentLoaded", () => {
  // 獲取畫布元素
  const canvas = document.getElementById("chartCanvas");
  canvas.width = 500; // 設置寬度
  canvas.height = 400; // 設置高度

  // 從 data-slug 屬性中獲取 slug
  const slug = canvas.dataset.slug;

  // 使用 slug 動態生成 API 路徑
  fetch(`/projects/${slug}/chart_data/`)
    .then((response) => response.json())
    .then((data) => {
      const ctx = canvas.getContext("2d");
      if (ctx) {
        new Chart(ctx, {
          type: "bar", // 圖表類型
          data: data,
          options: {
            responsive: false, // 禁用響應式
            plugins: {
              legend: {
                display: true,
              },
            },
          },
        });
      }
    })
    .catch((error) => console.error("Error fetching chart data:", error));
});

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
                suggestedMax: maxAmount + 1000, // 增加一點空間
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
                  outliers: box.outliers, // 確保包含離群值數據
                })),
                backgroundColor: data.datasets[0].backgroundColor,
                borderColor: data.datasets[0].borderColor,
                borderWidth: data.datasets[0].borderWidth,
              },
            ],
          },
          options: {
            responsive: false,
            maintainAspectRatio: false, // 確保圖表填滿畫布
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
                enabled: false, // 禁用 Tooltip，防止顯示數值
              },
              datalabels: {
                display: false, // 確保禁用 DataLabels 插件
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
          plugins: [], // 確保未啟用其他插件，避免干擾
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
                enabled: true, // 啟用 Tooltip
                callbacks: {
                  label: (tooltipItem) => {
                    return `人數: ${tooltipItem.raw}`;
                  },
                },
              },
              datalabels: {
                display: false, // 禁用數據標籤
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
                  stepSize: 1, // 設置步長為 1，僅顯示整數
                  callback: (value) => {
                    if (Number.isInteger(value)) return value; // 確保只顯示整數
                    return null;
                  },
                },
                suggestedMax: Math.max(...data.datasets.flatMap((dataset) => dataset.data)) + 2, // 上方多留 2 個單位空間
              },
            },
          },
        });
      }
    })
    .catch((error) => console.error("Error fetching chart data:", error));
});
