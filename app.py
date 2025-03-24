from flask import Flask, jsonify, request, Response
from database import MovieDatabase
import random
import requests

# 创建 Flask 应用实例
app = Flask(__name__)

# 添加根路径处理器
@app.route('/', methods=['GET'])
def index():
    """API根路径，提供API信息"""
    return jsonify({
        'name': '豆列电影库 API',
        'version': '1.0',
        'endpoints': {
            'movies_list': '/api/movies',
            'movie_detail': '/api/movies/<movie_id>',
            'random_movie': '/api/movies/random',
            'health_check': '/api/health',
            'proxy_image': '/api/proxy-image'
        },
        'documentation': '访问 /api/movies 获取电影列表'
    })

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """获取电影列表，支持分页和排序"""
    # 获取查询参数
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    sort_by = request.args.get('sort_by', 'time')  # 默认按时间排序
    order = request.args.get('order', 'desc')  # 默认降序
    
    # 计算偏移量
    offset = (page - 1) * per_page
    
    # 连接数据库
    db = MovieDatabase()
    try:
        # 构建排序条件
        if sort_by not in ['time', 'rating', 'title']:
            sort_by = 'time'  # 默认按时间排序
            
        if order not in ['asc', 'desc']:
            order = 'desc'  # 默认降序
        
        # 获取电影总数
        total_count = db.count_movies()
        
        # 获取排序后的电影列表
        movies = db.get_sorted_movies(sort_by, order, per_page, offset)
        
        # 计算总页数
        total_pages = (total_count + per_page - 1) // per_page
        
        # 在返回响应前添加调试代码
        for movie in movies:
            print(f"Movie: {movie['title']}, Image URL: {movie['image']}")
        
        # 构建响应数据
        response = {
            'movies': movies,
            'pagination': {
                'total_count': total_count,
                'total_pages': total_pages,
                'current_page': page,
                'per_page': per_page
            },
            'sort': {
                'sort_by': sort_by,
                'order': order
            }
        }
        
        return jsonify(response)
    finally:
        db.close()

@app.route('/api/movies/random', methods=['GET'])
def get_random_movie():
    """随机获取一部电影"""
    db = MovieDatabase()
    try:
        # 获取所有电影ID
        movie_ids = db.get_all_movie_ids()
        
        if not movie_ids:
            return jsonify({'error': '数据库中没有电影'}), 404
            
        # 随机选择一个ID
        random_id = random.choice(movie_ids)
        
        # 获取电影详情
        movie = db.get_movie_by_id(random_id)
        
        if not movie:
            return jsonify({'error': '获取电影信息失败'}), 500
            
        return jsonify({'movie': movie})
    finally:
        db.close()

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie_detail(movie_id):
    """获取电影详情"""
    db = MovieDatabase()
    try:
        movie = db.get_movie_by_id(movie_id)
        
        if not movie:
            return jsonify({'error': '电影不存在'}), 404
            
        return jsonify({'movie': movie})
    finally:
        db.close()

# 添加一个简单的健康检查接口
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

# 启用CORS（跨域资源共享）
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/api/proxy-image', methods=['GET'])
def proxy_image():
    """代理图片请求，绕过CORS限制"""
    url = request.args.get('url')
    if not url:
        return jsonify({'error': '缺少URL参数'}), 400
        
    try:
        # 添加请求头，模拟浏览器请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://movie.douban.com/',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        
        response = requests.get(url, headers=headers, stream=True)
        print(f"Proxy image response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Failed to fetch image: {url}")
            return jsonify({'error': '无法获取图片'}), 404
            
        # 打印响应头信息，帮助调试
        print(f"Response headers: {dict(response.headers)}")
            
        return Response(
            response.content, 
            content_type=response.headers.get('content-type', 'image/jpeg'),
            headers={
                'Cache-Control': 'public, max-age=86400',  # 缓存一天
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        print(f"Error proxying image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 