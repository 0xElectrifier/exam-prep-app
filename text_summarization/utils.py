from django.conf import settings
from google.oauth2 import service_account
from vertexai.language_models import TextGenerationModel
import json
import vertexai


google_cred = settings.ENV.str("GOOGLE_VISION_SERVICE_ACCOUNT")
json_account_info = json.loads(google_cred)


def summarize_content(text):
    credentials = service_account.Credentials.from_service_account_info(json_account_info)
    vertexai.init(project="eduhack-420512",credentials=credentials)
    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": 0.5,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(text, **parameters)

    return response
