import os
import logging
import requests
from flask import Flask, request, jsonify
from openai import OpenAI
import openai as openai_module  # Import the full openai module for fallback

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configuration from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ZAPI_INSTANCE_TOKEN = os.environ.get("ZAPI_INSTANCE_TOKEN")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")

# Initialize OpenAI client
openai_client = None
if OPENAI_API_KEY:
    try:
        # Initialize OpenAI client with only the supported arguments
        # This avoids the 'proxies' argument issue in Replit
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except TypeError as e:
        if "proxies" in str(e):
            # Handle Replit's automatic proxy injection
            logging.info("Retrying OpenAI client initialization without proxy settings")
            try:
                # Create a clean configuration dictionary with only the API key
                config = {"api_key": OPENAI_API_KEY}
                # Manually initialize the client with only the needed parameters
                openai_client = OpenAI(**config)
            except Exception as inner_e:
                logging.warning(
                    f"Failed to initialize OpenAI client on second attempt: {inner_e}"
                )
                openai_client = None
        else:
            logging.warning(f"Failed to initialize OpenAI client: {e}")
            openai_client = None
    except Exception as e:
        logging.warning(f"Failed to initialize OpenAI client: {e}")
        openai_client = None
else:
    logging.warning("OPENAI_API_KEY not set - GPT functionality will be disabled")


def ask_gpt(question):
    """
    Send a question to GPT-3.5-turbo and get a medical education focused response

    Args:
        question (str): The student's question or topic

    Returns:
        str: GPT's response or error message
    """
    if not openai_client:
        return "Desculpe, o serviço de IA não está disponível no momento. Verifique a configuração da API."

    try:
        # Medical education focused prompt in Portuguese
        prompt = f"Você é um professor de medicina que avalia alunos. Pergunta: {question}\nResponda com explicação detalhada e corrija gentilmente se necessário. Forneça informações educativas e precisas sobre o tópico médico."

        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um professor de medicina experiente e gentil. Sempre forneça explicações educativas, corrija erros com gentileza e incentive o aprendizado.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return (
            content.strip() if content else "Desculpe, não consegui gerar uma resposta."
        )

    except Exception as e:
        logging.error(f"Error calling OpenAI API: {str(e)}")
        return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"


def send_whatsapp_message(chat_id, message):
    """
    Send a message back to WhatsApp via Z-API

    Args:
        chat_id (str): The chat ID to send the message to
        message (str): The message content to send

    Returns:
        bool: True if successful, False otherwise
    """
    if not ZAPI_INSTANCE_TOKEN or not ZAPI_TOKEN:
        logging.error("Z-API credentials not configured")
        return False

    try:
        url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_TOKEN}/token/{ZAPI_TOKEN}/send-text"

        payload = {"phone": chat_id, "message": message}

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            logging.info(f"Message sent successfully to {chat_id}")
            return True
        else:
            logging.error(
                f"Failed to send message. Status: {response.status_code}, Response: {response.text}"
            )
            return False

    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {str(e)}")
        return False


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Webhook endpoint to receive messages from WhatsApp via Z-API

    Returns:
        tuple: Response message and status code
    """
    try:
        # Parse incoming JSON data
        data = request.get_json()

        if not data:
            logging.warning("No JSON data received")
            return "No data received", 400

        logging.debug(f"Received webhook data: {data}")

        # Extract message information
        # Z-API typically sends data in this format
        if "message" in data:
            message_data = data["message"]

            # Extract key fields
            text_message = message_data.get("text", {}).get("message", "")
            from_me = message_data.get("fromMe", False)
            chat_id = message_data.get("chatId", "")

            # Only process messages that are NOT from the bot itself
            if not from_me and text_message and chat_id:
                logging.info(f"Processing message from {chat_id}: {text_message}")

                # Get GPT response
                gpt_response = ask_gpt(text_message)

                # Send response back to WhatsApp
                if send_whatsapp_message(chat_id, gpt_response):
                    logging.info("Response sent successfully")
                else:
                    logging.error("Failed to send response")

            elif from_me:
                logging.debug("Ignoring message from bot itself")
            else:
                logging.debug("Message missing required fields or empty")

        return "ok", 200

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return f"Error: {str(e)}", 500


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify the service is running

    Returns:
        dict: Service status information
    """
    status = {
        "status": "healthy",
        "openai_configured": OPENAI_API_KEY is not None,
        "zapi_configured": bool(ZAPI_INSTANCE_TOKEN and ZAPI_TOKEN),
    }

    return jsonify(status), 200


@app.route("/", methods=["GET"])
def index():
    """
    Basic index page showing service status

    Returns:
        str: HTML page with service information
    """
    openai_status = "✅ Configurado" if OPENAI_API_KEY else "❌ Não configurado"
    zapi_status = (
        "✅ Configurado"
        if (ZAPI_INSTANCE_TOKEN and ZAPI_TOKEN)
        else "❌ Não configurado"
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Study Bot - Medical Education</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <h1 class="card-title text-center mb-4">
                                🤖 WhatsApp Study Bot
                            </h1>
                            <p class="text-center text-muted mb-4">
                                Bot de estudos médicos integrado com WhatsApp e GPT-3.5
                            </p>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <h5>Status dos Serviços:</h5>
                                    <ul class="list-group">
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            OpenAI API
                                            <span>{openai_status}</span>
                                        </li>
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            Z-API Integration
                                            <span>{zapi_status}</span>
                                        </li>
                                    </ul>
                                </div>
                                
                                <div class="col-md-6">
                                    <h5>Endpoints:</h5>
                                    <ul class="list-group">
                                        <li class="list-group-item">
                                            <code>POST /webhook</code><br>
                                            <small class="text-muted">Recebe mensagens do WhatsApp</small>
                                        </li>
                                        <li class="list-group-item">
                                            <code>GET /health</code><br>
                                            <small class="text-muted">Verificação de saúde da API</small>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            
                            <hr>
                            
                            <div class="alert alert-info">
                                <h6>Como usar:</h6>
                                <ol>
                                    <li>Configure as variáveis de ambiente necessárias</li>
                                    <li>Configure o webhook no Z-API apontando para <code>/webhook</code></li>
                                    <li>Envie mensagens relacionadas a medicina via WhatsApp</li>
                                    <li>Receba respostas educativas do GPT-3.5</li>
                                </ol>
                            </div>
                            
                            <div class="text-center">
                                <small class="text-muted">
                                    Desenvolvido para educação médica • Powered by OpenAI GPT-3.5
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    # Run the Flask application
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
