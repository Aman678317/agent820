import React, { useState } from 'react';
import { routePost } from '../api';

const PersonaRouter = () => {
    const [post, setPost] = useState('OpenAI just released a new model that might replace junior developers.');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleRoute = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await routePost(post);
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card">
            <h2 className="title-gradient">Phase 1: Persona Router</h2>
            <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
                Test the FAISS vector similarity routing. Paste a post and see which persona bots engage.
            </p>
            <textarea 
                value={post} 
                onChange={(e) => setPost(e.target.value)}
                rows={3}
            />
            <button onClick={handleRoute} disabled={loading}>
                {loading ? <span className="loader"></span> : 'Route Post'}
            </button>
            {error && <div className="error">{error}</div>}
            {result && (
                <div className="result-box">
                    <h4>Matched Bots:</h4>
                    {result.matched_bots && result.matched_bots.length > 0 ? result.matched_bots.map((b, i) => (
                        <div key={i} style={{ marginBottom: '0.5rem', marginTop: '0.5rem' }}>
                            <span className="badge">{b.bot_name} ({b.bot_id})</span>
                            <div>Score: {b.similarity_score}</div>
                            <div style={{color: 'var(--text-muted)'}}>{b.reason}</div>
                        </div>
                    )) : <div>No bots matched the threshold.</div>}
                </div>
            )}
        </div>
    );
};

export default PersonaRouter;
