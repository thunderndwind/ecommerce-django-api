import requests
from django.conf import settings

class AzureFaceIDAuth:
    def __init__(self):
        self.face_api_url = settings.AZURE_FACE_API_URL
        self.face_api_key = settings.AZURE_FACE_API_KEY

    def register_face(self, face_image):
        # Convert the image to binary and send it to Azure API for face detection
        headers = {
            'Ocp-Apim-Subscription-Key': self.face_api_key,
            'Content-Type': 'application/octet-stream'
        }
        response = requests.post(f'{self.face_api_url}/detect', headers=headers, data=face_image.read())

        if response.status_code == 200:
            face_data = response.json()
            return face_data[0]['faceId'] if face_data else None
        else:
            raise Exception(f"Azure Face API Error: {response.content}")

    def verify_face(self, face_image, face_id):
        # Use Azure API to verify the face with the stored face_id
        headers = {
            'Ocp-Apim-Subscription-Key': self.face_api_key,
            'Content-Type': 'application/octet-stream'
        }
        data = {'faceId': face_id, 'faceImage': face_image}
        response = requests.post(f'{self.face_api_url}/verify', headers=headers, json=data)
        return response.status_code == 200
