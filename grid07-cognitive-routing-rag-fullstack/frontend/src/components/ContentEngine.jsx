import React, { useState } from 'react';
import { generatePost } from '../api';

const ContentEngine = () => {
    const [botId, setBotId] = useState('bot_a');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await generatePost(botId);
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card">
            <h2 className="title-gradient">Phase 2: Content Engine</h2>
            <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
                LangGraph state machine generates autonomous opinionated content.
            </p>
            <select 
                value={botId} 
                onChange={(e) => setBotId(e.target.value)}
                style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', background: 'rgba(15,23,42,0.6)', color: 'white', border: '1px solid var(--card-border)', borderRadius: '8px' }}
            >
                <option value="bot_a">Tech Maximalist (bot_a)</option>
                <option value="bot_b">Doomer / Skeptic (bot_b)</option>
                <option value="bot_c">Finance Bro (bot_c)</option>
            </select>
            <button onClick={handleGenerate} disabled={loading} style={{ width: '100%' }}>
                {loading ? <span className="loader"></span> : 'Generate Post'}
            </button>
            {error && <div className="error">{error}</div>}
            {result && (
                <div className="result-box">
                    <span className="badge">Topic: {result.topic}</span>
                    <p style={{ color: 'white', marginTop: '0.5rem' }}>{result.post_content}</p>
                    <div style={{ fontSize: '0.75rem', marginTop: '1rem', opacity: 0.5 }}>
                        Raw JSON: {JSON.stringify(result)}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ContentEngine;
