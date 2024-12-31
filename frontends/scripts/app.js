import Alpine from "alpinejs";
import htmx from "htmx.org";
import Sortable from "sortablejs";

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
import { faSpinner, faHouse, faHeart, faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons"; // 引入 spinner 圖標
import "@fortawesome/fontawesome-svg-core/styles.css"; // 引入基本樣式

// 將圖標添加到庫中
library.add(faSpinner, faHouse, faHeart, faMagnifyingGlass);

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
