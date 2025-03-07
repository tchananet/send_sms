from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import send_sms_task

# Title Mapping
TITLE_MAPPING = {1: "Monsieur", 2: "Madame"}

# Car Model Mapping (update this based on your Odoo system)
CAR_MODEL_MAPPING = {
    1: "Toyota Corolla",
    2: "Nissan Qashqai",
    3: "Hyundai Tucson"
}

@api_view(["POST"])
def receive_webhook(request):
    """
    Receives webhook data from Odoo and triggers an async SMS sending task.
    """
    try:
        data = request.data  # Parse JSON payload from Odoo
        
        # Extract required fields with fallbacks
        title = TITLE_MAPPING.get(data.get("title"), "Cher")  # Default to "Cher Client"
        display_name = data.get("display_name", "Client")
        car_model = CAR_MODEL_MAPPING.get(data.get("x_studio_modele_voiture"), "un de nos véhicules")

        # Format the personalized message
        message_content = f"""Bonjour {title} {display_name},

        C’est le service client d'Alpha Motors.

        Merci encore d’avoir visité notre stand et pour l’intérêt que vous portez au véhicule {car_model}. Comme convenu, vous pouvez consulter notre catalogue complet en ligne via ce lien : https://www.alphamotors-cameroun.com/catalogue.

        Si vous avez des questions ou si vous souhaitez plus de détails, n’hésitez surtout pas à nous écrire par WhatsApp ou à nous appeler au 650 654 797. Nous serons ravis de vous assister.

        Excellente journée à vous, et à bientôt chez Alpha Motors !
        """

        # Assume phone number is retrieved elsewhere (e.g., another API call)
        phone_number = data.get("phone", 0)
        if phone_number==0:
            return Response({"status": "failed", "message": "No Phone Number"})
        #g Send SMS asynchronously
        send_sms_task.delay(phone_number, message_content)

        return Response({"status": "success", "message": "SMS task queued"})

    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)
