import tkinter as tk
from main import NASA_API
from ui import ApplicationWindow

def main():
    # Instancia o cliente da API
    api_client = NASA_API()
    
    # Cria a janela principal do Tkinter
    main_application_window = tk.Tk()
    
    # Instancia a interface, injetando a janela principal e o cliente da API
    application_instance = ApplicationWindow(main_application_window, api_client)
    
    # Inicia o loop da aplicação
    main_application_window.mainloop()

if __name__ == "__main__":
    main()
