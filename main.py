
import logging
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
from SECRETS import API_KEY
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)

class NASA_API():
    def __init__(self):
        self.URL : str = "https://api.nasa.gov/planetary/apod" 
        self.date :str = self.get_date()

    def get_date(self) -> str:
        DATA_LIMITE_INFERIOR = datetime(1995, 6, 16)
        DATA_ATUAL = datetime.now()

        while True:
            entrada =  input("Digite a data da consulta (yyyy-mm-dd): ")
            try:
                data_entry = datetime.strptime(entrada, "%Y-%m-%d")
            except ValueError:
                print("Erro: Formato inválido ou data inexistente. Use yyyy-mm-dd.")
                continue

            if data_entry < DATA_LIMITE_INFERIOR or data_entry > DATA_ATUAL:
                print("Erro: A data deve estar entre 1995-06-16 e a data de hoje.")
                continue
        
            return data_entry.strftime("%Y-%m-%d")

    def consulta(self):
        target_date = self.date
        params = {
            "api_key" : API_KEY,
            "date" : target_date
        }

        try: 
            resposta = requests.get(self.URL, params = params)
            resposta.raise_for_status()

            return resposta.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar a API: {e}")
            return None

    def get_image_url(self, dados):
        if not dados:
            return
        image_link = dados.get('url', None)

        return image_link
        
    def show_image(self,dados):
        url = self.get_image_url(dados)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image.show()
            else: 
                logging.error(f'Erro ao buscar a imagem: {response.status_code}')    
        except Exception as e:
            logging.error(f'Erro ao abrir a imagem: {e}')     
        

    

def main():
    api = NASA_API()
    dados = api.consulta()
    if dados:
        api.show_image(dados)

if __name__ == "__main__":
    main()  
