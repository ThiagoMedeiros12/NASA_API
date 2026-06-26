import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk

class ApplicationWindow:
    def __init__(self, root_window, api_client):
        self.root_window = root_window
        self.api = api_client
        
        self.root_window.title("NASA API - Imagem do Dia")
        self.root_window.geometry("900x700")
        self.root_window.minsize(500, 400)
        
        self.setup_user_interface()

    def setup_user_interface(self):
        # Frame de controles no topo
        self.control_frame = ttk.Frame(self.root_window)
        self.control_frame.pack(pady=20, fill='x')

        self.welcome_label = ttk.Label(
            self.control_frame, 
            text="NASA API", 
            font=("Papyrus", 16)
        )
        self.welcome_label.pack(pady=(0, 10))

        self.date_label = ttk.Label(self.control_frame, text="Digite a data da consulta (yyyy-mm-dd):")
        self.date_label.pack(pady=(5, 5))

        self.date_entry = ttk.Entry(self.control_frame, width=30)
        self.date_entry.pack(pady=(0, 10))

        self.submit_action_button = ttk.Button(
            self.control_frame, 
            text="Buscar", 
            command=self.handle_button_click
        )
        self.submit_action_button.pack(pady=5)

        # Label para exibir o título da imagem
        self.title_label = ttk.Label(self.root_window, text="", font=("Helvetica", 14, "bold"))
        self.title_label.pack(pady=5)

        # Label para exibir a imagem na interface
        self.image_label = ttk.Label(self.root_window)
        self.image_label.pack(pady=10, expand=True)

    def validate_date(self, date_str):
        DATA_LIMITE_INFERIOR = datetime(1995, 6, 16)
        DATA_ATUAL = datetime.now()
        
        try:
            data_entry = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Formato Inválido", "Erro: Formato inválido. Use yyyy-mm-dd.")
            return False
            
        if data_entry < DATA_LIMITE_INFERIOR or data_entry > DATA_ATUAL:
            messagebox.showwarning("Data Inválida", "Erro: A data deve estar entre 1995-06-16 e a data de hoje.")
            return False
            
        return True

    def handle_button_click(self):
        entered_date = self.date_entry.get().strip()
        
        if not entered_date:
            messagebox.showwarning("Input Required", "Por favor, insira uma data.")
            return
            
        if self.validate_date(entered_date):
            # Limpa imagem e título anterior
            self.title_label.configure(text="Buscando...")
            self.image_label.configure(image='')
            self.image_label.image = None
            self.root_window.update()

            dados = self.api.consulta(entered_date)
            
            if dados:
                media_type = self.api.get_media_type(dados)
                url = self.api.get_image_url(dados)
                titulo = dados.get("title", "")
                
                self.title_label.configure(text=titulo)
                
                if media_type == "video":
                    messagebox.showinfo("Vídeo", f"O APOD desta data é um vídeo.\nAcesse o link: {url}")
                elif url:
                    image = self.api.fetch_image(url)
                    if image:
                        self.display_image(image)
                    else:
                        messagebox.showerror("Erro", "Não foi possível processar a imagem.")
                else:
                    messagebox.showerror("Erro", "Nenhuma URL de mídia encontrada para esta data.")
            else:
                self.title_label.configure(text="Erro ao buscar dados.")
                messagebox.showerror("Erro", "Não foi possível buscar dados da API. Verifique sua chave.")

    def display_image(self, image):
        # Tamanho máximo que a imagem ocupará na janela
        max_width = 800
        max_height = 450
        
        width, height = image.size
        aspect_ratio = width / height
        
        # Redimensionar mantendo proporção caso seja muito grande
        if width > max_width or height > max_height:
            if aspect_ratio > 1: # Paisagem
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else: # Retrato
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
                
            # LANCZOS é o filtro recomendado de alta qualidade
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo # Evitar garbage collection