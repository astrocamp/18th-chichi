document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger-btn');
    const menu = document.getElementById('mobile-menu');
  
    if (hamburger && menu) {
      hamburger.addEventListener('click', function(e) {
        e.preventDefault();
        // 切換 'hidden' 和 'block' 類別來顯示或隱藏選單
        menu.classList.toggle('hidden');
        menu.classList.toggle('opacity-0');
        menu.classList.toggle('opacity-100');
        menu.classList.toggle('transition-opacity');
  
        // 切換圖標
        const icon = hamburger.querySelector('i');
        if (icon) {
          icon.classList.toggle('fa-bars');
          icon.classList.toggle('fa-times');
        }
      });
  
      // 點擊空白處關閉選單
      document.addEventListener('click', function(e) {
        if (!menu.contains(e.target) && !hamburger.contains(e.target)) {
          if (!menu.classList.contains('hidden')) {
            menu.classList.add('hidden', 'opacity-0');
            menu.classList.remove('opacity-100');
            menu.classList.remove('transition-opacity');
            
            // 切換回漢堡圖標
            const icon = hamburger.querySelector('i');
            if (icon && icon.classList.contains('fa-times')) {
              icon.classList.remove('fa-times');
              icon.classList.add('fa-bars');
            }
          }
        }
      });
  
      // 按下 ESC 鍵關閉選單
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          if (!menu.classList.contains('hidden')) {
            menu.classList.add('hidden', 'opacity-0');
            menu.classList.remove('opacity-100');
            menu.classList.remove('transition-opacity');
  
            // 切換回漢堡圖標
            const icon = hamburger.querySelector('i');
            if (icon && icon.classList.contains('fa-times')) {
              icon.classList.remove('fa-times');
              icon.classList.add('fa-bars');
            }
          }
        }
      });
    } else {
      console.error('Hamburger button 或 mobile menu 未找到。');
    }
  
    // 登出按鈕功能
    const logoutButtons = document.querySelectorAll('[data-logout-url]');
    logoutButtons.forEach(button => {
      button.addEventListener('click', async function() {
        const url = this.dataset.logoutUrl;
        const csrfToken = this.dataset.csrf;
  
        try {
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
              'Content-Type': 'application/json'
            },
          });
  
          if (response.ok) {
            window.location.reload();
          } else {
            console.error('登出失敗:', response.statusText);
          }
        } catch (error) {
          console.error('登出失敗:', error);
        }
      });
    });
  });