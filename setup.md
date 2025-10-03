# GOLLMF Setup Guide

## Prerequisites
- Node.js (version 14 or higher)
- OpenAI API key

## Installation

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Set up Environment Variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

3. **Get OpenAI API Key**
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Go to API Keys section
   - Create a new API key
   - Copy the key to your `.env` file

## Running the Application

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

The server will start on port 3000. Open http://localhost:3000 to play!

## API Endpoints

- `GET /` - Serves the game interface
- `POST /api/chat` - OpenAI chat endpoint
- `GET /api/health` - Health check

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `PORT` - Server port (default: 3000)

## Troubleshooting

### Common Issues

1. **"Invalid API key" error**
   - Check your OpenAI API key in `.env`
   - Make sure the key is valid and has credits

2. **"API quota exceeded" error**
   - Check your OpenAI account billing
   - Add credits to your account

3. **Server won't start**
   - Make sure Node.js is installed
   - Run `npm install` to install dependencies
   - Check that port 3000 is available

### Cost Management

- Each API call costs approximately $0.001-0.002
- Monitor your usage in the OpenAI dashboard
- Set usage limits in your OpenAI account

## Security Notes

- Never commit your `.env` file to version control
- The API key is kept secure on the server side
- Client-side code never sees the API key directly
