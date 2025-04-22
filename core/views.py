from rest_framework.decorators import api_view
from rest_framework.response import Response 
import requests
import logging
import re
from whatsapp_sms import settings

import locale
# locale.setlocale(locale.LC_ALL, 'fr_FR.utf8') 

    

# git add . & git commit -m "Debugging" & git push origin main


# Title Mapping
TITLE_MAPPING = {1: "Mr.", 2: "Mme.", 3: "Mr.",}

SMS_API_URL = settings.sms_api_url

WHATSAPP_API_URL = "https://app.techsoft-sms.com/api/v3/sms/send"


# # Car Model Mapping (update this based on your Odoo system)
# CAR_MODEL_MAPPING = {
#     1: "Toyota Corolla",
#     2: "Nissan Qashqai",
#     3: "Hyundai Tucson"
# }

# Dictionnaire des véhicules avec leurs index
CAR_MODEL_MAPPING = {
    19: "Berline MG7",
    27: "CHANGAN 4X4 UNI-K",
    26: "CHANGAN CS55 PLUS", 
    13: "Geely Cool",
    18: "Haval H5",
    52: "Haval H6",
    9: "Haval M6 Plus", 
    16: "Pick-Up Rich 6",
    21: "Tank 300",
}


@api_view(["POST"])
def receive_webhook_recall(request):
    # logging.error(f"Received Webhook Data: {request.data}")
    # logging.error(f"Received Webhook Header: {request.headers}")
    """
    Receives webhook data from Odoo and triggers an async SMS sending task.

    """ 

    french_days = {
        0: "lundi",
        1: "mardi",
        2: "mercredi",
        3: "jeudi",
        4: "vendredi",
        5: "samedi",
        6: "dimanche",
    }


    try:
        data = request.data  # Parse JSON payload from Odoo
        
        # Extract required fields with fallbacks
        title = TITLE_MAPPING.get(data.get("title"), "Cher")  # Default to "Cher Client"
        display_name = data.get("display_name", "Client")
        activity_date = data.get("x_date_rendez_vous", "") 
        if activity_date: 
            # formatted_date = activity_date.strftime('%A %d %B %Y') 
            # formatted_activity_date = f"{day_in_french} {formatted_date}"

            weekday = activity_date.weekday()  # Monday is 0 and Sunday is 6
            day_in_french = french_days.get(weekday, "")
            formatted_date = activity_date.strftime('%d-%m-%Y')
            formatted_activity_date = f"{day_in_french} {formatted_date}"


        else:
            formatted_date = ""
            formatted_activity_date = ""

        # Format the personalized message
        message_content = f"""Bonjour M./Mme. {display_name}, 

        C'est le service client de Alpha Motors. Nous avons noté votre absence à votre rendez-vous du {formatted_activity_date}.

        Nous comprenons que des imprévus peuvent survenir. Si vous souhaitez reprogrammer votre rendez-vous afin de discuter de votre projet automobile, n'hésitez pas à contacter notre service client au 692 091 685 / 650 654 797 pour que nous trouvions une nouvelle date qui vous convienne.

        Le service client de Alpha Motors Cameroun reste à votre disposition.

        Cordialement,
        Alpha Motors Cameroun.
        """
        
        # Assume phone number is retrieved elsewhere (e.g., another API call)
        phone_number = str(data.get("phone", 0)).replace(" ","")
        phone_number = format_cameroon_number(phone_number)

        whatsapp_number = str(data.get("mobile", 0)).replace(" ","")
        whatsapp_number = format_cameroon_number(whatsapp_number)

        # Headers
        headers = {
            "Authorization": f"Bearer {settings.techsoft}",
            "Content-Type": "application/json"
        }
 
        if whatsapp_number=="0":
            if phone_number=="0": 
                logging.error(f"{phone_number} whatsapp is {whatsapp_number}")
                return Response({"status": "failed", "message": "No Phone Number"}, status=200) 
            else :
                whatsapp_number = phone_number 

        whatsapp_payload =   {  
        "recipient": whatsapp_number,   
        "sender_id": "237692091685",
        "type": "whatsapp",
        "message": message_content,
        }

        whatsapp_payload_w_document =   {  
        "recipient": whatsapp_number,
        "sender_id": "237692091685",
        "type": "whatsapp",
        "message": "FICHE TECHNIQUE ALPHA MOTORS",
        "media_url":"https://meek-nasturtium-1b6cb0.netlify.app/fichetechnique.pdf"
        }
        # logging.error(f"Received Webhook Data: {sms_payload}")
        
        try:
            if whatsapp_number != "False":
                sent_whatsapp = send_Whatsapp(whatsapp_payload, headers)   
                if sent_whatsapp:
                    pass
                else:
                    send_SMS(sms_payload)
            else:
                # send_SMS(sms_payload)
                pass
                # send_Whatsapp(whatsapp_payload, headers)
            # send_Whatsapp(whatsapp_payload, headers)
        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=500)
        
        return Response({"status": "success", "message": "SMS Sent"}, status=200) 

    except Exception as e:
        print(e)
        logging.error(e)
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def receive_webhook(request):
    # logging.error(f"Received Webhook Data: {request.data}")
    # logging.error(f"Received Webhook Header: {request.headers}")
    """
    Receives webhook data from Odoo and triggers an async SMS sending task.
    """
    

    try:
        data = request.data  # Parse JSON payload from Odoo
        
        # Extract required fields with fallbacks
        title = TITLE_MAPPING.get(data.get("title"), "Cher")  # Default to "Cher Client"
        display_name = data.get("display_name", "Client")
        car_model = CAR_MODEL_MAPPING.get(data.get("x_studio_many2one_field_44a_1iffl5utu"), "un de nos véhicules")

        # Format the personalized message
        message_content = f"""Bonjour M./Mme. {display_name},

        C’est le service client d'Alpha Motors.

        Merci encore d’avoir visité notre stand et pour l’intérêt que vous portez au véhicule {car_model}. Comme convenu, vous pouvez consulter notre catalogue complet.

        Si vous avez des questions ou si vous souhaitez plus de détails, n’hésitez surtout pas à nous écrire par WhatsApp ou à nous appeler au 692 091 685 / 650 654 797. Nous serons ravis de vous assister.

        Excellente journée à vous, et à bientôt chez Alpha Motors !
        """

        SMS_message_content = f"""Bonjour {title} {display_name},
        Merci d’avoir visité notre stand et pour l’intérêt porté au {car_model}. Retrouvez notre catalogue en ligne ici : https://shr.pn/alpha-motors. 
        Pour toute question, contactez-nous au 692 091 685 ou via WhatsApp. À bientôt chez Alpha Motors !
        """ 
        
        # Assume phone number is retrieved elsewhere (e.g., another API call)
        phone_number = str(data.get("phone", 0)).replace(" ","")
        phone_number = format_cameroon_number(phone_number)

        whatsapp_number = str(data.get("mobile", 0)).replace(" ","")
        whatsapp_number = format_cameroon_number(whatsapp_number)
        if "dm" in whatsapp_number:
            whatsapp_number=phone_number

        # Headers
        headers = {
            "Authorization": f"Bearer {settings.techsoft}",
            "Content-Type": "application/json"
        }

        # Data payload
        data = {
            "recipient": "237655272036",
            "sender_id": "237657467945",
            "type": "whatsapp",
            "message": "This is a test message"
        }

        if phone_number=="0" and whatsapp_number=="0" :
            logging.error(f"{phone_number} whatsapp is {whatsapp_number}")
            return Response({"status": "failed", "message": "No Phone Number"}, status=200)
        # Send SMS asynchronously
        # send_sms_task.delay(phone_number, message_content)
        
        """
        Sends an SMS asynchronously using an external API.
        """
        sms_payload =   {
        "sender": "AlphaMotors",
        "recipient": phone_number,
        "text": SMS_message_content
        }

        whatsapp_payload =   {  
        "recipient": whatsapp_number,
        "sender_id": "237692091685",
        "type": "whatsapp",
        "message": message_content
        }
        # logging.error(f"Received Webhook Data: {sms_payload}")

        whatsapp_payload_w_document =   {  
        "recipient": whatsapp_number,
        "sender_id": "237692091685",
        "type": "whatsapp",
        "message": "FICHE TECHNIQUE ALPHA MOTORS",
        "media_url":"https://meek-nasturtium-1b6cb0.netlify.app/fichetechnique.pdf"
        }
        
        try:
            if whatsapp_number != "False":
                sent_whatsapp = send_Whatsapp(whatsapp_payload, headers, whatsapp_payload_w_document)   
                if sent_whatsapp :
                    pass
                else:
                    send_SMS(sms_payload)
            else:
                send_SMS(sms_payload)
                # send_Whatsapp(whatsapp_payload, headers)
            # send_Whatsapp(whatsapp_payload, headers)
        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=500)
        
        return Response({"status": "success", "message": "SMS Sent"}, status=200)


        # return Response({"status": "success", "message": "SMS task queued"})

    except Exception as e:
        print(e)
        logging.error(e)
        return Response({"error": str(e)}, status=500)



