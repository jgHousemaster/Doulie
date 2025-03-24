import React, { useState, useEffect } from 'react';
import {
  Stack,
  Text,
  Image,
  Rating,
  Spinner,
  MessageBar,
  MessageBarType,
  IconButton,
  Separator
} from '@fluentui/react';
import { fetchMovieDetail } from '../api';

const MovieDetail = ({ movieId, onBack }) => {
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMovie = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchMovieDetail(movieId);
        setMovie(data.movie);
      } catch (err) {
        setError('加载电影详情失败，请稍后重试');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadMovie();
  }, [movieId]);

  if (loading) {
    return (
      <Stack horizontalAlign="center" tokens={{ padding: 20 }}>
        <Spinner label="正在加载电影详情..." />
      </Stack>
    );
  }

  if (error) {
    return (
      <MessageBar messageBarType={MessageBarType.error}>
        {error}
      </MessageBar>
    );
  }

  if (!movie) {
    return (
      <MessageBar messageBarType={MessageBarType.warning}>
        未找到电影信息
      </MessageBar>
    );
  }

  return (
    <Stack tokens={{ childrenGap: 16, padding: 16 }}>
      <Stack horizontal verticalAlign="center">
        <IconButton
          iconProps={{ iconName: 'Back' }}
          onClick={onBack}
          styles={{ root: { marginRight: 8 } }}
        />
        <Text variant="xLarge">{movie.title}</Text>
      </Stack>

      <Separator />

      <Stack horizontal tokens={{ childrenGap: 20 }} wrap>
        <Stack.Item>
          <Image
            src={movie.image || 'https://via.placeholder.com/300x450?text=无图片'}
            alt={movie.title}
            width={240}
            height={360}
            imageFit="cover"
          />
        </Stack.Item>

        <Stack.Item grow styles={{ root: { minWidth: 300, maxWidth: 600 } }}>
          <Stack tokens={{ childrenGap: 12 }}>
            {movie.rating && (
              <Stack horizontal verticalAlign="center" tokens={{ childrenGap: 8 }}>
                <Text variant="medium">评分:</Text>
                <Rating
                  max={5}
                  rating={parseFloat(movie.rating) / 2}
                  readOnly
                />
                <Text variant="large" styles={{ root: { fontWeight: 'bold' } }}>
                  {movie.rating}
                </Text>
              </Stack>
            )}

            <Stack tokens={{ childrenGap: 8 }}>
              <Text variant="medium">添加时间:</Text>
              <Text>{movie.time || '未知'}</Text>
            </Stack>

            <Stack tokens={{ childrenGap: 8 }}>
              <Text variant="medium">简介:</Text>
              <Text>
                {movie.abstract ? (
                  movie.abstract.split('\n').map((line, i) => (
                    <React.Fragment key={i}>
                      {line}
                      <br />
                    </React.Fragment>
                  ))
                ) : (
                  '暂无简介'
                )}
              </Text>
            </Stack>
          </Stack>
        </Stack.Item>
      </Stack>
    </Stack>
  );
};

export default MovieDetail; 