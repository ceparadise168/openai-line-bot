import os
import openai
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

# Initialize the LINE bot SDK
line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

# Initialize the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define a function to generate a response using the ChatGPT API
def generate_response(text):
    prompt = f"User: {text}\nChatbot:"
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = prompt,
        temperature = 0.9,
        max_tokens = 256,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0.6
    )
    return response.choices[0].text.strip()

# Define the function that handles incoming messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    response = generate_response(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

# Define the Lambda function handler
def lambda_handler(event, context):
    signature = event["headers"]["x-line-signature"]
    body = event["body"]
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token and secret.")
        return {"statusCode": 400, "body": "Invalid signature"}
    return {"statusCode": 200, "body": "OK"}
