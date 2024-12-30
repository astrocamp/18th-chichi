import Alpine from "alpinejs";
import htmx from "htmx.org";

window.Alpine = Alpine;
window.htmx = htmx;

export function formHandler() {
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

Alpine.start();

// Font Awesome 引入
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import { faSpinner, faHouse, faHeart } from "@fortawesome/free-solid-svg-icons"; // 引入 spinner 圖標
import "@fortawesome/fontawesome-svg-core/styles.css"; // 引入基本樣式

// 將圖標添加到庫中
library.add(faSpinner, faHouse, faHeart);

// 自動掃描 DOM 並渲染圖標
dom.watch();
