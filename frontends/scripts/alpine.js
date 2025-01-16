import Alpine from "alpinejs";
window.Alpine = Alpine;

function formHandler() {
  return {
    products: [{ name: "" }],
    options: [{ name: "", price: 0 }],
    addProduct() {
      this.products.push({ name: "" });
    },
    removeProduct(index) {
      this.products.splice(index, 1);
    },
    addOption() {
      this.options.push({ name: "", price: 0 });
    },
    removeOption(index) {
      this.options.splice(index, 1);
    },
  };
}

function rewardForm(basePrice) {
  return {
    basePrice: parseFloat(basePrice),
    totalPrice: parseFloat(basePrice),
    updateTotal(event) {
      const price = parseFloat(event.target.dataset.price);
      if (event.target.checked) {
        this.totalPrice += price;
      } else {
        this.totalPrice -= price;
      }
    },
  };
}

window.rewardForm = rewardForm;
window.formHandler = formHandler;

function fileUploadHandler() {
  return {
    fileName: "尚未選擇檔案",
    previewUrl: null,

    handleFile(event) {
      const file = event.target.files[0];

      if (file) {
        this.fileName = file.name;

        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        this.fileName = "尚未選擇檔案";
        this.previewUrl = null;
      }
    },
  };
}
window.fileUploadHandler = fileUploadHandler;

function initBackToTopButton() {
  return {
    isVisible: false, // 狀態控制按鈕是否顯示

    init() {
      // 監聽滾動事件
      window.addEventListener("scroll", () => {
        this.isVisible = window.scrollY > 300; // 滾動超過 300px 顯示按鈕
      });
    },

    scrollToTop() {
      // 平滑滾動到頁面頂部
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
  };
}
window.initBackToTopButton = initBackToTopButton;

function rewardManager() {
  return {
    showToast: false,
    toastMessage: "",
    validateBeforeAdd(event) {
      // 停止默認的鏈接跳轉行為
      event.preventDefault();

      // 檢查是否存在商品
      const hasProducts = document.querySelectorAll("#product-list li:not(.text-gray-500)").length > 0;

      if (!hasProducts) {
        this.toastMessage = "請先新增商品，再新增回饋方案！";
        this.showToast = true;

        // 1.5 秒後自動隱藏提示框
        setTimeout(() => {
          this.showToast = false;
        }, 1500);
      } else {
        // 從按鈕的 href 屬性獲取目標 URL
        const targetUrl = event.target.closest("a").getAttribute("href");
        window.location.href = targetUrl;
      }
    },
  };
}
window.rewardManager = rewardManager;

function dateValidationHandler(defaultDate, today) {
  return {
    selectedDate: defaultDate || "", // 初始化為預設值或空字串
    isInvalid: false,
    today: today,

    validateDate() {
      // 檢查日期是否有效
      this.isInvalid = this.selectedDate > this.today;
    },

    init() {
      // 預設值初始化時進行驗證
      if (this.selectedDate) {
        this.validateDate();
      }
    },
  };
}
window.dateValidationHandler = dateValidationHandler;
