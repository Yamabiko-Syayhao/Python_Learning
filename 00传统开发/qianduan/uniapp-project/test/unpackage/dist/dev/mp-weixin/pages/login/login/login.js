"use strict";
const common_vendor = require("../../../common/vendor.js");
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "login",
  setup(__props) {
    let userName = common_vendor.ref("admin");
    let passWord = common_vendor.ref("123456");
    return (_ctx, _cache) => {
      "raw js";
      const __returned__ = {
        a: common_vendor.unref(userName),
        b: common_vendor.o(($event) => common_vendor.isRef(userName) ? userName.value = $event.detail.value : userName = $event.detail.value, "e9"),
        c: common_vendor.unref(passWord),
        d: common_vendor.o(($event) => common_vendor.isRef(passWord) ? passWord.value = $event.detail.value : passWord = $event.detail.value, "cb"),
        e: common_vendor.o(
          //@ts-ignore
          (...args) => _ctx.handleLogin && _ctx.handleLogin(...args),
          "04"
        ),
        f: common_vendor.sei(common_vendor.gei(_ctx, ""), "view"),
        g: `${_ctx.u_s_b_h}px`,
        h: `${_ctx.u_s_a_i_b}px`,
        i: common_vendor.pvhc(_ctx.$scope.data.virtualHostClass)
      };
      return __returned__;
    };
  }
});
wx.createPage(_sfc_main);
//# sourceMappingURL=../../../../.sourcemap/mp-weixin/pages/login/login/login.js.map
