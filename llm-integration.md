# LLM Integration Guide

To connect GOLLMF to a real LLM API, you'll need to replace the `simulateGPTResponse()` function with actual API calls.

## OpenAI Integration

### 1. Get API Key
- Sign up at [OpenAI](https://platform.openai.com/)
- Create an API key in your dashboard
- Add it to your environment variables

### 2. Update the JavaScript

Replace the `simulateGPTResponse()` function in `index.html`:

```javascript
async function callOpenAI(prompt) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${YOUR_API_KEY}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: 'gpt-3.5-turbo',
            messages: [
                {
                    role: 'system',
                    content: 'You are a helpful assistant. Respond naturally to user questions.'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            max_tokens: 150,
            temperature: 0.7
        })
    });
    
    const data = await response.json();
    return data.choices[0].message.content;
}
```

### 3. Update submitPrompt function

```javascript
async function submitPrompt() {
    const input = document.getElementById('promptInput');
    const prompt = input.value.trim();
    
    if (!prompt || gameCompleted) return;
    
    // Add user message to conversation
    addMessage('You', prompt, 'user-message');
    
    // Check for traps
    const trapPenalty = checkTraps(prompt);
    const promptWords = prompt.split(' ').length;
    const totalWords = promptWords + trapPenalty;
    
    wordCount += totalWords;
    
    if (trapPenalty > 0) {
        addTrapWarning(trapPenalty);
    }
    
    // Show loading state
    addMessage('GPT', 'Thinking...', 'gpt-message');
    
    try {
        // Call real OpenAI API
        const gptResponse = await callOpenAI(prompt);
        
        // Remove loading message and add real response
        const conversation = document.getElementById('conversation');
        conversation.removeChild(conversation.lastChild);
        addMessage('GPT', gptResponse, 'gpt-message');
        
        // Check for win
        if (checkWin(gptResponse)) {
            showWinMessage();
            gameCompleted = true;
            document.getElementById('nextHoleBtn').style.display = 'block';
        }
    } catch (error) {
        console.error('API Error:', error);
        addMessage('GPT', 'Sorry, I encountered an error. Please try again.', 'gpt-message');
    }
    
    // Update score and progress
    updateScore();
    updateProgress();
    
    // Clear input
    input.value = '';
}
```

## Alternative LLM APIs

### Anthropic Claude
```javascript
async function callClaude(prompt) {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'x-api-key': YOUR_API_KEY,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
            model: 'claude-3-sonnet-20240229',
            max_tokens: 150,
            messages: [{
                role: 'user',
                content: prompt
            }]
        })
    });
    
    const data = await response.json();
    return data.content[0].text;
}
```

### Google Gemini
```javascript
async function callGemini(prompt) {
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${YOUR_API_KEY}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contents: [{
                parts: [{
                    text: prompt
                }]
            }]
        })
    });
    
    const data = await response.json();
    return data.candidates[0].content.parts[0].text;
}
```

## Security Considerations

### 1. API Key Protection
- **Never expose API keys in client-side code**
- Use a backend proxy server
- Implement rate limiting
- Add user authentication

### 2. Backend Proxy Example (Node.js/Express)

```javascript
// server.js
const express = require('express');
const cors = require('cors');
const { OpenAI } = require('openai');

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

app.post('/api/chat', async (req, res) => {
    try {
        const { prompt } = req.body;
        
        const completion = await openai.chat.completions.create({
            model: 'gpt-3.5-turbo',
            messages: [
                { role: 'user', content: prompt }
            ],
            max_tokens: 150
        });
        
        res.json({ response: completion.choices[0].message.content });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Proxy server running on port 3000');
});
```

### 3. Frontend Update
```javascript
async function callOpenAI(prompt) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });
    
    const data = await response.json();
    return data.response;
}
```

## Cost Optimization

### 1. Token Limits
- Set `max_tokens` to limit response length
- Use shorter system prompts
- Implement conversation history limits

### 2. Caching
- Cache common responses
- Use localStorage for conversation history
- Implement smart caching strategies

### 3. Rate Limiting
- Limit requests per user
- Implement cooldown periods
- Add usage tracking

## Deployment Options

### 1. Vercel (Recommended)
- Easy deployment with environment variables
- Built-in serverless functions
- Automatic HTTPS

### 2. Netlify
- Serverless functions support
- Easy environment variable management
- Good for static sites

### 3. Railway/Render
- Full backend deployment
- Database integration
- More control over server configuration

## Example Environment Variables

```bash
# .env.local
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
```

Remember to add `.env.local` to your `.gitignore` file!
