from django.db import models
from django.utils import timezone
from datetime import timedelta


class FoodItem(models.Model):
    """食物项目模型"""
    MEAL_CHOICES = [
        ('breakfast', '早餐'),
        ('lunch', '午餐'),
        ('dinner', '晚餐'),
    ]
    
    name = models.CharField('食物名称', max_length=100)
    meal_type = models.CharField('餐点类型', max_length=20, choices=MEAL_CHOICES)
    image = models.ImageField('图片', upload_to='foods/', blank=True, null=True)
    description = models.TextField('描述', max_length=200, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        verbose_name = '食物项目'
        verbose_name_plural = '食物项目'
        ordering = ['meal_type', 'name']
    
    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.name}"
    
    def get_vote_count(self, for_date=None):
        """获取投票数"""
        if for_date is None:
            # 默认获取明天的投票
            for_date = (timezone.now() + timedelta(days=1)).date()
        return self.votes.filter(vote_for_date=for_date).count()


class Vote(models.Model):
    """投票记录模型"""
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='votes', verbose_name='食物')
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    voted_at = models.DateTimeField('投票时间', auto_now_add=True)
    vote_for_date = models.DateField('投票日期')  # 投票针对的日期（明天）
    
    class Meta:
        verbose_name = '投票记录'
        verbose_name_plural = '投票记录'
        ordering = ['-voted_at']
        # 同一IP每天只能为同一食物投一票
        unique_together = [['food', 'ip_address', 'vote_for_date']]
    
    def __str__(self):
        return f"{self.food.name} - {self.vote_for_date}"


class Suggestion(models.Model):
    """意见建议模型"""
    CATEGORY_CHOICES = [
        ('complaint', '投诉'),
        ('suggestion', '建议'),
        ('praise', '表扬'),
    ]
    
    content = models.TextField('内容', max_length=1000)
    category = models.CharField('类别', max_length=20, choices=CATEGORY_CHOICES, default='suggestion')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    is_public = models.BooleanField('是否公开', default=True)
    is_processed = models.BooleanField('是否已处理', default=False)
    contact_info = models.CharField('联系方式', max_length=100, blank=True)
    admin_note = models.TextField('管理员备注', blank=True)
    
    class Meta:
        verbose_name = '意见建议'
        verbose_name_plural = '意见建议'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
