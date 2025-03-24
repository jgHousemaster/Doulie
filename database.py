import sqlite3
import os

class MovieDatabase:
    def __init__(self, db_file='movies.db'):
        """初始化数据库连接"""
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """连接到数据库"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"数据库连接错误: {e}")
            return False
            
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            
    def create_table(self):
        """创建电影信息表"""
        if not self.conn:
            if not self.connect():
                return False
                
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                rating TEXT,
                image TEXT,
                abstract TEXT,
                time TEXT,
                doulist_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"创建表错误: {e}")
            return False
            
    def drop_table(self):
        """删除电影信息表"""
        if not self.conn:
            if not self.connect():
                return False
                
        try:
            self.cursor.execute('DROP TABLE IF EXISTS movies')
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"删除表错误: {e}")
            return False
            
    def insert_movie(self, movie_data, doulist_id=None):
        """插入一条电影记录"""
        if not self.conn:
            if not self.connect():
                return False
                
        try:
            # 准备SQL语句和参数
            sql = '''
            INSERT INTO movies (title, rating, image, abstract, time, doulist_id)
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (
                movie_data.get('title', ''),
                movie_data.get('rating', ''),
                movie_data.get('image', ''),
                movie_data.get('abstract', ''),
                movie_data.get('time', ''),
                doulist_id
            )
            
            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"插入数据错误: {e}")
            return False
            
    def update_movie(self, movie_id, movie_data):
        """更新电影记录"""
        if not self.conn:
            if not self.connect():
                return False
                
        try:
            # 准备SQL语句和参数
            sql = '''
            UPDATE movies
            SET title = ?, rating = ?, image = ?, abstract = ?, time = ?
            WHERE id = ?
            '''
            params = (
                movie_data.get('title', ''),
                movie_data.get('rating', ''),
                movie_data.get('image', ''),
                movie_data.get('abstract', ''),
                movie_data.get('time', ''),
                movie_id
            )
            
            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"更新数据错误: {e}")
            return False
            
    def delete_movie(self, movie_id):
        """删除电影记录"""
        if not self.conn:
            if not self.connect():
                return False
                
        try:
            self.cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"删除数据错误: {e}")
            return False
            
    def get_movie_by_id(self, movie_id):
        """根据ID获取电影信息"""
        if not self.conn:
            if not self.connect():
                return None
                
        try:
            self.cursor.execute('''
            SELECT id, title, rating, image, abstract, time, doulist_id, created_at
            FROM movies
            WHERE id = ?
            ''', (movie_id,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'rating': row[2],
                    'image': row[3],
                    'abstract': row[4],
                    'time': row[5],
                    'doulist_id': row[6],
                    'created_at': row[7]
                }
            return None
        except sqlite3.Error as e:
            print(f"查询数据错误: {e}")
            return None
            
    def get_movies_by_doulist(self, doulist_id):
        """获取指定豆列的所有电影"""
        if not self.conn:
            if not self.connect():
                return []
                
        try:
            self.cursor.execute('''
            SELECT id, title, rating, image, abstract, time, doulist_id, created_at
            FROM movies
            WHERE doulist_id = ?
            ORDER BY time DESC
            ''', (doulist_id,))
            
            movies = []
            for row in self.cursor.fetchall():
                movies.append({
                    'id': row[0],
                    'title': row[1],
                    'rating': row[2],
                    'image': row[3],
                    'abstract': row[4],
                    'time': row[5],
                    'doulist_id': row[6],
                    'created_at': row[7]
                })
            return movies
        except sqlite3.Error as e:
            print(f"查询数据错误: {e}")
            return []
            
    def get_all_movies(self, limit=100, offset=0):
        """获取所有电影，支持分页"""
        if not self.conn:
            if not self.connect():
                return []
                
        try:
            self.cursor.execute('''
            SELECT id, title, rating, image, abstract, time, doulist_id, created_at
            FROM movies
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            movies = []
            for row in self.cursor.fetchall():
                movies.append({
                    'id': row[0],
                    'title': row[1],
                    'rating': row[2],
                    'image': row[3],
                    'abstract': row[4],
                    'time': row[5],
                    'doulist_id': row[6],
                    'created_at': row[7]
                })
            return movies
        except sqlite3.Error as e:
            print(f"查询数据错误: {e}")
            return []
            
    def search_movies(self, keyword):
        """搜索电影"""
        if not self.conn:
            if not self.connect():
                return []
                
        try:
            # 在标题和简介中搜索关键词
            self.cursor.execute('''
            SELECT id, title, rating, image, abstract, time, doulist_id, created_at
            FROM movies
            WHERE title LIKE ? OR abstract LIKE ?
            ORDER BY created_at DESC
            ''', (f'%{keyword}%', f'%{keyword}%'))
            
            movies = []
            for row in self.cursor.fetchall():
                movies.append({
                    'id': row[0],
                    'title': row[1],
                    'rating': row[2],
                    'image': row[3],
                    'abstract': row[4],
                    'time': row[5],
                    'doulist_id': row[6],
                    'created_at': row[7]
                })
            return movies
        except sqlite3.Error as e:
            print(f"搜索数据错误: {e}")
            return []
            
    def count_movies(self):
        """统计电影总数"""
        if not self.conn:
            if not self.connect():
                return 0
                
        try:
            self.cursor.execute('SELECT COUNT(*) FROM movies')
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"统计数据错误: {e}")
            return 0

    def get_sorted_movies(self, sort_by='time', order='desc', limit=100, offset=0):
        """获取排序后的电影列表，支持分页"""
        if not self.conn:
            if not self.connect():
                return []
            
        try:
            # 验证排序字段
            if sort_by not in ['time', 'rating', 'title']:
                sort_by = 'time'
            
            # 验证排序方向
            if order not in ['asc', 'desc']:
                order = 'desc'
            
            # 特殊处理评分排序（需要转换为数值）
            if sort_by == 'rating':
                # 使用CAST将评分转换为数值进行排序
                self.cursor.execute(f'''
                SELECT id, title, rating, image, abstract, time, doulist_id, created_at
                FROM movies
                ORDER BY CAST(rating AS REAL) {order}, time DESC
                LIMIT ? OFFSET ?
                ''', (limit, offset))
            else:
                # 其他字段正常排序
                self.cursor.execute(f'''
                SELECT id, title, rating, image, abstract, time, doulist_id, created_at
                FROM movies
                ORDER BY {sort_by} {order}
                LIMIT ? OFFSET ?
                ''', (limit, offset))
            
            movies = []
            for row in self.cursor.fetchall():
                movies.append({
                    'id': row[0],
                    'title': row[1],
                    'rating': row[2],
                    'image': row[3],
                    'abstract': row[4],
                    'time': row[5],
                    'doulist_id': row[6],
                    'created_at': row[7]
                })
            return movies
        except sqlite3.Error as e:
            print(f"查询数据错误: {e}")
            return []

    def get_all_movie_ids(self):
        """获取所有电影ID列表"""
        if not self.conn:
            if not self.connect():
                return []
            
        try:
            self.cursor.execute('SELECT id FROM movies')
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"获取电影ID错误: {e}")
            return []

# 简单测试代码
if __name__ == "__main__":
    # 创建数据库实例
    db = MovieDatabase()
    
    # 创建表
    db.create_table()
    
    # 插入测试数据
    test_movie = {
        'title': '测试电影',
        'rating': '8.5',
        'image': 'https://example.com/image.jpg',
        'abstract': '导演: 测试导演\n主演: 测试演员\n年份: 2023',
        'time': '2023-04-01 12:00:00'
    }
    
    movie_id = db.insert_movie(test_movie, '123456')
    print(f"插入电影ID: {movie_id}")
    
    # 查询电影
    movie = db.get_movie_by_id(movie_id)
    print("查询结果:", movie)
    
    # 更新电影
    test_movie['rating'] = '9.0'
    db.update_movie(movie_id, test_movie)
    
    # 再次查询
    movie = db.get_movie_by_id(movie_id)
    print("更新后结果:", movie)
    
    # 关闭连接
    db.close()
