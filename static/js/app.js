(function () {
  "use strict";

  window.tpSetTheme = function (theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem('tp-theme', theme); } catch (e) {}
  };
  window.tpToggleTheme = function () {
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    window.tpSetTheme(current === 'dark' ? 'light' : 'dark');
  };

  window.tpToggleSidebarCollapse = function () {
    var sidebar = document.getElementById('sidebar');
    var main = document.getElementById('mainArea');
    if (!sidebar || !main) return;
    var collapsed = sidebar.classList.toggle('collapsed');
    main.classList.toggle('collapsed', collapsed);
    try { localStorage.setItem('tp-sidebar-collapsed', collapsed ? '1' : '0'); } catch (e) {}
  };

  window.tpToggleSidebarMobile = function () {
    var sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.toggle('open');
  };

  window.tpToast = function (message, type) {
    var stack = document.getElementById('toastStack');
    if (!stack || !message) return;
    var el = document.createElement('div');
    el.className = 'tp-toast ' + (type || 'info');
    el.textContent = message;
    stack.appendChild(el);
    setTimeout(function () {
      el.style.transition = 'opacity .2s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 200);
    }, 4200);
  };

  var cmdkItems = [];
  window.tpRegisterCommands = function (items) { cmdkItems = items || []; };

  function paletteBackdrop() { return document.getElementById('cmdkBackdrop'); }

  function openPalette() {
    var backdrop = paletteBackdrop();
    if (!backdrop) return;
    backdrop.style.display = 'flex';
    var input = document.getElementById('cmdkInput');
    if (input) { input.value = ''; setTimeout(function () { input.focus(); }, 10); }
    renderPaletteItems('');
  }
  function closePalette() {
    var backdrop = paletteBackdrop();
    if (backdrop) backdrop.style.display = 'none';
  }
  function isPaletteOpen() {
    var backdrop = paletteBackdrop();
    return !!backdrop && backdrop.style.display === 'flex';
  }
  function renderPaletteItems(query) {
    var list = document.getElementById('cmdkList');
    if (!list) return;
    var q = query.trim().toLowerCase();
    var filtered = cmdkItems.filter(function (item) { return item.label.toLowerCase().indexOf(q) !== -1; });
    list.innerHTML = '';
    filtered.forEach(function (item, i) {
      var div = document.createElement('div');
      div.className = 'cmdk-item' + (i === 0 ? ' active' : '');
      var label = document.createElement('span');
      label.textContent = item.label;
      var group = document.createElement('span');
      group.style.color = 'var(--text-muted)';
      group.style.fontSize = '0.75rem';
      group.textContent = item.group || '';
      div.appendChild(label);
      div.appendChild(group);
      div.addEventListener('click', function () { window.location.href = item.url; });
      list.appendChild(div);
    });
    if (!filtered.length) {
      var empty = document.createElement('div');
      empty.style.padding = '1rem';
      empty.style.color = 'var(--text-muted)';
      empty.style.fontSize = '0.85rem';
      empty.textContent = 'No matches.';
      list.appendChild(empty);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('tp-sidebar-collapsed') === '1') {
      var sidebar = document.getElementById('sidebar');
      var main = document.getElementById('mainArea');
      if (sidebar && main) { sidebar.classList.add('collapsed'); main.classList.add('collapsed'); }
    }

    document.querySelectorAll('[data-countup]').forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-countup'));
      if (isNaN(target)) return;
      var suffix = el.getAttribute('data-suffix') || '';
      var decimals = el.getAttribute('data-decimals') === '1' ? 1 : 0;
      var start = null;
      var duration = 700;
      function step(ts) {
        if (!start) start = ts;
        var progress = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var value = target * eased;
        el.textContent = value.toFixed(decimals) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });

    var input = document.getElementById('cmdkInput');
    if (input) input.addEventListener('input', function (e) { renderPaletteItems(e.target.value); });
    var backdrop = paletteBackdrop();
    if (backdrop) backdrop.addEventListener('click', function (e) { if (e.target === backdrop) closePalette(); });
  });

  document.addEventListener('keydown', function (e) {
    var key = (e.key || '').toLowerCase();
    if ((e.metaKey || e.ctrlKey) && key === 'k') {
      e.preventDefault();
      openPalette();
      return;
    }
    if (!isPaletteOpen()) return;
    if (e.key === 'Escape') { closePalette(); return; }
    if (e.key === 'Enter') {
      var active = document.querySelector('.cmdk-item.active');
      if (active) active.click();
      return;
    }
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      var items = Array.prototype.slice.call(document.querySelectorAll('.cmdk-item'));
      if (!items.length) return;
      var idx = items.findIndex(function (i) { return i.classList.contains('active'); });
      if (idx === -1) idx = 0;
      items[idx].classList.remove('active');
      var next = e.key === 'ArrowDown' ? Math.min(idx + 1, items.length - 1) : Math.max(idx - 1, 0);
      items[next].classList.add('active');
    }
  });

  window.tpOpenPalette = openPalette;
  window.tpClosePalette = closePalette;
})();
