const API_BASE_URL = 'http://localhost:8080/api';

export const fetchMovies = async (page = 1, perPage = 10, sortBy = 'time', order = 'desc') => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/movies?page=${page}&per_page=${perPage}&sort_by=${sortBy}&order=${order}`
    );
    if (!response.ok) {
      throw new Error('获取电影列表失败');
    }
    return await response.json();
  } catch (error) {
    console.error('API错误:', error);
    throw error;
  }
};

export const fetchMovieDetail = async (movieId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/movies/${movieId}`);
    if (!response.ok) {
      throw new Error('获取电影详情失败');
    }
    return await response.json();
  } catch (error) {
    console.error('API错误:', error);
    throw error;
  }
};

export const fetchRandomMovie = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/movies/random`);
    if (!response.ok) {
      throw new Error('获取随机电影失败');
    }
    return await response.json();
  } catch (error) {
    console.error('API错误:', error);
    throw error;
  }
}; 