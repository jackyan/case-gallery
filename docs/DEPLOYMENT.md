# 生产环境部署指南

本文档介绍如何将食堂意见建议平台部署到 Linux 生产环境。推荐使用 **Nginx** 作为反向代理服务器，配合 **Gunicorn** 作为 WSGI 容器。

## 1. 基础环境准备

确保服务器已安装：
- Python 3.10+
- SQLite3 (或 PostgreSQL/MySQL)
- Nginx
- Git

## 2. 代码获取与依赖安装

```bash
# 1. 克隆代码
git clone <repository_url>
cd case-gallery

# 2. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
pip install gunicorn  # 生产环境需要额外安装 gunicorn
```

## 3. 环境变量配置

在生产环境中，**切勿**直接在代码中使用硬编码的 `SECRET_KEY` 或开启 `DEBUG=True`。
建议使用环境变量或 `.env` 文件（需要安装 `python-dotenv`）。

修改 `config/settings.py`：

```python
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
ALLOWED_HOSTS = ['yourdomain.com', '127.0.0.1']
```

## 4. 静态文件收集

生产环境不能由 Django 直接提供静态文件，需要收集到统一目录由 Nginx 提供。

```bash
# 收集静态文件
python manage.py collectstatic
```

此命令会将所有 CSS/JS 图片收集到 `staticfiles/` 目录。

## 5. Gunicorn 配置

创建一个 systemd 服务文件来管理 Gunicorn 进程。

文件: `/etc/systemd/system/gunicorn.service`

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/path/to/case-gallery
ExecStart=/path/to/case-gallery/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/path/to/case-gallery/config.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

启动并启用服务：
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 6. Nginx 配置

配置 Nginx 代理请求到 Gunicorn，并处理静态文件。

文件: `/etc/nginx/sites-available/case-gallery`

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    # 静态文件
    location /static/ {
        alias /path/to/case-gallery/staticfiles/;
    }

    # 媒体文件 (用户上传的图片)
    location /media/ {
        alias /path/to/case-gallery/media/;
    }

    # 代理到 Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/case-gallery/config.sock;
    }
}
```

启用配置并重启 Nginx：
```bash
sudo ln -s /etc/nginx/sites-available/case-gallery /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## 7. Docker 部署 (可选)

如果偏好容器化部署，可以使用以下 `Dockerfile`。

**Dockerfile**:
```dockerfile
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 复制项目代码
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

**运行 Docker**:
```bash
docker build -t case-gallery .
docker run -d -p 8000:8000 case-gallery
```
> 注意：Docker 部署时仍建议在前方配置 Nginx 处理 SSL 和静态文件，或使用 Docker Compose 编排。
