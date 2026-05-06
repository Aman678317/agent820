import React, { useState } from 'react';
import { askChat } from '../api';

const ChatAssistant = () => {
    const [message, setMessage] = useState('Explain this project in simple words.');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleAsk = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await askChat(message);
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card" style={{ background: 'rgba(59, 130, 246, 0.05)' }}>
            <h2 className="title-gradient">AI Chat Assistant</h2>
            <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
                Ask anything about the project architecture, features, or deployment.
            </p>
            <textarea 
                value={message} 
                onChange={(e) => setMessage(e.target.value)}
                rows={2}
                placeholder="Ask anything about this project..."
            />
            <button onClick={handleAsk} disabled={loading}>
                {loading ? <span className="loader"></span> : 'Ask AI'}
            </button>
            {error && <div className="error">{error}</div>}
            {result && (
                <div className="result-box" style={{ background: 'rgba(0,0,0,0.4)', border: '1px solid rgba(59, 130, 246, 0.2)' }}>
                    <span className="badge">Provider: {result.provider}</span>
                    <p style={{ color: 'white', marginTop: '0.5rem', whiteSpace: 'pre-wrap' }}>{result.answer}</p>
                </div>
            )}
        </div>
    );
};

export default ChatAssistant;
