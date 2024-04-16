from rest_framework.exceptions import APIException

class GoogleVisionAPIException(APIException):
    status_code = 400
    default_detail = 'Google Vision API error'
    default_code = 'google_vision_api_error'

class GoogleCloudServiceAccountCredentialsException(APIException):
    status_code = 400
    default_detail = 'Google Cloud Service Account credentials error'
    default_code = 'google_cloud_service_account_credentials_error'

class UnexpectedException(APIException):
    status_code = 500
    default_detail = 'Unexpected error'
    default_code = 'unexpected_error'