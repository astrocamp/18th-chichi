// Font Awesome 引入
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import { faSpinner, faHouse, faHeart, faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons"; // 引入 spinner 圖標
import "@fortawesome/fontawesome-svg-core/styles.css"; // 引入基本樣式

// 將圖標添加到庫中
library.add(faSpinner, faHouse, faHeart, faMagnifyingGlass);

// 自動掃描 DOM 並渲染圖標
dom.watch();
