/* ===========================================
   CHART.JS 初始化 — SWD原则配置
   注意：每次生成报告时，根据实际数据填写labels和datasets
   =========================================== */

/* 移动端检测：≤768px 时关闭宽高比联动，由 CSS min-height 控制高度 */
const isMobile = window.matchMedia('(max-width: 768px)').matches;

const ctx1 = document.getElementById('chart1');
if (ctx1) {
  new Chart(ctx1, {
    type: 'line',  // 根据数据类型选择：line/bar/scatter
    data: {
      labels: [/* x轴标签 */],
      datasets: [{
        label: '[系列名]',
        data: [/* 数据点 */],
        borderColor: '#2f4f4f',
        backgroundColor: 'rgba(47,79,79,0.08)',
        borderWidth: 2,
        pointRadius: 4,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: !isMobile,
      plugins: {
        legend: { display: false },
        title: { display: false }
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { font: { family: 'Helvetica Neue' } }
        },
        y: {
          grid: { color: '#f0ece2', lineWidth: 1 },
          border: { display: false },
          ticks: { font: { family: 'Helvetica Neue' } }
        }
      }
    }
  });
}

/* ===========================================
   FLOAT TOC — 悬浮目录滚动高亮
   用 IntersectionObserver 监听各节进入视口，
   自动给对应目录项加 .active 类
   =========================================== */
(function () {
  const toc   = document.getElementById('floatToc');
  if (!toc) return;

  const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  // 收集正文 section id
  const ids      = links.map(a => a.getAttribute('href').slice(1));
  const sections = ids.map(id => document.getElementById(id)).filter(Boolean);

  // 去重（子节 .sub 可能指向同一 id）
  const uniqueSections = [...new Set(sections)];

  let activeId = null;

  const setActive = (id) => {
    if (id === activeId) return;
    activeId = id;
    links.forEach(a => {
      const match = a.getAttribute('href') === '#' + id;
      a.classList.toggle('active', match);
    });
    // 让高亮项在目录中保持可见（目录本身有滚动条时）
    const activeLink = toc.querySelector('a.active');
    if (activeLink) {
      activeLink.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  };

  // IntersectionObserver：section 进入视口上半部分时激活
  const observer = new IntersectionObserver((entries) => {
    // 找出所有当前可见的 section，取 y 坐标最小（最靠近顶部）的
    const visible = entries
      .filter(e => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (visible.length > 0) {
      setActive(visible[0].target.id);
    }
  }, {
    rootMargin: '-10% 0px -60% 0px',  // 触发区：视口上方10%到中间40%
    threshold: 0
  });

  uniqueSections.forEach(sec => observer.observe(sec));

  // 平滑滚动（覆盖 CSS scroll-behavior，确保目录点击也有动画）
  links.forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const target = document.getElementById(a.getAttribute('href').slice(1));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();

/* ===========================================
   VERIFY PANEL — 悬浮验证面板控制器
   功能：
     · 点击标题栏或按 V 键展开/折叠
     · 自动扫描三区内容，统计 ✓ 和 ✗ 行，更新徽章
     · 有 ✗ 偏差项时：面板橙框、显示偏差汇总区、自动展开
     · 全部通过时：绿色徽章、默认折叠
   =========================================== */
(function () {
  const panel       = document.getElementById('verifyPanel');
  const toggle      = document.getElementById('verifyToggle');
  const body        = document.getElementById('verifyBody');
  const badge       = document.getElementById('verifyBadge');
  const statsEl     = document.getElementById('verifyStatsContent');
  const calcEl      = document.getElementById('verifyCalcContent');
  const warnSection = document.getElementById('verifyWarnSection');
  const warnContent = document.getElementById('verifyWarnContent');
  const note        = document.getElementById('verifyNote');
  if (!panel || !toggle) return;

  /* ---- 收集所有区域文本，统计通过/偏差数 ---- */
  function parseSummary() {
    const allText = [statsEl, calcEl].map(el => el ? el.textContent : '').join('\n');
    const passed  = (allText.match(/✓/g) || []).length;
    const warned  = (allText.match(/✗/g) || []).length;
    const total   = passed + warned;

    if (total === 0) {
      badge.textContent = '暂无数据';
      badge.style.background = '';
      return;
    }

    if (warned > 0) {
      panel.classList.add('has-warn');
      badge.textContent = `${passed}✓  ${warned}✗`;

      /* 提取偏差行，填充偏差汇总区 */
      if (warnSection && warnContent) {
        const warnLines = allText.split('\n')
          .filter(l => l.includes('✗'))
          .join('\n');
        warnContent.textContent = warnLines;
        warnSection.style.display = '';
      }

      if (note && !note.textContent.trim()) {
        note.textContent =
          `⚠ 发现 ${warned} 项计算偏差，报告正文保留原始数据，` +
          `建议在「讨论」节说明偏差原因。`;
      }
    } else {
      panel.classList.remove('has-warn');
      badge.textContent = `${passed}/${total} 通过`;
      if (warnSection) warnSection.style.display = 'none';
    }
  }

  /* ---- 展开/折叠 ---- */
  function open()  { panel.classList.add('open');    toggle.setAttribute('aria-expanded', 'true'); }
  function close() { panel.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
  function togglePanel() { panel.classList.contains('open') ? close() : open(); }

  /* ---- 有偏差时默认展开，全部通过则默认折叠 ---- */
  parseSummary();
  if (panel.classList.contains('has-warn')) open();

  toggle.addEventListener('click', togglePanel);

  /* ---- V 键快捷键（不在输入框时）---- */
  document.addEventListener('keydown', e => {
    if ((e.key === 'v' || e.key === 'V') &&
        !e.target.getAttribute('contenteditable') &&
        !['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) {
      e.preventDefault();
      togglePanel();
    }
  });
})();

/* ===========================================
   MOBILE NAV — 移动端浮动导航按钮
   功能：
     · 点击 ☰ 按钮展开目录菜单
     · 点击菜单项平滑滚动到对应章节，并自动关闭菜单
     · 点击遮罩层关闭菜单
     · 仅在 1024px 以下生效（CSS 控制显示）
   =========================================== */
(function () {
  const btn     = document.getElementById('mobileNavBtn');
  const menu    = document.getElementById('mobileNavMenu');
  const overlay = document.getElementById('mobileNavOverlay');
  if (!btn || !menu) return;

  function openMenu() {
    menu.classList.add('open');
    overlay.classList.add('open');
    btn.classList.add('open');
    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('aria-label', '关闭目录');
  }
  function closeMenu() {
    menu.classList.remove('open');
    overlay.classList.remove('open');
    btn.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', '打开目录');
  }
  function toggleMenu() {
    btn.classList.contains('open') ? closeMenu() : openMenu();
  }

  btn.addEventListener('click', e => { e.stopPropagation(); toggleMenu(); });
  overlay.addEventListener('click', closeMenu);

  /* 点击菜单项：平滑滚动 + 关闭菜单 */
  menu.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const target = document.getElementById(a.getAttribute('href').slice(1));
      if (target) {
        // 考虑固定元素遮挡，向上偏移 16px
        const y = target.getBoundingClientRect().top + window.scrollY - 16;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
      closeMenu();
    });
  });
})();

/* ===========================================
   INLINE EDITOR — 内联文本编辑器
   触发方式：
     1. 鼠标悬停页面左上角热区（80×80px）→ 编辑按钮出现 → 点击
     2. 键盘快捷键 E 键（在文本框内输入时无效）
     3. 直接点击热区
   编辑模式下：
     - 所有 p、h1-h4、li、td、.abstract p、.keywords 可点击编辑
     - 编辑中的元素有绿色边框高亮
     - Ctrl+S / Cmd+S 保存到 localStorage 并导出文件
     - 再次触发 E 或点击按钮退出编辑模式
   注意：不使用 CSS ~ 兄弟选择器控制显隐（pointer-events:none 会断链）
         必须用 JS + 400ms 延时实现热区悬停效果
   =========================================== */
class ReportInlineEditor {
  constructor() {
    this.isActive   = false;
    this.storageKey = 'lab-report-edits-' + encodeURIComponent(document.title);
    this.editableSelector = [
      'h1','h2.section-title','h3','h4',
      'p:not(.no-edit)',
      'li:not(.no-edit)',
      'td:not(.no-edit)',
      '.abstract p',
      '.keywords',
      '.subtitle',
      '.journal-bar div'
    ].join(',');

    this._buildUI();
    this._bindHotzone();
    this._bindKeyboard();
    this._restoreFromStorage();
  }

  /* ---------- UI 构建 ---------- */
  _buildUI() {
    // 热区（左上角不可见触发区域）
    this.hotzone = document.createElement('div');
    this.hotzone.className = 'edit-hotzone';
    this.hotzone.title = '点击进入编辑模式';

    // 编辑切换按钮
    this.btn = document.createElement('button');
    this.btn.className = 'edit-toggle';
    this.btn.id = 'editToggle';
    this.btn.title = '编辑报告文字 (E)';
    this.btn.innerHTML = '✏️';

    // 状态提示条（编辑模式时显示在顶部）
    this.bar = document.createElement('div');
    this.bar.className = 'edit-statusbar';
    this.bar.innerHTML =
      '<span>✏️ 编辑模式 — 点击任意文字开始编辑</span>' +
      '<span class="edit-actions">' +
        '<kbd>Ctrl+S</kbd> 保存并导出 &nbsp;|&nbsp; ' +
        '<kbd>E</kbd> 退出编辑' +
      '</span>';

    document.body.prepend(this.bar);
    document.body.prepend(this.btn);
    document.body.prepend(this.hotzone);

    this.btn.addEventListener('click', () => this.toggleEditMode());
  }

  /* ---------- 热区悬停（400ms grace period，避免指针事件断链）---------- */
  _bindHotzone() {
    let hideTimer = null;

    const showBtn = () => {
      clearTimeout(hideTimer);
      this.btn.classList.add('show');
    };
    const scheduleHide = () => {
      hideTimer = setTimeout(() => {
        if (!this.isActive) this.btn.classList.remove('show');
      }, 400);
    };

    this.hotzone.addEventListener('mouseenter', showBtn);
    this.hotzone.addEventListener('mouseleave', scheduleHide);
    this.hotzone.addEventListener('click',      () => this.toggleEditMode());
    this.btn.addEventListener('mouseenter',     showBtn);
    this.btn.addEventListener('mouseleave',     scheduleHide);
  }

  /* ---------- 键盘快捷键 ---------- */
  _bindKeyboard() {
    document.addEventListener('keydown', e => {
      // E 键切换编辑模式（在 contenteditable 内输入时跳过）
      if ((e.key === 'e' || e.key === 'E') &&
          !e.target.getAttribute('contenteditable') &&
          !['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) {
        e.preventDefault();
        this.toggleEditMode();
      }
      // Ctrl+S / Cmd+S 保存
      if ((e.ctrlKey || e.metaKey) && e.key === 's' && this.isActive) {
        e.preventDefault();
        this.saveAndExport();
      }
    });
  }

  /* ---------- 编辑模式开关 ---------- */
  toggleEditMode() {
    this.isActive ? this.exitEditMode() : this.enterEditMode();
  }

  enterEditMode() {
    this.isActive = true;
    this.btn.classList.add('active','show');
    this.btn.innerHTML = '✅';
    this.btn.title = '退出编辑模式 (E)';
    document.body.classList.add('edit-mode-on');

    // 给所有可编辑元素加上 contenteditable
    document.querySelectorAll(this.editableSelector).forEach(el => {
      // 跳过验证摘要框、代码块、图注（不应手动编辑）
      if (el.closest('.verification, .formula, figcaption, .references')) return;
      el.setAttribute('contenteditable', 'true');
      el.setAttribute('data-edit-original', el.innerHTML);
      el.classList.add('editable-active');
      // 失焦时自动存 localStorage
      el.addEventListener('blur', () => this._autosave(), { passive: true });
    });
  }

  exitEditMode() {
    this.isActive = false;
    this.btn.classList.remove('active');
    if (!this._hotzoneHovered) this.btn.classList.remove('show');
    this.btn.innerHTML = '✏️';
    this.btn.title = '编辑报告文字 (E)';
    document.body.classList.remove('edit-mode-on');

    document.querySelectorAll('[contenteditable="true"]').forEach(el => {
      el.removeAttribute('contenteditable');
      el.classList.remove('editable-active');
    });

    this._autosave();
  }

  /* ---------- 自动保存到 localStorage ---------- */
  _autosave() {
    const edits = {};
    document.querySelectorAll('[data-edit-original]').forEach((el, i) => {
      const key = el.dataset.editOriginal ? 'el-' + i : null;
      if (key) edits[key] = { html: el.innerHTML, tag: el.tagName, index: i };
    });
    try {
      localStorage.setItem(this.storageKey, JSON.stringify({
        savedAt: new Date().toISOString(),
        body: document.querySelector('main').innerHTML
      }));
    } catch(e) { /* localStorage 不可用时静默失败 */ }
  }

  /* ---------- 从 localStorage 恢复 ---------- */
  _restoreFromStorage() {
    try {
      const raw = localStorage.getItem(this.storageKey);
      if (!raw) return;
      const data = JSON.parse(raw);
      if (data && data.body) {
        document.querySelector('main').innerHTML = data.body;
        // 图表需要重新初始化（innerHTML 替换后 canvas 上下文丢失）
        this._reinitCharts();
        console.info('[ReportEditor] 已从本地存储恢复上次编辑，保存时间:', data.savedAt);
      }
    } catch(e) {}
  }

  /* ---------- 恢复后重新初始化 Chart.js ---------- */
  _reinitCharts() {
    // 销毁已有实例，再重建
    Object.values(Chart.instances || {}).forEach(c => c.destroy());
    // 触发自定义事件，让页面内的图表初始化代码重新运行
    document.dispatchEvent(new CustomEvent('report-editor-restored'));
  }

  /* ---------- 保存并导出 HTML 文件 ---------- */
  saveAndExport() {
    this._autosave();

    // 临时移除编辑态样式再序列化
    const wasActive = this.isActive;
    document.body.classList.remove('edit-mode-on');
    document.querySelectorAll('[contenteditable]').forEach(el => {
      el.removeAttribute('contenteditable');
      el.classList.remove('editable-active');
    });

    const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;

    // 恢复编辑态
    if (wasActive) {
      document.body.classList.add('edit-mode-on');
      document.querySelectorAll(this.editableSelector).forEach(el => {
        if (el.closest('.verification, .formula, figcaption, .references')) return;
        el.setAttribute('contenteditable', 'true');
        el.classList.add('editable-active');
      });
    }

    // 触发下载
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const a    = document.createElement('a');
    a.href     = URL.createObjectURL(blob);
    a.download = (document.title || 'lab-report') + '-edited.html';
    a.click();
    URL.revokeObjectURL(a.href);

    this._showToast('✅ 已保存并导出文件');
  }

  /* ---------- 轻量 Toast 提示 ---------- */
  _showToast(msg) {
    const t = document.createElement('div');
    t.className = 'edit-toast';
    t.textContent = msg;
    document.body.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 400); }, 2200);
  }
}

// 初始化编辑器
const reportEditor = new ReportInlineEditor();