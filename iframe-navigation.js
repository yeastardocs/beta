// 在 iframe 页面中拦截所有 <a> 链接的点击行为，阻止其默认跳转，然后通过 postMessage 通知父页面（主页面）执行跳转，实现统一由父页面控制导航、更新 URL 和菜单状态
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", (e) => {
        const href = a.getAttribute("href");
        if (href) {
          if (href.startsWith("https://help.yeastar.com")) return;
          e.preventDefault();
          window.parent.postMessage({ type: "navigate", href }, "*");
        }
      });
    });
  });
})();
