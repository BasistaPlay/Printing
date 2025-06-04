// === LIBRARIES ===
import Alpine from 'alpinejs';
import htmx from 'htmx.org';
import Cookies from 'js-cookie';
import $ from 'jquery';
window.$ = $;
window.jQuery = $;
import html2canvas from 'html2canvas';
import { fabric } from 'fabric';
import domtoimage from 'dom-to-image';

// === PLUGINS ===
import 'jquery-ui/ui/widget';
import 'jquery-ui/ui/widgets/mouse';
import 'jquery-ui/ui/widgets/draggable';
import 'jquery-ui/ui/widgets/resizable';
import 'jquery-ui-touch-punch';

// === SWUP ===
import Swup from 'swup';
import SwupHeadPlugin from '@swup/head-plugin';
import SwupScriptsPlugin from '@swup/scripts-plugin';

// === INIT ===
import 'lazysizes';
import './darkmode.js';
import './base.js';
import './app.js';

// === HOME ===
import './home/home_page.js';

// === USER ===
import './User/account.js';
import './User/phone.js';

// === PRODUCT ===
import './Product/addimage.js';
import './Product/addtext.js';
import './Product/addtocart.js';
import './Product/aiimagegenerate.js';
import './Product/design.js';
import './Product/general_design.js';
import './Product/SaveDesign.js';


window.Alpine = Alpine;
document.addEventListener('DOMContentLoaded', () => {
  Alpine.start();
});