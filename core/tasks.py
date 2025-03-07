from celery import shared_task
import requests

SMS_API_URL = "https://api.avlytext.com/v1/sms?api_key=H8krDAYH8deiNpKgSKqFlRjbY3Gx9N09ESfujWfcxrp0Sw6Msftk6XZ0OfSA0xQe67k5"
SMS_API_KEY = "your_api_key_here"

@shared_task
def send_sms_task(phone_number, message_content):
    """
    Sends an SMS asynchronously using an external API.
    """
    sms_payload =   {
    "sender": "AlphaMotors",
    "recipient": phone_number,
    "text": message_content
    }
    
    try:
        response = requests.post(SMS_API_URL, json=sms_payload)
        return response.json()  # Return API response (useful for logging)
    except Exception as e:
        return {"error": str(e)}
