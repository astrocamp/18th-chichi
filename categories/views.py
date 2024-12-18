from django.shortcuts import render
from .models import Category


def initialize_categories():
    categories = [
        "藝術",
        "漫畫",
        "工藝",
        "舞蹈",
        "設計",
        "時尚",
        "影片",
        "食品",
        "遊戲",
        "新聞",
        "音樂",
        "攝影",
        "出版",
        "科技",
        "劇院",
    ]
    for title in categories:
        Category.objects.get_or_create(title=title)


def index(request):
    initialize_categories()
    categories = Category.objects.all()
    return render(request, "categories/index.html", {"categories": categories})
