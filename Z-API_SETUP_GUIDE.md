# Z-API Integration Setup Guide

## Step 1: Create Z-API Account and Get WhatsApp Instance

1. **Go to Z-API Website**
   - Visit: https://z-api.io/
   - Click "Sign Up" or "Register"

2. **Create Your Account**
   - Fill in your email and create a password
   - Verify your email address

3. **Create a WhatsApp Instance**
   - After logging in, click "Create Instance" or "New Instance"
   - Choose a name for your instance (e.g., "StudyBot")
   - Select a plan (they usually have a free tier for testing)

4. **Connect Your WhatsApp**
   - You'll get a QR code to scan
   - Open WhatsApp on your phone
   - Go to WhatsApp Web (three dots menu → WhatsApp Web)
   - Scan the QR code displayed on Z-API dashboard
   - Your WhatsApp will now be connected to Z-API

## Step 2: Get Your API Credentials

After connecting WhatsApp, you'll see your dashboard with:

1. **Instance Token** - This looks like: `3C4B2A1D0E`
2. **API Token** - This looks like: `F9E8D7C6B5A4`

You need both of these values.

## Step 3: Configure Environment Variables

You need to set these environment variables in your deployment:

```
ZAPI_INSTANCE_TOKEN=your_instance_token_here
ZAPI_TOKEN=your_api_token_here
```

For example:
```
ZAPI_INSTANCE_TOKEN=3C4B2A1D0E
ZAPI_TOKEN=F9E8D7C6B5A4
```

## Step 4: Set Up Webhook in Z-API Dashboard

1. **Find Webhook Settings**
   - In your Z-API dashboard, look for "Webhook" or "Webhook URL" settings
   - This might be under "Settings" or "Configuration"

2. **Enter Your Bot's Webhook URL**
   - If testing locally: `https://your-replit-url.replit.app/webhook`
   - If deployed on Render: `https://your-app-name.onrender.com/webhook`
   - Make sure to include `/webhook` at the end

3. **Enable the Webhook**
   - Make sure the webhook is enabled/active
   - Some Z-API services have a toggle to turn webhooks on/off

## Step 5: Test Your Integration

1. **Send a test message** to your connected WhatsApp number
2. **Check your application logs** to see if the webhook is receiving messages
3. **Verify the bot responds** with a GPT-generated medical education response

## Troubleshooting

### Common Issues:

1. **Webhook not receiving messages:**
   - Check if your webhook URL is publicly accessible
   - Verify the webhook URL is correct in Z-API dashboard
   - Make sure your application is running

2. **Messages not being sent:**
   - Verify your ZAPI_INSTANCE_TOKEN and ZAPI_TOKEN are correct
   - Check if your Z-API instance is still connected to WhatsApp
   - Look at application logs for error messages

3. **Bot responding to its own messages:**
   - The code already handles this by checking `fromMe` field
   - If issues persist, check Z-API webhook payload format

### Checking Your Setup:

Visit your application's homepage to see the status:
- ✅ OpenAI API: Should show "Configurado" 
- ✅ Z-API Integration: Should show "Configurado" when both tokens are set

## Security Notes

- Keep your API tokens private and secure
- Don't share them in public repositories or chat
- Use environment variables, never hardcode them in your code
- Regularly monitor your Z-API usage to avoid unexpected charges

## Next Steps After Setup

Once everything is working:
1. Test with medical education questions in Portuguese
2. Monitor the logs for any issues
3. Consider upgrading your Z-API plan for production use
4. Deploy to a production hosting service like Render.com