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
