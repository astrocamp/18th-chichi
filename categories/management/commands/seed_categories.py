from django.core.management.base import BaseCommand
from categories.models import Category

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        root_categories = [
            {
                'title': '藝術',
                'children': [
                    {'title': '概念藝術'},
                    {'title': '數位藝術'},
                    {'title': '裝置藝術'},
                    {'title': '表演藝術'},
                    {'title': '公共藝術'},
                ],
            },
            {
                'title': '漫畫',
                'children': [
                    {'title': '作品選集'},
                    {'title': '漫畫書'},
                    {'title': '活動'},
                    {'title': '圖畫小說'},
                    {'title': '網路漫畫'},
                ],
            },
            {
                'title': '工藝',
                'children': [
                    {'title': '玻璃'},
                    {'title': '編織'},
                    {'title': '陶藝'},
                    {'title': '拼布'},
                    {'title': '木工'},
                ],
            },
            {
                'title': '舞蹈',
                'children': [
                    {'title': '演出'},
                    {'title': '現代舞'},
                    {'title': '街舞'},
                    {'title': '芭雷舞'},
                    {'title': '踢踏舞'},
                ],
            },
            {
                'title': '設計',
                'children': [
                    {'title': '建築'},
                    {'title': '城市設計'},
                    {'title': '平面設計'},
                    {'title': '產品設計'},
                    {'title': '互動式設計'},
                ],
            },
            {
                'title': '時尚',
                'children': [
                    {'title': '配件'},
                    {'title': '服飾'},
                    {'title': '童裝'},
                    {'title': '鞋類'},
                    {'title': '寵物時尚'},
                ],
            },
            {
                'title': '影劇',
                'children': [
                    {'title': '動作'},
                    {'title': '動畫'},
                    {'title': '喜劇'},
                    {'title': '浪漫'},
                    {'title': '恐怖'},
                ],
            },
            {
                'title': '食品',
                'children': [
                    {'title': '飲料'},
                    {'title': '素食'},
                    {'title': '農場'},
                    {'title': '農產品市場'},
                    {'title': '餐廳'},
                ],
            },
            {
                'title': '遊戲',
                'children': [
                    {'title': '電玩'},
                    {'title': '手機遊戲'},
                    {'title': '撲克牌'},
                    {'title': '拼圖'},
                    {'title': '桌上遊戲'},
                ],
            },
            {
                'title': '新聞',
                'children': [
                    {'title': '音訊'},
                    {'title': '照片'},
                    {'title': '刊物'},
                    {'title': '影片'},
                    {'title': '網站'},
                ],
            },
            {
                'title': '音樂',
                'children': [
                    {'title': '藍調'},
                    {'title': '古典'},
                    {'title': '鄉村'},
                    {'title': '爵士'},
                    {'title': '搖滾'},
                ],
            },
            {
                'title': '攝影',
                'children': [
                    {'title': '動物'},
                    {'title': '風景'},
                    {'title': '自然'},
                    {'title': '人物'},
                    {'title': '場所'},
                ],
            },
            {
                'title': '出版',
                'children': [
                    {'title': '學術'},
                    {'title': '畫冊'},
                    {'title': '童書'},
                    {'title': '小說'},
                    {'title': '雜誌'},
                ],
            },
            {
                'title': '科技',
                'children': [
                    {'title': '3D列印'},
                    {'title': '應用程式'},
                    {'title': '航空'},
                    {'title': '機器人'},
                    {'title': '軟體'},
                ],
            },
            {
                'title': '劇院',
                'children': [
                    {'title': '歌舞劇'},
                    {'title': '實驗性'},
                    {'title': '節慶'},
                    {'title': '沉浸式'},
                    {'title': '音樂劇'},
                ],
            },
        ]

        for root in root_categories:
            root_category, created = Category.objects.get_or_create(title=root['title'])
            for child in root.get('children', []):
                Category.objects.get_or_create(title=child['title'], parent=root_category)

        self.stdout.write(self.style.SUCCESS('Successfully seeded categories!'))
