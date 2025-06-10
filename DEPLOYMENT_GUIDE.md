# WhatsApp Study Bot - Deployment Guide

## Option 1: Deploy to Render.com (Recommended - Free)

### Step 1: Prepare Your Code for Deployment

1. **Create a GitHub Repository**
   - Go to https://github.com and create a new repository
   - Upload all your project files: `app.py`, `main.py`, `pyproject.toml`, `uv.lock`

### Step 2: Deploy to Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose the repository with your bot code

3. **Configure Build Settings**
   - **Name**: `whatsapp-study-bot` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt` or leave empty (Render auto-detects)
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`

4. **Set Environment Variables**
   In the "Environment" section, add:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ZAPI_INSTANCE_TOKEN=your_instance_token_here
   ZAPI_TOKEN=your_api_token_here
   SESSION_SECRET=any_random_string_here
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete (5-10 minutes)
   - You'll get a URL like: `https://whatsapp-study-bot.onrender.com`

### Step 3: Configure Z-API Webhook

1. **Get Your Render URL**
   - Your webhook URL will be: `https://your-app-name.onrender.com/webhook`
   - Example: `https://whatsapp-study-bot.onrender.com/webhook`

2. **Set Webhook in Z-API Dashboard**
   - Go to your Z-API dashboard
   - Find "Webhook" settings
   - Enter: `https://your-app-name.onrender.com/webhook`
   - Enable the webhook

## Option 2: Use Replit's Public URL (For Testing)

If you want to test with your current Replit setup:

1. **Make Your Repl Public**
   - In Replit, go to your project settings
   - Enable "Always On" (may require paid plan)
   - Get your public URL from the webview

2. **Use the Replit URL**
   - Your webhook URL would be: `https://your-repl-name.your-username.repl.co/webhook`
   - Configure this in your Z-API dashboard

## Option 3: Deploy to Railway (Alternative)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Connect your repository
   - Railway will auto-detect it's a Python app
   - Set the same environment variables as above

3. **Get Your Railway URL**
   - Use the provided URL + `/webhook` for your Z-API webhook

## Requirements.txt File

Create this file if it doesn't exist:

```
flask==3.0.0
gunicorn==21.2.0
openai==1.3.8
requests==2.31.0
```

## Testing Your Deployment

1. **Check Status Page**
   - Visit your deployed URL (without /webhook)
   - Verify both OpenAI and Z-API show as "Configurado"

2. **Test Health Endpoint**
   - Visit: `https://your-url.com/health`
   - Should return JSON with status information

3. **Test WhatsApp Integration**
   - Send a message to your connected WhatsApp number
   - Example: "Explique sobre infarto agudo do miocárdio"
   - Bot should respond with educational content

## Troubleshooting

### Common Issues:

1. **Deployment Fails**
   - Check that all files are in your repository
   - Verify requirements.txt has correct package versions
   - Check build logs for specific errors

2. **Environment Variables Not Working**
   - Double-check all variable names are exact
   - Ensure no extra spaces in values
   - Restart the service after adding variables

3. **Webhook Not Receiving Messages**
   - Verify webhook URL is publicly accessible
   - Check that URL ends with `/webhook`
   - Test URL in browser - should return "Method Not Allowed" for GET requests

4. **Bot Not Responding**
   - Check application logs for errors
   - Verify OpenAI API key is valid and has credits
   - Ensure Z-API instance is still connected to WhatsApp

## Production Considerations

1. **Monitoring**
   - Set up error logging and monitoring
   - Monitor API usage and costs
   - Set up health check alerts

2. **Security**
   - Never commit API keys to repository
   - Use environment variables for all secrets
   - Consider implementing rate limiting

3. **Scaling**
   - Most platforms auto-scale based on traffic
   - Monitor response times and add resources if needed
   - Consider implementing message queuing for high volume

## Support

- Render.com: Has extensive documentation and free tier
- Railway: Good alternative with simple deployment
- Always test in a staging environment before production