@api_view(["POST", "GET"])
def index(request):
    # logging.error(f"Received Webhook Data: {request.data}")
    # logging.error(f"Received Webhook Header: {request.headers}")
    """
    Receives webhook data from Odoo and triggers an async SMS sending task.

    """ 

    try: 
        
        return Response({"status": "success", "message": "SMS Sent"}, status=200) 

    except Exception as e:
        print(e)
        logging.error(e)
        return Response({"error": str(e)}, status=500)




def format_cameroon_number(phone):
    """
    Converts a 9-digit phone number starting with '6' into the international format (+237).
    """
    # Check if the phone number is exactly 9 digits and starts with 6
    if re.fullmatch(r"6\d{8}", phone):
        return "+237" + phone
    return phone  # Return as is if it doesn't match


def send_SMS(payload):
    """
    Converts a 9-digit phone number starting with '6' into the international format (+237).
    """
    response = requests.post(SMS_API_URL, json=payload)
    # return response.json()  # Return API response (useful for logging) 
    # Check if the SMS was sent successfully
    if response.status_code == 200: 
        logging.info("SENT SMS")
        return True 
    else: 
        logging.error(f"SMS FAILED: PAYLOAD = {payload}")
        return False
    
def send_Whatsapp( payload, headers, whatsapp_payload_w_document={}):
    """
    Converts a 9-digit phone number starting with '6' into the international format (+237).
    """

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload) 

    if response.status_code == 200: 
        next_response = requests.post(WHATSAPP_API_URL, headers=headers, json=whatsapp_payload_w_document) 
        if next_response.status_code == 200:  
            return True
        else:
            logging.error(f"NEXT WHATSAPP FAILED: PAYLOAD = {whatsapp_payload_w_document}")
        return True
    else: 
        logging.error(f"WHATSAPP FAILED: PAYLOAD = {payload}")
        return False