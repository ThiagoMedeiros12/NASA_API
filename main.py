
from datetime import datetime
import requests
from SECRETS import API_KEY



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

    def print_data(self, dados):
        if not dados:
            return

        print("-" * 40)
        print(f"Data: {dados['date']}")
        print(f"Título: {dados['title']}")
        print(f"Tipo de Mídia: {dados['media_type']}")
        
        if dados['media_type'] == 'image':
            print(f"URL da Imagem: {dados['url']}")
        else:
            print(f"URL do Vídeo: {dados['url']}")
        
        print(f"Explicação: {dados['explanation']}")
        print("-" * 40)

        
    

def main():
    api = NASA_API()
    dados = api.consulta()
    if dados:
        print(f"\nSucesso! Imagem encontrada: {dados.get('title')}")
        print(f"URL: {dados.get('url')}")

if __name__ == "__main__":
    main()  
