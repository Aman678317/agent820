const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const routePost = async (postContent, threshold = 0.85) => {
    const res = await fetch(`${API_BASE_URL}/api/route`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ post_content: postContent, threshold })
    });
    if (!res.ok) {
        const errText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errText}`);
    }
    return res.json();
};

export const generatePost = async (botId) => {
    const res = await fetch(`${API_BASE_URL}/api/generate-post`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bot_id: botId })
    });
    if (!res.ok) {
        const errText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errText}`);
    }
    return res.json();
};

export const generateDefenseReply = async (humanReply) => {
    const res = await fetch(`${API_BASE_URL}/api/defense-reply`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ human_reply: humanReply })
    });
    if (!res.ok) {
        const errText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errText}`);
    }
    return res.json();
};

export const askChat = async (message) => {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    if (!res.ok) {
        const errText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errText}`);
    }
    return res.json();
};
