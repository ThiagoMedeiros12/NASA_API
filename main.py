import logging
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
from SECRETS import API_KEY

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)

class NASA_API:
    def __init__(self):
        self.URL = "https://api.nasa.gov/planetary/apod" 

    def consulta(self, target_date):
        params = {
            "api_key": API_KEY,
            "date": target_date
        }

        try: 
            resposta = requests.get(self.URL, params=params)
            resposta.raise_for_status()
            return resposta.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao consultar a API: {e}")
            return None

    def get_image_url(self, dados):
        if not dados:
            return None
        return dados.get('url', None)

    def get_media_type(self, dados):
        if not dados:
            return None
        return dados.get('media_type', None)

    def fetch_image(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                return image
            else: 
                logging.error(f'Erro ao buscar a imagem: {response.status_code}')
                return None
        except Exception as e:
            logging.error(f'Erro ao abrir a imagem: {e}')     
            return None
