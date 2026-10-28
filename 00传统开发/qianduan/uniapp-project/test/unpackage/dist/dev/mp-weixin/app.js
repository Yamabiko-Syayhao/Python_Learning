"use strict";
Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const common_vendor = require("./common/vendor.js");
if (!Math) {
  "./pages/login/login/login.js";
  "./pages/index/index.js";
  "./pages/mine/mine.js";
  "./pages/car/car.js";
}
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "App",
  setup(__props) {
    common_vendor.onLaunch(() => {
      common_vendor.index.__f__("log", "at App.uvue:7", "App Launch");
    });
    common_vendor.onAppShow(() => {
      common_vendor.index.__f__("log", "at App.uvue:11", "App Show");
    });
    common_vendor.onAppHide(() => {
      common_vendor.index.__f__("log", "at App.uvue:15", "App Hide");
    });
    return () => {
    };
  }
});
function createApp() {
  const app = common_vendor.createSSRApp(_sfc_main);
  return {
    app
  };
}
createApp().app.mount("#app");
exports.createApp = createApp;
//# sourceMappingURL=../.sourcemap/mp-weixin/app.js.map
