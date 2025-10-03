const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const OpenAI = require('openai');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// Serve static files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// OpenAI API endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { prompt, conversationHistory = [] } = req.body;
    
    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    // Prepare messages for OpenAI
    const messages = [
      {
        role: 'system',
        content: 'You are a helpful assistant. Respond naturally to user questions. Keep your responses concise and helpful.'
      },
      ...conversationHistory,
      {
        role: 'user',
        content: prompt
      }
    ];

    // Call OpenAI API
    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: messages,
      max_tokens: 150,
      temperature: 0.7,
    });

    const response = completion.choices[0].message.content;
    
    res.json({ 
      response: response,
      usage: completion.usage 
    });

  } catch (error) {
    console.error('OpenAI API Error:', error);
    
    // Handle different types of errors
    if (error.code === 'insufficient_quota') {
      return res.status(402).json({ 
        error: 'API quota exceeded. Please check your OpenAI account.' 
      });
    }
    
    if (error.code === 'invalid_api_key') {
      return res.status(401).json({ 
        error: 'Invalid API key. Please check your OpenAI configuration.' 
      });
    }
    
    res.status(500).json({ 
      error: 'Failed to get response from AI. Please try again.' 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    hasOpenAIKey: !!process.env.OPENAI_API_KEY
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 GOLLMF server running on port ${PORT}`);
  console.log(`📝 OpenAI API Key configured: ${!!process.env.OPENAI_API_KEY}`);
  console.log(`🌐 Open http://localhost:${PORT} to play!`);
});

module.exports = app;
