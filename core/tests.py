from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import json
from .models import FoodItem, Vote, Suggestion

class FoodItemModelTest(TestCase):
    def test_create_food_item(self):
        """测试创建食物项目"""
        food = FoodItem.objects.create(
            name="测试食物",
            meal_type="breakfast",
            description="描述"
        )
        self.assertEqual(food.name, "测试食物")
        self.assertTrue(food.is_active)
        self.assertEqual(str(food), "早餐 - 测试食物")

class VoteModelTest(TestCase):
    def setUp(self):
        self.food = FoodItem.objects.create(name="测试食物", meal_type="lunch")
        self.tomorrow = (timezone.now() + timedelta(days=1)).date()

    def test_vote_uniqueness(self):
        """测试同一IP同一天只能投一票"""
        # 第一票
        Vote.objects.create(
            food=self.food,
            ip_address="127.0.0.1",
            vote_for_date=self.tomorrow
        )
        
        # 尝试投第二票（应该失败）
        with self.assertRaises(Exception):
            Vote.objects.create(
                food=self.food,
                ip_address="127.0.0.1",
                vote_for_date=self.tomorrow
            )

class APITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.food = FoodItem.objects.create(name="红烧肉", meal_type="lunch")
        self.vote_url = reverse('core:submit_vote')
        self.rankings_url = reverse('core:get_rankings')
        self.suggestion_url = reverse('core:submit_suggestion')

    def test_get_rankings(self):
        """测试获取排行榜API"""
        response = self.client.get(self.rankings_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('breakfast', data)
        self.assertIn('lunch', data)
        self.assertIn('dinner', data)

    def test_submit_vote_success(self):
        """测试投票成功"""
        response = self.client.post(self.vote_url, {'food_id': self.food.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # 验证数据库记录
        self.assertEqual(Vote.objects.count(), 1)

    def test_submit_vote_duplicate(self):
        """测试重复投票"""
        # 第一次投票
        self.client.post(self.vote_url, {'food_id': self.food.id})
        
        # 第二次投票
        response = self.client.post(self.vote_url, {'food_id': self.food.id})
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('已经', data['error'])

    def test_submit_suggestion(self):
        """测试提交建议"""
        response = self.client.post(self.suggestion_url, {
            'content': '测试建议内容',
            'category': 'suggestion'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # 验证数据库
        self.assertEqual(Suggestion.objects.count(), 1)
        self.assertEqual(Suggestion.objects.first().content, '测试建议内容')
