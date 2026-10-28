"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "index",
  setup(__props) {
    const title = common_vendor.ref("Hello");
    common_vendor.onLoad(() => {
      common_vendor.index.__f__("log", "at pages/index/index.uvue:21", "首页加载");
    });
    common_vendor.onPageShow(() => {
      common_vendor.index.__f__("log", "at pages/index/index.uvue:26", "进入首页页面");
    });
    common_vendor.onPageHide(() => {
      common_vendor.index.__f__("log", "at pages/index/index.uvue:31", "离开首页页面");
    });
    return (_ctx, _cache) => {
      "raw js";
      const __returned__ = {
        a: common_assets._imports_0,
        b: common_vendor.t(common_vendor.unref(title)),
        c: common_vendor.sei(common_vendor.gei(_ctx, ""), "view"),
        d: `${_ctx.u_s_b_h}px`,
        e: `${_ctx.u_s_a_i_b}px`,
        f: common_vendor.pvhc(_ctx.$scope.data.virtualHostClass)
      };
      return __returned__;
    };
  }
});
wx.createPage(_sfc_main);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/index/index.js.map
