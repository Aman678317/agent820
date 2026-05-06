import React from 'react';
import Hero from './components/Hero.jsx';
import PersonaRouter from './components/PersonaRouter.jsx';
import ContentEngine from './components/ContentEngine.jsx';
import CombatEngine from './components/CombatEngine.jsx';
import ChatAssistant from './components/ChatAssistant.jsx';

function App() {
  return (
    <div className="container">
      <Hero />
      <div className="section">
        <PersonaRouter />
      </div>
      <div className="grid section">
        <ContentEngine />
        <CombatEngine />
      </div>
      <div className="section">
        <ChatAssistant />
      </div>
    </div>
  );
}

export default App;
