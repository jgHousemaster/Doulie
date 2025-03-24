import requests
from bs4 import BeautifulSoup
import time
from database import MovieDatabase

def parse_movie_item(item):
    """解析单个电影条目的详细信息"""
    movie_info = {}
    
    try:
        # 获取标题 (从 title div 的 a 标签中获取)
        title_div = item.find('div', class_='title')
        if title_div and title_div.a:
            movie_info['title'] = title_div.a.text.strip()
        
        # 获取评分 (直接查找 rating_nums class)
        rating = item.find('span', class_='rating_nums')
        if rating:
            movie_info['rating'] = rating.text.strip()
        
        # 获取海报图片链接
        post_div = item.find('div', class_='post')
        if post_div and post_div.img:
            movie_info['image'] = post_div.img['src']
        
        # 获取简介信息 (保留原始格式)
        abstract = item.find('div', class_='abstract')
        if abstract:
            movie_info['abstract'] = abstract.get_text(strip=True, separator='\n')
        
        # 获取时间 (在 actions div 下的 time 标签)
        time_tag = item.find('div', class_='actions').find('time', class_='time')
        if time_tag:
            movie_info['time'] = time_tag.text.strip()

        return movie_info
        
    except Exception as e:
        print(f'解析电影信息时发生错误: {e}')
        return None

def fetch_doulist_movies(doulist_id, max_pages=10):
    """获取豆列中的所有电影信息并存储到数据库"""
    # 初始化数据库
    db = MovieDatabase()
    
    # 重建表（先删除再创建）
    db.drop_table()
    db.create_table()
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    base_url = f'https://www.douban.com/doulist/{doulist_id}/'
    total_movies = 0
    
    try:
        for page in range(max_pages):
            # 构建当前页面的URL
            url = f'{base_url}?start={page * 25}&sort=time&playable=0&sub_type='
            print(f'正在获取第 {page + 1} 页...')
            
            # 添加延时避免请求过快
            time.sleep(2)
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_='doulist-item')
            
            # 如果没有找到电影条目，说明已经到达最后一页
            if not items:
                print('没有更多电影了')
                break
            
            # 处理当前页面的每个电影条目
            for item in items:
                movie_info = parse_movie_item(item)
                if movie_info:
                    # 将电影信息存入数据库
                    movie_id = db.insert_movie(movie_info, doulist_id)
                    if movie_id:
                        total_movies += 1
                        print(f"已保存: {movie_info.get('title')} (ID: {movie_id})")
            
            print(f'第 {page + 1} 页处理完成')
            
    except Exception as e:
        print(f'获取电影列表时发生错误: {e}')
    finally:
        # 输出统计信息
        print(f'爬取完成，共保存 {total_movies} 部电影')
        
        # 关闭数据库连接
        db.close()
        
        return total_movies

def display_movies_from_db(doulist_id, limit=10):
    """从数据库中读取并显示电影信息"""
    db = MovieDatabase()
    try:
        # 获取指定豆列的电影
        movies = db.get_movies_by_doulist(doulist_id)
        
        print(f"\n数据库中的电影信息 (共 {len(movies)} 部):")
        print("=" * 50)
        
        # 显示前limit部电影的详细信息
        for i, movie in enumerate(movies[:limit]):
            print(f"[{i+1}] {movie['title']} - 评分: {movie['rating']}")
            print(f"添加时间: {movie['time']}")
            print(f"海报: {movie['image']}")
            print(f"简介: {movie['abstract']}")
            print("-" * 50)
            
        # 如果电影数量超过limit，显示省略信息
        if len(movies) > limit:
            print(f"... 还有 {len(movies) - limit} 部电影 ...")
            
    except Exception as e:
        print(f"显示电影信息时发生错误: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    doulist_id = '157902238'  # 豆列ID
    
    # 爬取电影信息并存储到数据库
    fetch_doulist_movies(doulist_id, max_pages=10)  # 限制最多爬取10页
    
    # 从数据库读取并显示电影信息
    display_movies_from_db(doulist_id)
