import Litepicker from 'litepicker';

document.addEventListener('DOMContentLoaded', function() {
    const startDateElement = document.getElementById('start-date');
    const endDateElement = document.getElementById('end-date');

    // 只在需要的頁面上初始化日期選擇器
    if (startDateElement && endDateElement) {
        new Litepicker({
            element: startDateElement,
            elementEnd: endDateElement,
            enableTime: true,
            singleMode: false,
            lang: 'zh-TW',
            format: 'YYYY-MM-DD',
            numberOfMonths: 2,  
            numberOfColumns: 2,
            startDate: new Date(),  
            minDate: new Date(),    
            tooltipText: {
                one: '天',
                other: '天'
            },
            setup: (picker) => {
                picker.on('selected', (startDate, endDate) => {
                    console.log('選擇的日期範圍：', {
                        start: startDate.format('YYYY-MM-DD'),
                        end: endDate.format('YYYY-MM-DD')
                    });
                });
            }
        });
    }
});