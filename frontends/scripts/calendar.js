import Litepicker from "litepicker";

document.addEventListener("DOMContentLoaded", function () {
  const startDateInput = document.getElementById("start-date");
  const endDateInput = document.getElementById("end-date");
  const errorElement = document.getElementById("date-error");
  const form = document.querySelector("form");

  // 初始化 Litepicker
  new Litepicker({
    element: startDateInput,
    elementEnd: endDateInput,
    enableTime: true,
    singleMode: false,
    lang: "zh-TW",
    format: "YYYY-MM-DD",
    numberOfMonths: 2,
    numberOfColumns: 2,
    startDate: new Date(),
    minDate: new Date(),
    tooltipText: {
      one: "天",
      other: "天",
    },
    setup: (picker) => {
      picker.on("selected", () => {
        errorElement.classList.add("hidden"); // 隱藏錯誤訊息
      });
    },
  });

  // 表單提交驗證
  form.addEventListener("submit", (e) => {
    if (!startDateInput.value || !endDateInput.value) {
      e.preventDefault(); // 阻止表單提交
      errorElement.classList.remove("hidden"); // 顯示錯誤訊息
    }
  });
});
