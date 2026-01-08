# API 接口文档

本文档详细说明了食堂意见建议平台的后端 API 接口。所有接口均基于 HTTP 协议，返回 JSON 格式数据。

## 通用说明

*   **基准 URL**: 默认为 `http://localhost:8000`
*   **请求头**:
    *   POST 请求必须包含 `X-CSRFToken` 头部，值为 cookie 中的 `csrftoken`。
    *   `Content-Type: application/x-www-form-urlencoded` 或 `multipart/form-data` (本项目主要使用 Form Data)。
*   **响应格式**:
    *   成功: `{"success": true, "message": "...", ...}` (部分 GET 接口直接返回数据对象)
    *   失败: `{"success": false, "error": "错误信息"}`

---

## 1. 获取排行榜数据

获取早餐、午餐、晚餐的实时投票排名数据。

*   **Endpoint**: `/api/rankings/`
*   **Method**: `GET`
*   **Auth**: 不需要

### 响应参数

返回一个对象，包含三个数组：`breakfast`, `lunch`, `dinner`。每个数组元素包含：

| 字段    | 类型           | 说明     |
| :------ | :------------- | :------- |
| `id`    | int            | 食物 ID  |
| `name`  | string         | 食物名称 |
| `votes` | int            | 当前票数 |
| `image` | string \| null | 图片 URL |

### 响应示例

```json
{
    "breakfast": [
        {
            "id": 1,
            "name": "小笼包",
            "votes": 45,
            "image": "/media/foods/xiaolongbao.jpg"
        },
        {
            "id": 2,
            "name": "豆浆",
            "votes": 20,
            "image": null
        }
    ],
    "lunch": [ ... ],
    "dinner": [ ... ]
}
```

---

## 2. 获取词云数据

获取基于用户建议生成的热词及其权重。

*   **Endpoint**: `/api/wordcloud/`
*   **Method**: `GET`
*   **Auth**: 不需要

### 响应参数

| 字段    | 类型  | 说明     |
| :------ | :---- | :------- |
| `words` | array | 词汇列表 |

每项包含：
*   `text`: 关键词文本
*   `weight`: 权重值（用于前端决定字体大小）

### 响应示例

```json
{
    "words": [
        {"text": "好吃", "weight": 85.5},
        {"text": "食堂", "weight": 62.1},
        {"text": "太咸", "weight": 40.0}
    ]
}
```

---

## 3. 提交投票

为特定食物投票。

*   **Endpoint**: `/api/vote/`
*   **Method**: `POST`
*   **Auth**: 不需要（基于 IP 限制）

### 请求参数

| 参数名    | 类型 | 必选 | 说明          |
| :-------- | :--- | :--- | :------------ |
| `food_id` | int  | 是   | 目标食物的 ID |

### 响应示例

**成功:**
```json
{
    "success": true,
    "message": "投票成功！"
}
```

**失败 (重复投票):**
```json
{
    "success": false,
    "error": "您今天已经为这个食物投过票了"
}
```

---

## 4. 提交意见建议

提交用户的文本反馈。

*   **Endpoint**: `/api/suggestion/`
*   **Method**: `POST`
*   **Auth**: 不需要

### 请求参数

| 参数名         | 类型   | 必选 | 说明                                            |
| :------------- | :----- | :--- | :---------------------------------------------- |
| `content`      | string | 是   | 建议内容 (1-1000字)                             |
| `category`     | string | 否   | 类别: `suggestion`(默认), `complaint`, `praise` |
| `contact_info` | string | 否   | 联系方式                                        |

### 响应示例

**成功:**
```json
{
    "success": true,
    "message": "提交成功，感谢您的反馈！"
}
```

**失败 (内容为空):**
```json
{
    "success": false,
    "error": "内容不能为空"
}
```
