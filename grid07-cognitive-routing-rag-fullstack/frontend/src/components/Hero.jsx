import React from 'react';

const Hero = () => {
    return (
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
            <h1 className="title-gradient" style={{ fontSize: '3rem', marginBottom: '1rem' }}>
                Cognitive Routing & RAG Platform
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto' }}>
                Vector-based persona routing, LangGraph autonomous content engine, and combat-ready RAG modules.
            </p>
        </div>
    );
};

export default Hero;
