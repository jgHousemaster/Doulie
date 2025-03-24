import React from 'react';
import { 
  DocumentCard, 
  DocumentCardTitle, 
  DocumentCardImage, 
  DocumentCardDetails,
  Text,
  Stack,
  Rating
} from '@fluentui/react';

const MovieCard = ({ movie, onClick }) => {
  return (
    <DocumentCard 
      onClick={() => onClick(movie.id)} 
      styles={{ 
        root: { 
          maxWidth: 320, 
          minWidth: 280, 
          margin: '10px', 
          cursor: 'pointer',
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
        } 
      }}
    >
      <DocumentCardImage 
        height={180} 
        imageFit="cover"
        imageSrc={movie.image || 'https://via.placeholder.com/300x180?text=无图片'}
      />
      <DocumentCardDetails>
        <DocumentCardTitle 
          title={movie.title} 
          shouldTruncate 
          styles={{ root: { padding: '12px 12px 4px 12px' } }}
        />
        <Stack horizontal tokens={{ padding: '0 12px 8px 12px' }}>
          <Stack.Item grow>
            <Text variant="small">
              {movie.time ? new Date(movie.time).toLocaleDateString() : '未知日期'}
            </Text>
          </Stack.Item>
          <Stack.Item>
            {movie.rating && (
              <Stack horizontal verticalAlign="center">
                <Rating 
                  max={5}
                  rating={parseFloat(movie.rating) / 2} 
                  readOnly 
                  size={Rating.Size.Small}
                />
                <Text variant="medium" styles={{ root: { marginLeft: 4 } }}>
                  {movie.rating}
                </Text>
              </Stack>
            )}
          </Stack.Item>
        </Stack>
      </DocumentCardDetails>
    </DocumentCard>
  );
};

export default MovieCard; 