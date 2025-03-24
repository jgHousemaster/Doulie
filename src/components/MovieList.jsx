import React, { useState, useEffect } from 'react';
import { 
  Stack, 
  Dropdown, 
  Spinner, 
  MessageBar, 
  MessageBarType,
  Text,
  Pagination,
  PrimaryButton,
  CommandBar
} from '@fluentui/react';
import { fetchMovies } from '../api';
import MovieCard from './MovieCard';

const sortOptions = [
  { key: 'time-desc', text: '时间 (最新)', data: { sortBy: 'time', order: 'desc' } },
  { key: 'time-asc', text: '时间 (最早)', data: { sortBy: 'time', order: 'asc' } },
  { key: 'rating-desc', text: '评分 (高到低)', data: { sortBy: 'rating', order: 'desc' } },
  { key: 'rating-asc', text: '评分 (低到高)', data: { sortBy: 'rating', order: 'asc' } },
  { key: 'title-asc', text: '标题 (A-Z)', data: { sortBy: 'title', order: 'asc' } },
  { key: 'title-desc', text: '标题 (Z-A)', data: { sortBy: 'title', order: 'desc' } },
];

const MovieList = ({ onSelectMovie, onRandomMovie }) => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({ currentPage: 1, totalPages: 1 });
  const [sort, setSort] = useState({ sortBy: 'time', order: 'desc' });
  
  const loadMovies = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchMovies(
        pagination.currentPage, 
        10, 
        sort.sortBy, 
        sort.order
      );
      setMovies(data.movies);
      setPagination({
        currentPage: data.pagination.current_page,
        totalPages: data.pagination.total_pages
      });
    } catch (err) {
      setError('加载电影列表失败，请稍后重试');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMovies();
  }, [pagination.currentPage, sort]);

  const handleSortChange = (_, option) => {
    if (option) {
      setSort(option.data);
      setPagination({ ...pagination, currentPage: 1 });
    }
  };

  const handlePageChange = (page) => {
    setPagination({ ...pagination, currentPage: page });
  };

  const commandItems = [
    {
      key: 'refresh',
      text: '刷新',
      iconProps: { iconName: 'Refresh' },
      onClick: loadMovies
    },
    {
      key: 'random',
      text: '随机电影',
      iconProps: { iconName: 'Random' },
      onClick: onRandomMovie
    }
  ];

  return (
    <Stack tokens={{ childrenGap: 16, padding: 16 }}>
      <Stack horizontal horizontalAlign="space-between" verticalAlign="center">
        <Text variant="xLarge">豆列电影库</Text>
        <CommandBar items={commandItems} styles={{ root: { padding: 0 } }} />
      </Stack>
      
      <Stack horizontal horizontalAlign="end">
        <Dropdown
          label="排序方式"
          selectedKey={`${sort.sortBy}-${sort.order}`}
          onChange={handleSortChange}
          options={sortOptions}
          styles={{ root: { width: 200 } }}
        />
      </Stack>

      {error && (
        <MessageBar messageBarType={MessageBarType.error}>
          {error}
        </MessageBar>
      )}

      {loading ? (
        <Stack horizontalAlign="center" tokens={{ padding: 20 }}>
          <Spinner label="正在加载电影..." />
        </Stack>
      ) : (
        <>
          <Stack horizontal wrap horizontalAlign="center">
            {movies.length > 0 ? (
              movies.map(movie => (
                <MovieCard 
                  key={movie.id} 
                  movie={movie} 
                  onClick={onSelectMovie} 
                />
              ))
            ) : (
              <Text>没有找到电影</Text>
            )}
          </Stack>

          {pagination.totalPages > 1 && (
            <Pagination
              currentPage={pagination.currentPage}
              totalPages={pagination.totalPages}
              onChange={handlePageChange}
            />
          )}
        </>
      )}
    </Stack>
  );
};

export default MovieList; 