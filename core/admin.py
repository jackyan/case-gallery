from django.contrib import admin
from .models import FoodItem, Vote, Suggestion


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    """食物项目管理"""
    list_display = ['name', 'meal_type', 'is_active', 'created_at', 'get_today_votes']
    list_filter = ['meal_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['meal_type', 'name']
    
    fieldsets = [
        ('基本信息', {
            'fields': ['name', 'meal_type', 'description']
        }),
        ('图片', {
            'fields': ['image']
        }),
        ('状态', {
            'fields': ['is_active']
        }),
    ]
    
    def get_today_votes(self, obj):
        """获取今日投票数"""
        from django.utils import timezone
        from datetime import timedelta
        tomorrow = (timezone.now() + timedelta(days=1)).date()
        return obj.get_vote_count(tomorrow)
    get_today_votes.short_description = '明日投票数'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """投票记录管理"""
    list_display = ['food', 'vote_for_date', 'ip_address', 'voted_at']
    list_filter = ['vote_for_date', 'voted_at', 'food__meal_type']
    search_fields = ['food__name', 'ip_address']
    date_hierarchy = 'voted_at'
    readonly_fields = ['voted_at']
    
    def has_add_permission(self, request):
        """禁止手动添加投票"""
        return False


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    """意见建议管理"""
    list_display = ['get_short_content', 'category', 'is_processed', 'is_public', 'created_at']
    list_filter = ['category', 'is_processed', 'is_public', 'created_at']
    search_fields = ['content', 'contact_info']
    list_editable = ['is_processed', 'is_public']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = [
        ('内容信息', {
            'fields': ['category', 'content', 'contact_info']
        }),
        ('状态管理', {
            'fields': ['is_public', 'is_processed', 'admin_note']
        }),
        ('时间信息', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]
    
    def get_short_content(self, obj):
        """显示简短内容"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_short_content.short_description = '内容摘要'
    
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    
    def mark_as_processed(self, request, queryset):
        """批量标记为已处理"""
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'成功标记 {updated} 条记录为已处理')
    mark_as_processed.short_description = '标记为已处理'
    
    def mark_as_unprocessed(self, request, queryset):
        """批量标记为未处理"""
        updated = queryset.update(is_processed=False)
        self.message_user(request, f'成功标记 {updated} 条记录为未处理')
    mark_as_unprocessed.short_description = '标记为未处理'
