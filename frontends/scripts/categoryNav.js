// 分類導航相關的 Alpine.js 代碼
export function initCategoryNav(currentCategory = '全部') {
    return {
        activeTab: currentCategory,
        filterProjects(category) {
            this.activeTab = category;
            const url = new URL(window.location.href);
            url.search = '';
            if (category !== '全部') {
                url.searchParams.set('category', category);
            }
            window.location.href = url.toString();
        }
    }
}

export function initCategoryScroll() {
    return {
        showLeftArrow: false,
        showRightArrow: false,
        scrollContainer: null,
        init() {
            this.scrollContainer = this.$refs.categoryNav;
            this.checkArrows();
            this.scrollContainer.addEventListener('scroll', () => this.checkArrows());

            // 頁面載入後, 自動捲動到當前 activeTab 按鈕
            this.$nextTick(() => {
                const activeBtn = this.scrollContainer.querySelector(`[data-category='${this.$root.activeTab}']`);
                if (activeBtn) {
                    activeBtn.scrollIntoView({
                        behavior: 'smooth',
                        inline: 'center'
                    });
                }
            });
        },
        checkArrows() {
            this.showLeftArrow = this.scrollContainer.scrollLeft > 0;
            this.showRightArrow = 
                this.scrollContainer.scrollLeft < 
                (this.scrollContainer.scrollWidth - this.scrollContainer.clientWidth);
        },
        scrollLeft() {
            this.scrollContainer.scrollBy({ left: -400, behavior: 'smooth' });
        },
        scrollRight() {
            this.scrollContainer.scrollBy({ left: 400, behavior: 'smooth' });
        }
    }
}

// 專案列表頁面的分類管理
export function categoryManagerall() {
    return {
        activeTab: '全部',
        showLeftArrow: false,
        showRightArrow: false,
        scrollContainer: null,
        init() {
            // 從 URL 獲取當前分類
            const urlParams = new URLSearchParams(window.location.search);
            this.activeTab = urlParams.get('category') || '全部';

            // 初始化滾動容器
            this.scrollContainer = document.querySelector('[data-category-nav]');
            this.checkArrows();
            this.scrollContainer.addEventListener('scroll', () => this.checkArrows());

            // 自動滾動到當前分類
            this.$nextTick(() => {
                const activeBtn = this.scrollContainer.querySelector(`[data-category='${this.activeTab}']`);
                if (activeBtn) {
                    activeBtn.scrollIntoView({
                        behavior: 'smooth',
                        inline: 'center'
                    });
                }
            });
        },
        filterProjects(category) {
            this.activeTab = category;
            const url = new URL(window.location.href);
            url.search = '';
            if (category !== '全部') {
                url.searchParams.set('category', category);
            }
            window.location.href = url.toString();
        },
        checkArrows() {
            this.showLeftArrow = this.scrollContainer.scrollLeft > 0;
            this.showRightArrow = 
                this.scrollContainer.scrollLeft < 
                (this.scrollContainer.scrollWidth - this.scrollContainer.clientWidth);
        },
        scrollLeft() {
            this.scrollContainer.scrollBy({ left: -400, behavior: 'smooth' });
        },
        scrollRight() {
            this.scrollContainer.scrollBy({ left: 400, behavior: 'smooth' });
        }
    }
} 