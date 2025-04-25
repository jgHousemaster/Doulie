# 豆瓣电影收藏助手

## 使用方法

### 初始化

`/main.py` 中：修改第 133 行 `doulist_id` 为你的豆瓣豆列 ID。

运行 `python main.py` 爬取豆瓣豆列电影信息，并存储到数据库。（每次运行都会销毁旧的数据库并重新爬取）

### 运行后端

运行 `python app.py` 启动后端服务。

### 运行前端

运行 `cd frontend && npm start` 启动前端服务。

### 停止服务

Ctrl + C 终止前后端程序。

## 技术栈

- 后端：Python + Flask
- 前端：React + TypeScript + Fluent UI
- 数据库：SQLite

## 项目结构

根目录：

- `main.py`：爬取豆瓣豆列电影信息，并存储到数据库。
- `app.py`：启动后端服务。
- `frontend`：前端项目目录。

frontend 目录：

- `src`：前端源码目录。
- `public`：静态文件目录。
- `package.json`：前端项目配置文件。
- `tsconfig.json`：TypeScript 配置文件。
