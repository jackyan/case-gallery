#!/usr/bin/env python
"""
添加示例数据到数据库
"""
import os
import django
from datetime import timedelta

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from core.models import FoodItem, Vote, Suggestion

def add_sample_data():
    """添加示例数据"""
    
    # 清除现有数据（可选）
    print("清除现有数据...")
    FoodItem.objects.all().delete()
    Suggestion.objects.all().delete()
    
    # 添加早餐食物
    print("添加早餐食物...")
    breakfast_foods = [
        {'name': '小笼包', 'description': '鲜美多汁的传统小笼包'},
        {'name': '豆浆油条', 'description': '经典中式早餐组合'},
        {'name': '煎饺', 'description': '香脆可口的煎饺'},
        {'name': '粥配小菜', 'description': '清淡养胃的早餐'},
        {'name': '肉包子', 'description': '热气腾腾的肉包子'},
    ]
    
    for food_data in breakfast_foods:
        FoodItem.objects.create(
            meal_type='breakfast',
            **food_data
        )
    
    # 添加午餐食物
    print("添加午餐食物...")
    lunch_foods = [
        {'name': '红烧肉盖浇饭', 'description': '香浓美味的红烧肉'},
        {'name': '宫保鸡丁', 'description': '经典川菜'},
        {'name': '西红柿炒蛋', 'description': '家常小炒'},
        {'name': '糖醋里脊', 'description': '酸甜可口'},
        {'name': '鱼香肉丝', 'description': '下饭神菜'},
        {'name': '麻婆豆腐', 'description': '川味豆腐'},
        {'name': '青椒肉丝', 'description': '简单家常菜'},
    ]
    
    for food_data in lunch_foods:
        FoodItem.objects.create(
            meal_type='lunch',
            **food_data
        )
    
    # 添加晚餐食物
    print("添加晚餐食物...")
    dinner_foods = [
        {'name': '酸菜鱼', 'description': '酸辣开胃的鱼片'},
        {'name': '烤鸡腿', 'description': '香嫩多汁'},
        {'name': '炸鸡排', 'description': '外酥里嫩'},
        {'name': '番茄牛腩', 'description': '软烂入味'},
        {'name': '清蒸鲈鱼', 'description': '清淡鲜美'},
        {'name': '水煮肉片', 'description': '麻辣爽口'},
    ]
    
    for food_data in dinner_foods:
        FoodItem.objects.create(
            meal_type='dinner',
            **food_data
        )
    
    # 添加一些示例投票
    print("添加示例投票...")
    tomorrow = (timezone.now() + timedelta(days=1)).date()
    all_foods = list(FoodItem.objects.all())
    
    # 为前几个食物添加不同数量的投票
    import random
    for i, food in enumerate(all_foods[:10]):
        vote_count = random.randint(5, 50)
        for j in range(vote_count):
            Vote.objects.create(
                food=food,
                vote_for_date=tomorrow,
                ip_address=f"192.168.1.{j % 255}"
            )
    
    # 添加示例建议
    print("添加示例建议...")
    suggestions = [
        {'content': '食堂的菜品很好吃，就是份量有点少，希望能多一点。', 'category': 'suggestion'},
        {'content': '早餐的包子很好吃，但是经常卖完，建议多做一些。', 'category': 'suggestion'},
        {'content': '食堂环境很好，阿姨们服务态度也很好，点赞！', 'category': 'praise'},
        {'content': '希望能增加一些素菜选项，照顾素食主义者。', 'category': 'suggestion'},
        {'content': '午餐的汤有点咸，能不能淡一点？', 'category': 'complaint'},
        {'content': '食堂的餐具很干净，卫生做得很好！', 'category': 'praise'},
        {'content': '晚餐的菜品种类有点少，希望能多样化一些。', 'category': 'suggestion'},
        {'content': '价格很实惠，性价比很高，感谢食堂！', 'category': 'praise'},
        {'content': '建议增加麻辣烫窗口，很多同学都喜欢吃。', 'category': 'suggestion'},
        {'content': '今天的红烧肉超级好吃，厨师手艺棒棒的！', 'category': 'praise'},
    ]
    
    for suggestion_data in suggestions:
        Suggestion.objects.create(**suggestion_data)
    
    print("\n示例数据添加完成！")
    print(f"- 食物项目: {FoodItem.objects.count()} 个")
    print(f"- 投票记录: {Vote.objects.count()} 条")
    print(f"- 意见建议: {Suggestion.objects.count()} 条")

if __name__ == '__main__':
    add_sample_data()
