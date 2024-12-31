import Alpine from "alpinejs";
import htmx from "htmx.org";

window.Alpine = Alpine;
window.htmx = htmx;

Alpine.start();

// Font Awesome 引入
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import {
  faSpinner,
  faHouse,
  faHeart,
  faArrowRight,
  faCheck,
} from "@fortawesome/free-solid-svg-icons";
import "@fortawesome/fontawesome-svg-core/styles.css";

// 將圖標添加到庫中
library.add(faSpinner, faHouse, faHeart, faArrowRight, faCheck);

// 自動掃描 DOM 並渲染圖標
dom.watch();
