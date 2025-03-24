import React, { useState, useEffect } from 'react';
import {
  Stack,
  Text,
  Image,
  Rating,
  Spinner,
  MessageBar,
  MessageBarType,
  PrimaryButton,
  IconButton,
  Separator
} from '@fluentui/react';
import { fetchRandomMovie } from '../api';

const RandomMovie = ({ onBack, onSelectMovie }) => {
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadRandomMovie = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchRandomMovie();
      setMovie(data.movie);
    } catch (err) {
      setError('加载随机电影失败，请稍后重试');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRandomMovie();
  }, []);

  if (loading) {
    return (
      <Stack horizontalAlign="center" tokens={{ padding: 20 }}>
        <Spinner label="正在加载随机电影..." />
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
        <Text variant="xLarge">随机推荐: {movie.title}</Text>
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

            <Stack horizontal tokens={{ childrenGap: 8 }} styles={{ root: { marginTop: 16 } }}>
              <PrimaryButton 
                text="查看详情" 
                onClick={() => onSelectMovie(movie.id)} 
              />
              <PrimaryButton 
                text="再来一部" 
                onClick={loadRandomMovie} 
                iconProps={{ iconName: 'Refresh' }}
              />
            </Stack>
          </Stack>
        </Stack.Item>
      </Stack>
    </Stack>
  );
};

export default RandomMovie; 