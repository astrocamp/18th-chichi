import "./alpine.js";
import htmx from "htmx.org";
import "./chart.js";
import "./sortable.js";
import "./fontawesome.js";
import "./navbar.js";
import "./register.js";
import "./calendar.js";
import { initCategoryNav, initCategoryScroll, categoryManagerall } from "./categoryNav.js";
import "./fullcalendar.js";
window.htmx = htmx;

window.htmx = htmx;
window.initCategoryNav = initCategoryNav;
window.initCategoryScroll = initCategoryScroll;
window.categoryManagerall = categoryManagerall;

window.Alpine = Alpine;

Alpine.start();
