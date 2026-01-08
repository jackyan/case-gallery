# 投诉建议网站 - 实施方案

## 项目概述

本项目是一个基于 Django 的投诉和建议网站，主要功能包括：

1. **明天最想吃榜** - 实时更新的食物投票排行榜
   - 早饭前三名
   - 午饭前五名  
   - 晚饭前五名
   - 点击可进入投票页面

2. **意见和建议词云** - 动态滚动的词云展示
   - 从提交的意见建议中提取关键词
   - 点击可进入提交页面

## 技术栈

- **后端**: Django 4.x + SQLite3
- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **词云**: 使用 CSS 动画实现滚动效果
- **响应式设计**: 适配手机端和电脑端

---

## 数据库模型设计

### Core Application

#### [NEW] [models.py](core/models.py)

三个核心模型：

```python
# 1. FoodItem - 食物项目
class FoodItem(models.Model):
    MEAL_CHOICES = [
        ('breakfast', '早餐'),
        ('lunch', '午餐'),
        ('dinner', '晚餐'),
    ]
    name = models.CharField('食物名称', max_length=100)
    meal_type = models.CharField('餐点类型', max_length=20, choices=MEAL_CHOICES)
    image = models.ImageField('图片', upload_to='foods/', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否启用', default=True)

# 2. Vote - 投票记录
class Vote(models.Model):
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='votes')
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    voted_at = models.DateTimeField('投票时间', auto_now_add=True)
    vote_for_date = models.DateField('投票日期')  # 投票针对的日期（明天）

# 3. Suggestion - 意见建议
class Suggestion(models.Model):
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
```

---

## 后台管理

#### [NEW] [admin.py](core/admin.py)

为所有模型配置 Django Admin：

- **FoodItemAdmin**: 支持按餐点类型筛选、批量操作
- **VoteAdmin**: 显示投票统计、按日期筛选
- **SuggestionAdmin**: 分类筛选、处理状态管理

---

## 视图层设计

#### [NEW] [views.py](core/views.py)

| 视图                | URL                | 功能                   |
| ------------------- | ------------------ | ---------------------- |
| `index`             | `/`                | 首页，展示排行榜和词云 |
| `vote_page`         | `/vote/`           | 投票页面，分类展示食物 |
| `submit_vote`       | `/api/vote/`       | 投票 API (POST)        |
| `suggestion_page`   | `/suggestion/`     | 意见建议提交页面       |
| `submit_suggestion` | `/api/suggestion/` | 提交意见 API (POST)    |
| `get_rankings`      | `/api/rankings/`   | 获取排行榜数据 (GET)   |
| `get_wordcloud`     | `/api/wordcloud/`  | 获取词云数据 (GET)     |

---

## 前端页面设计

### 设计理念

- **现代简约风格**: 使用卡片式布局和圆角设计
- **响应式设计**: CSS Grid + Flexbox 实现自适应
- **动态效果**: CSS 动画 + JavaScript 实现滚动词云
- **色彩方案**: 
  - 早餐: 温暖的橙色系 `#FF9500`
  - 午餐: 活力的绿色系 `#34C759`
  - 晚餐: 安静的蓝色系 `#007AFF`

### 页面结构

#### [NEW] [templates/base.html](core/templates/base.html)

基础模板，包含：
- 响应式 meta 标签
- 全局样式和导航
- JavaScript 公共脚本

#### [NEW] [templates/index.html](core/templates/index.html)

首页布局：
```
┌─────────────────────────────────────────────────┐
│                   页面标题                        │
├─────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 早餐TOP3 │  │ 午餐TOP5 │  │ 晚餐TOP5 │      │
│  │ 🥇 XXX   │  │ 🥇 XXX   │  │ 🥇 XXX   │      │
│  │ 🥈 XXX   │  │ 🥈 XXX   │  │ 🥈 XXX   │      │
│  │ 🥉 XXX   │  │ 🥉 XXX   │  │ 🥉 XXX   │      │
│  │          │  │ 4. XXX   │  │ 4. XXX   │      │
│  │          │  │ 5. XXX   │  │ 5. XXX   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
├─────────────────────────────────────────────────┤
│                  意见建议词云                     │
│     建议    投诉    改进    服务    口味           │
│  (滚动动画展示关键词，点击进入提交页面)             │
└─────────────────────────────────────────────────┘
```

#### [NEW] [templates/vote.html](core/templates/vote.html)

投票页面：
- Tab 切换早/中/晚餐
- 食物卡片网格展示
- 点击投票，实时反馈

#### [NEW] [templates/suggestion.html](core/templates/suggestion.html)

意见建议页面：
- 类别选择（投诉/建议/表扬）
- 文本输入框
- 匿名提交

---

## 项目结构

```
case-gallery/
├── manage.py
├── config/                      # Django 项目配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                        # 核心应用
│   ├── __init__.py
│   ├── admin.py                 # Admin 配置
│   ├── apps.py
│   ├── models.py                # 数据模型
│   ├── views.py                 # 视图
│   ├── urls.py                  # URL 路由
│   ├── templates/               # 模板
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── vote.html
│   │   └── suggestion.html
│   └── static/                  # 静态文件
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── static/                      # 全局静态文件
├── media/                       # 上传文件
├── db.sqlite3                   # SQLite 数据库
└── requirements.txt
```

---

## 验证计划

### 自动化测试
```bash
# 1. 运行 Django 开发服务器
python manage.py runserver

# 2. 检查数据库迁移
python manage.py check

# 3. 浏览器测试各页面
```

### 手动验证

1. **首页功能**
   - 排行榜数据正确显示
   - 词云动态滚动
   - 点击跳转正常

2. **投票功能**
   - 分类切换正常
   - 投票提交成功
   - 排行榜实时更新

3. **意见建议功能**
   - 表单提交成功
   - 词云数据更新

4. **响应式设计**
   - 手机端页面布局正常
   - 点击交互友好

---

## 依赖清单

```
Django>=4.2
Pillow>=10.0  # 处理图片上传
jieba>=0.42   # 中文分词（用于词云关键词提取）
```
