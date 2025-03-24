import React, { useState } from 'react';
import { initializeIcons, ThemeProvider, Stack } from '@fluentui/react';
import MovieList from './components/MovieList';
import MovieDetail from './components/MovieDetail';
import RandomMovie from './components/RandomMovie';

// 初始化 FluentUI 图标
initializeIcons();

const App = () => {
  const [view, setView] = useState('list');
  const [selectedMovieId, setSelectedMovieId] = useState(null);

  const handleSelectMovie = (movieId) => {
    setSelectedMovieId(movieId);
    setView('detail');
  };

  const handleBackToList = () => {
    setView('list');
  };

  const handleRandomMovie = () => {
    setView('random');
  };

  return (
    <ThemeProvider>
      <Stack styles={{ root: { minHeight: '100vh', backgroundColor: '#f3f2f1' } }}>
        {view === 'list' && (
          <MovieList 
            onSelectMovie={handleSelectMovie} 
            onRandomMovie={handleRandomMovie}
          />
        )}
        
        {view === 'detail' && selectedMovieId && (
          <MovieDetail 
            movieId={selectedMovieId} 
            onBack={handleBackToList} 
          />
        )}
        
        {view === 'random' && (
          <RandomMovie 
            onBack={handleBackToList}
            onSelectMovie={handleSelectMovie}
          />
        )}
      </Stack>
    </ThemeProvider>
  );
};

export default App; 