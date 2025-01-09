// 定義並導出到全局
window.showModal = function(url) {
  const modal = document.getElementById('modal');
  const modalContent = document.getElementById('modal-content');

  // 顯示彈出視窗
  modal.classList.remove('hidden');

  // 載入內容
  fetch(url)
    .then(response => response.text())
    .then(html => {
      modalContent.innerHTML = html;
    });

  // 點擊背景關閉彈出視窗
  modal.addEventListener('click', function (e) {
    if (e.target === modal) {
      closeModal();
    }
  });
}

window.closeModal = function() {
  const modal = document.getElementById('modal');
  modal.classList.add('hidden');
}

// 按下 ESC 鍵關閉彈出視窗
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    window.closeModal();
  }
}); 