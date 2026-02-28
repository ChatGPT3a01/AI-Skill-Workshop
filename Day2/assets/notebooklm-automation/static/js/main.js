/**
 * 亮言~NotebookLM 自動化 Skill
 * 主要 JavaScript 檔案
 */

// ===== 全域變數 =====
window.currentNotebookId = null;

// ===== 頁面載入時執行 =====
document.addEventListener('DOMContentLoaded', function() {
    // 檢查認證狀態
    checkAuthStatusNav();

    // 載入主題設定
    loadTheme();
});

// ===== 認證狀態檢查 (導航列) =====
async function checkAuthStatusNav() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();

        const badge = document.getElementById('auth-status');
        if (badge) {
            if (data.authenticated) {
                badge.className = 'badge bg-success';
                badge.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i>已登入';
            } else {
                badge.className = 'badge bg-danger';
                badge.innerHTML = '<i class="bi bi-x-circle-fill me-1"></i>未登入';
            }
        }
    } catch (error) {
        console.error('檢查認證狀態失敗:', error);
        const badge = document.getElementById('auth-status');
        if (badge) {
            badge.className = 'badge bg-warning';
            badge.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-1"></i>檢查失敗';
        }
    }
}

// ===== 主題管理 =====
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'modern';
    applyTheme(savedTheme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

// ===== 通用工具函式 =====

/**
 * 顯示 Toast 通知
 */
function showToast(message, type = 'info') {
    // 如果沒有 Toast 容器，建立一個
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1100';
        document.body.appendChild(container);
    }

    const toastId = 'toast-' + Date.now();
    const icons = {
        'success': 'check-circle-fill',
        'danger': 'x-circle-fill',
        'warning': 'exclamation-triangle-fill',
        'info': 'info-circle-fill'
    };

    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${icons[type]} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 3000 });
    toast.show();

    // 自動移除
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * 格式化日期時間
 */
function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * 複製文字到剪貼簿
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('已複製到剪貼簿', 'success');
    } catch (error) {
        showToast('複製失敗', 'danger');
    }
}

/**
 * API 請求包裝器
 */
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API 請求失敗:', error);
        return { success: false, error: error.message };
    }
}

// ===== 快捷鍵支援 =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter 執行指令
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const commandInput = document.getElementById('command-input');
        if (commandInput && document.activeElement === commandInput) {
            e.preventDefault();
            if (typeof executeCommand === 'function') {
                executeCommand();
            }
        }
    }
});
