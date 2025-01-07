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
