from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
import jieba.analyse
from collections import Counter

from .models import FoodItem, Vote, Suggestion


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    """首页视图"""
    return render(request, 'index.html')


@require_GET
def get_rankings(request):
    """获取排行榜数据 API"""
    tomorrow = (timezone.now() + timedelta(days=1)).date()
    
    # 获取三个餐点的排行榜
    rankings = {}
    
    # 早餐前3名
    breakfast_items = FoodItem.objects.filter(
        meal_type='breakfast', 
        is_active=True
    ).annotate(
        vote_count=Count('votes', filter=Q(votes__vote_for_date=tomorrow))
    ).order_by('-vote_count')[:3]
    
    rankings['breakfast'] = [
        {
            'id': item.id,
            'name': item.name,
            'votes': item.vote_count,
            'image': item.image.url if item.image else None
        }
        for item in breakfast_items
    ]
    
    # 午餐前5名
    lunch_items = FoodItem.objects.filter(
        meal_type='lunch',
        is_active=True
    ).annotate(
        vote_count=Count('votes', filter=Q(votes__vote_for_date=tomorrow))
    ).order_by('-vote_count')[:5]
    
    rankings['lunch'] = [
        {
            'id': item.id,
            'name': item.name,
            'votes': item.vote_count,
            'image': item.image.url if item.image else None
        }
        for item in lunch_items
    ]
    
    # 晚餐前5名
    dinner_items = FoodItem.objects.filter(
        meal_type='dinner',
        is_active=True
    ).annotate(
        vote_count=Count('votes', filter=Q(votes__vote_for_date=tomorrow))
    ).order_by('-vote_count')[:5]
    
    rankings['dinner'] = [
        {
            'id': item.id,
            'name': item.name,
            'votes': item.vote_count,
            'image': item.image.url if item.image else None
        }
        for item in dinner_items
    ]
    
    return JsonResponse(rankings)


@require_GET
def get_wordcloud(request):
    """获取词云数据 API"""
    # 获取最近30天的公开建议
    cutoff_date = timezone.now() - timedelta(days=30)
    suggestions = Suggestion.objects.filter(
        is_public=True,
        created_at__gte=cutoff_date
    ).values_list('content', flat=True)
    
    # 合并所有文本
    all_text = ' '.join(suggestions)
    
    # 使用 jieba 提取关键词
    keywords = jieba.analyse.extract_tags(all_text, topK=30, withWeight=True)
    
    # 转换为前端需要的格式
    wordcloud_data = [
        {'text': word, 'weight': weight * 100}
        for word, weight in keywords
    ]
    
    return JsonResponse({'words': wordcloud_data})


@ensure_csrf_cookie
def vote_page(request):
    """投票页面"""
    # 获取所有活跃的食物，按餐点分类
    breakfast_foods = FoodItem.objects.filter(meal_type='breakfast', is_active=True)
    lunch_foods = FoodItem.objects.filter(meal_type='lunch', is_active=True)
    dinner_foods = FoodItem.objects.filter(meal_type='dinner', is_active=True)
    
    context = {
        'breakfast_foods': breakfast_foods,
        'lunch_foods': lunch_foods,
        'dinner_foods': dinner_foods,
    }
    return render(request, 'vote.html', context)


@require_POST
def submit_vote(request):
    """提交投票 API"""
    try:
        food_id = request.POST.get('food_id')
        if not food_id:
            return JsonResponse({'success': False, 'error': '缺少食物ID'})
        
        food = FoodItem.objects.get(id=food_id, is_active=True)
        ip_address = get_client_ip(request)
        tomorrow = (timezone.now() + timedelta(days=1)).date()
        
        # 检查是否已经投过票
        existing_vote = Vote.objects.filter(
            food=food,
            ip_address=ip_address,
            vote_for_date=tomorrow
        ).exists()
        
        if existing_vote:
            return JsonResponse({
                'success': False,
                'error': '您今天已经为这个食物投过票了'
            })
        
        # 创建投票记录
        Vote.objects.create(
            food=food,
            ip_address=ip_address,
            vote_for_date=tomorrow
        )
        
        return JsonResponse({
            'success': True,
            'message': '投票成功！'
        })
        
    except FoodItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': '食物不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@ensure_csrf_cookie
def suggestion_page(request):
    """意见建议提交页面"""
    return render(request, 'suggestion.html')


@require_POST
def submit_suggestion(request):
    """提交意见建议 API"""
    try:
        content = request.POST.get('content', '').strip()
        category = request.POST.get('category', 'suggestion')
        contact_info = request.POST.get('contact_info', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': '内容不能为空'})
        
        if len(content) > 1000:
            return JsonResponse({'success': False, 'error': '内容不能超过1000字'})
        
        # 创建建议记录
        Suggestion.objects.create(
            content=content,
            category=category,
            contact_info=contact_info
        )
        
        return JsonResponse({
            'success': True,
            'message': '提交成功，感谢您的反馈！'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
