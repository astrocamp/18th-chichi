from django.shortcuts import render
from .models import SubCategory


def initialize_subcategories():
    subcategories = [
        "陶瓷",
        "概念藝術",
        "數位藝術",
        "繪圖",
        "裝置藝術",
        "混合媒體",
        "繪畫",
        "表演藝術",
        "公共藝術",
        "雕塑",
        "社會參與",
        "紡織品",
        "影片藝術",
        "作品選集",
        "漫畫書",
        "活動",
        "圖畫小說",
        "網路漫畫",
        "蠟燭",
        "鉤針編織",
        "DIY",
        "刺繡",
        "玻璃",
        "編織",
        "陶藝",
        "出版",
        "拼布",
        "文具",
        "織造",
        "木工",
        "演出",
        "太空",
        "工作坊",
        "建築",
        "城市設計",
        "平面設計",
        "互動式設計",
        "產品設計",
        "玩具",
        "字型設計",
        "配件",
        "服飾",
        "童裝",
        "時裝",
        "鞋類",
        "珠寶",
        "寵物時尚",
        "Ready-to-wear",
        "動作",
        "動畫",
        "喜劇",
        "紀錄片",
        "話劇",
        "實驗性",
        "家庭",
        "奇幻",
        "節慶",
        "恐怖",
        "電影院",
        "MV",
        "敘事電影",
        "浪漫",
        "科幻",
        "短片",
        "電視",
        "驚悚",
        "網路劇集",
        "社區花園",
        "料理書",
        "飲料",
        "活動",
        "農產品市場",
        "農場",
        "美食車",
        "餐廳",
        "少量生產",
        "太空",
        "素食",
        "遊戲相關硬體",
        "實況遊戲",
        "手機遊戲",
        "撲克牌",
        "拼圖",
        "桌上遊戲",
        "電玩",
        "音訊",
        "照片",
        "出版",
        "影片",
        "網站",
        "藍調",
        "芯片",
        "古典音樂",
        "喜劇",
        "鄉村 & 民謠音樂",
        "電子音樂",
        "信仰",
        "Hip-Hop",
        "獨立搖滾",
        "爵士",
        "兒童",
        "拉丁",
        "金屬",
        "流行音樂",
        "龐克",
        "R&B",
        "搖滾",
        "世界音樂",
        "動物",
        "藝術",
        "自然",
        "人物",
        "相片書",
        "場所",
        "學術",
        "作品選集",
        "畫冊",
        "行事曆",
        "童書",
        "喜劇",
        "虛構小說",
        "活版印刷",
        "文學期刊",
        "文學空間",
        "非虛構小說",
        "期刊",
        "詩詞",
        "廣播 & 播客",
        "翻譯",
        "年輕人",
        "雜誌",
        "3D 列印",
        "應用程式",
        "相機器材",
        "電子類 DIY",
        "製造工具",
        "航空",
        "小工具",
        "硬體",
        "創客空間",
        "機器人",
        "軟體",
        "聲音",
        "太空探索",
        "穿戴式裝置",
        "網站",
        "喜劇",
        "實驗性",
        "節慶",
        "沉浸式",
        "音樂劇",
        "演出",
    ]
    for subcategory_title in subcategories:
        SubCategory.objects.get_or_create(title=subcategory_title)


def subindex(request):
    initialize_subcategories()
    subcategories = SubCategory.objects.all()
    return render(request, "subcategories/index.html", {"subcategories": subcategories})
