// source/scripts/math-fix.js

// 1. 配置 MathJax (必须在脚本加载前定义)
window.MathJax = {
  tex: {
    // 兼容 Pandoc 的 \(...\) 和原始 Markdown 的 $...$
    inlineMath: [ ['$','$'], ['\\(','\\)'] ], 
    displayMath: [ ['$$','$$'], ['\\[','\\]'] ],
    processEscapes: true
  },
  startup: {
    // 页面加载后自动尝试渲染
    pageReady: () => {
      return MathJax.startup.defaultPageReady();
    }
  }
};

// 2. 针对 PJAX 和 首次加载延迟的补丁
function forceRenderMath() {
  if (window.MathJax && window.MathJax.typesetPromise) {
    // 强制重绘
    MathJax.typesetPromise();
  } else {
    // 如果 MathJax 还没加载完，1秒后重试
    setTimeout(forceRenderMath, 1000);
  }
}

// 监听 Fluid 的 PJAX 跳转事件
document.addEventListener('pjax:complete', forceRenderMath);

// 监听 DOM 加载完成事件
document.addEventListener('DOMContentLoaded', forceRenderMath);