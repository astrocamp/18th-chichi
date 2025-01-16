import Litepicker from "litepicker";

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("project-form");
  const startDateInput = document.getElementById("start-date");
  const endDateInput = document.getElementById("end-date");
  const errorElement = document.getElementById("date-error");

  // 初始化 Litepicker
  if (startDateInput && endDateInput) {
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
      setup: (picker) => {
        picker.on("selected", () => {
          errorElement.classList.add("hidden"); // 隱藏錯誤訊息
        });
      },
    });
  }

  // 表單提交驗證
  if (form) {
    form.addEventListener("submit", (e) => {
      const startDate = startDateInput.value;
      const endDate = endDateInput.value;

      // 驗證日期是否填寫
      if (!startDate || !endDate) {
        e.preventDefault(); // 阻止表單提交
        errorElement.classList.remove("hidden");
        errorElement.textContent = "請選擇開始日期和結束日期";
        return;
      }

      // 驗證結束日期是否晚於開始日期
      if (new Date(startDate) > new Date(endDate)) {
        e.preventDefault(); // 阻止表單提交
        errorElement.classList.remove("hidden");
        errorElement.textContent = "結束日期必須晚於開始日期";
        return;
      }

      // 如果檢查通過，隱藏錯誤訊息
      errorElement.classList.add("hidden");
    });
  }
});
