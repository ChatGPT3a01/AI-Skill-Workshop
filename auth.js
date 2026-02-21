/**
 * 學員登錄系統 — AI Skill 實作課
 * 學員密碼：預設 SKILL2026（可由管理員變更）
 * 終極密碼：管理員專用，可修改學員密碼
 */
(function () {
  // ===== 密碼雜湊 =====
  var DEFAULT_STUDENT_HASH = '26c30f7f6c428d5d5c191ac8e9476d1c2d001d37834d1f50029d2949e65d49d3';
  var MASTER_HASH = '3ee7f6541f8186b90ad66c06d6e5bf89ca81c3c16c07b48800d751ac21adcd23';

  // ===== 工具函式 =====
  function sha256(str) {
    var encoder = new TextEncoder();
    var data = encoder.encode(str);
    return crypto.subtle.digest('SHA-256', data).then(function (buf) {
      return Array.from(new Uint8Array(buf)).map(function (b) {
        return b.toString(16).padStart(2, '0');
      }).join('');
    });
  }

  function isLoggedIn() {
    return sessionStorage.getItem('skillAuth') === 'true';
  }

  function isMaster() {
    return sessionStorage.getItem('skillMaster') === 'true';
  }

  // ===== 建立登錄畫面 =====
  function createLoginOverlay() {
    var overlay = document.createElement('div');
    overlay.id = 'authOverlay';
    overlay.innerHTML =
      '<div id="authBox">' +
        '<div id="authLogo">🔐</div>' +
        '<h2 id="authTitle">學員登錄</h2>' +
        '<p id="authSubtitle">AI Skill 實作課｜專業流程變現為 AI 技能教戰手冊</p>' +
        '<div id="authForm">' +
          '<input type="password" id="authPassword" placeholder="請輸入課程密碼" autocomplete="off">' +
          '<button id="authSubmit">登　錄</button>' +
          '<p id="authError"></p>' +
        '</div>' +
        '<div id="adminPanel" style="display:none;">' +
          '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.15);margin:20px 0;">' +
          '<h3 style="color:#a78bfa;font-size:14px;margin-bottom:12px;">🛡️ 管理員面板</h3>' +
          '<p style="color:rgba(255,255,255,0.6);font-size:12px;margin-bottom:8px;">變更學員密碼：</p>' +
          '<input type="text" id="newStudentPwd" placeholder="輸入新的學員密碼">' +
          '<button id="changePwdBtn">變更密碼</button>' +
          '<button id="resetPwdBtn" style="background:transparent;border:1px solid rgba(255,255,255,0.2);margin-top:6px;">恢復預設 (SKILL2026)</button>' +
          '<p id="adminMsg"></p>' +
        '</div>' +
      '</div>';

    // ===== 樣式 =====
    var style = document.createElement('style');
    style.textContent =
      '#authOverlay{' +
        'position:fixed;top:0;left:0;right:0;bottom:0;z-index:99999;' +
        'background:linear-gradient(135deg,#1a1035 0%,#2d1b69 50%,#1a1035 100%);' +
        'display:flex;align-items:center;justify-content:center;' +
        'font-family:"Microsoft JhengHei","Segoe UI",Arial,sans-serif;' +
      '}' +
      '#authBox{' +
        'background:rgba(255,255,255,0.06);backdrop-filter:blur(20px);' +
        '-webkit-backdrop-filter:blur(20px);' +
        'border:1px solid rgba(255,255,255,0.1);border-radius:20px;' +
        'padding:48px 40px;width:380px;max-width:90vw;text-align:center;' +
        'box-shadow:0 20px 60px rgba(0,0,0,0.4);' +
        'animation:authFadeIn 0.5s ease;' +
      '}' +
      '@keyframes authFadeIn{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}' +
      '#authLogo{font-size:48px;margin-bottom:16px;}' +
      '#authTitle{color:#fff;font-size:24px;font-weight:700;margin-bottom:8px;}' +
      '#authSubtitle{color:rgba(255,255,255,0.5);font-size:13px;margin-bottom:32px;}' +
      '#authForm input,#adminPanel input{' +
        'width:100%;padding:14px 18px;border:1px solid rgba(255,255,255,0.15);' +
        'border-radius:12px;background:rgba(255,255,255,0.08);color:#fff;' +
        'font-size:16px;outline:none;transition:border-color 0.3s;' +
        'font-family:inherit;' +
      '}' +
      '#authForm input:focus,#adminPanel input:focus{border-color:#7c3aed;}' +
      '#authForm input::placeholder,#adminPanel input::placeholder{color:rgba(255,255,255,0.3);}' +
      '#authSubmit,#changePwdBtn,#resetPwdBtn{' +
        'width:100%;padding:14px;border:none;border-radius:12px;' +
        'background:linear-gradient(135deg,#7c3aed,#a855f7);color:#fff;' +
        'font-size:16px;font-weight:600;cursor:pointer;margin-top:12px;' +
        'transition:transform 0.2s,box-shadow 0.2s;font-family:inherit;' +
      '}' +
      '#authSubmit:hover,#changePwdBtn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(124,58,237,0.4);}' +
      '#authError{color:#f87171;font-size:13px;margin-top:12px;min-height:20px;}' +
      '#adminMsg{color:#a78bfa;font-size:13px;margin-top:10px;min-height:20px;}' +
      '#authBox .authShake{animation:authShake 0.4s ease;}' +
      '@keyframes authShake{0%,100%{transform:translateX(0);}25%{transform:translateX(-8px);}75%{transform:translateX(8px);}}';

    document.head.appendChild(style);
    document.body.appendChild(overlay);

    // ===== 事件綁定 =====
    var pwdInput = document.getElementById('authPassword');
    var submitBtn = document.getElementById('authSubmit');
    var errorEl = document.getElementById('authError');

    function doLogin() {
      var pwd = pwdInput.value.trim();
      if (!pwd) {
        errorEl.textContent = '請輸入密碼';
        return;
      }
      submitBtn.textContent = '驗證中...';
      submitBtn.disabled = true;

      sha256(pwd).then(function (hash) {
        // 檢查終極密碼
        if (hash === MASTER_HASH) {
          sessionStorage.setItem('skillAuth', 'true');
          sessionStorage.setItem('skillMaster', 'true');
          showAdminPanel();
          return;
        }
        // 檢查自訂密碼
        var customHash = localStorage.getItem('skillCustomHash');
        if (customHash && hash === customHash) {
          sessionStorage.setItem('skillAuth', 'true');
          overlay.remove();
          return;
        }
        // 檢查預設密碼
        if (hash === DEFAULT_STUDENT_HASH) {
          sessionStorage.setItem('skillAuth', 'true');
          overlay.remove();
          return;
        }
        // 密碼錯誤
        errorEl.textContent = '密碼錯誤，請重新輸入';
        pwdInput.value = '';
        pwdInput.focus();
        submitBtn.textContent = '登　錄';
        submitBtn.disabled = false;
        var box = document.getElementById('authBox');
        box.classList.remove('authShake');
        void box.offsetWidth;
        box.classList.add('authShake');
      });
    }

    submitBtn.addEventListener('click', doLogin);
    pwdInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') doLogin();
    });

    // 自動 focus
    setTimeout(function () { pwdInput.focus(); }, 300);
  }

  // ===== 管理員面板 =====
  function showAdminPanel() {
    var overlay = document.getElementById('authOverlay');
    var authForm = document.getElementById('authForm');
    var adminPanel = document.getElementById('adminPanel');
    var title = document.getElementById('authTitle');
    var logo = document.getElementById('authLogo');

    logo.textContent = '🛡️';
    title.textContent = '管理員已登錄';
    authForm.innerHTML =
      '<button id="authEnter" style="width:100%;padding:14px;border:none;border-radius:12px;' +
      'background:linear-gradient(135deg,#059669,#10b981);color:#fff;font-size:16px;font-weight:600;' +
      'cursor:pointer;transition:transform 0.2s;font-family:inherit;">✅ 進入課程</button>';

    document.getElementById('authEnter').addEventListener('click', function () {
      overlay.remove();
    });

    adminPanel.style.display = 'block';

    // 顯示目前密碼狀態
    var adminMsg = document.getElementById('adminMsg');
    var customDisplay = localStorage.getItem('skillCustomDisplay');
    if (customDisplay) {
      adminMsg.textContent = '目前學員密碼：' + customDisplay;
    } else {
      adminMsg.textContent = '目前使用預設密碼';
    }

    // 變更密碼
    document.getElementById('changePwdBtn').addEventListener('click', function () {
      var newPwd = document.getElementById('newStudentPwd').value.trim();
      if (!newPwd) {
        adminMsg.textContent = '請輸入新密碼';
        adminMsg.style.color = '#f87171';
        return;
      }
      if (newPwd.length < 4) {
        adminMsg.textContent = '密碼至少 4 個字元';
        adminMsg.style.color = '#f87171';
        return;
      }
      sha256(newPwd).then(function (hash) {
        localStorage.setItem('skillCustomHash', hash);
        localStorage.setItem('skillCustomDisplay', newPwd);
        adminMsg.textContent = '✅ 學員密碼已變更為：' + newPwd;
        adminMsg.style.color = '#34d399';
        document.getElementById('newStudentPwd').value = '';
      });
    });

    // 恢復預設
    document.getElementById('resetPwdBtn').addEventListener('click', function () {
      localStorage.removeItem('skillCustomHash');
      localStorage.removeItem('skillCustomDisplay');
      adminMsg.textContent = '✅ 已恢復預設密碼 (SKILL2026)';
      adminMsg.style.color = '#34d399';
    });
  }

  // ===== 初始化 =====
  function init() {
    if (isLoggedIn()) return; // 已登錄，不顯示
    createLoginOverlay();
  }

  // 等 DOM 載入完成
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
