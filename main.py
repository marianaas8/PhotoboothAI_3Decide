import os
import cv2
import io
import requests
from tkinter.filedialog import askopenfilename
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from tkinter import font

selected_photo = None  # Variável global para armazenar o caminho da foto selecionada

def get_available_filename(prefix="picture", extension=".jpg"):
    """Função para obter um nome de arquivo disponível."""
    counter = 1
    while True:
        filename = f"{prefix}_{counter}{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

def escolher_estilo(foto):
    """Função para escolher o estilo de transformação da foto."""
    def processar_escolha(escolha):
        root.destroy()  # Fechar a janela de escolha de estilo
        if escolha == 1:
            subprocess.run(["python", "places.py", foto, user_name])
        elif escolha == 2:
            subprocess.run(["python", "superhero.py", foto, user_name])
        elif escolha == 3:
            subprocess.run(["python", "outfit.py", foto, user_name])
        elif escolha == 4:
            subprocess.run(["python", "sports.py", foto, user_name])
        elif escolha == 5:
            subprocess.run(["python", "jobs.py", foto, user_name])
        elif escolha == 6:
            subprocess.run(["python", "movies.py", foto, user_name])
        else:
            print("Escolha inválida. Por favor, digite 1, 2 ou 3.")

    # Configuração da janela principal
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Escolha o estilo da foto")

    # Rótulo para instruções ao usuário
    label = tk.Label(root, text="Escolha o estilo pretendido para a sua foto:", font=('Verdana', 20))
    label.pack(side=tk.TOP, pady=10)

    frame = tk.Frame(root)
    frame.pack()

    # Caminhos das imagens de estilo (ajuste conforme necessário)
    img_paths = [
        r"Icons\Models\places.png",
        r"Icons\Models\superhero.png",
        r"Icons\Models\outfit.png",
        r"Icons\Models\sports.png",
        r"Icons\Models\jobs.png",
        r"Icons\Models\movies.png",
    ]

    # Carregar e redimensionar as imagens de estilo
    images = []
    for path in img_paths:
        img = Image.open(path)
        img = img.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        images.append(photo)

    font_size = 14
    button_font = font.Font(size=font_size)

    # Botões para escolher o estilo
    tk.Button(frame, text="Transportar para um país à sua escolha", image=images[0], compound="top", command=lambda: processar_escolha(1), font=button_font).grid(row=0, column=0)
    tk.Button(frame, text="Transformar-se num Super-Herói", image=images[1], compound="top", command=lambda: processar_escolha(2), font=button_font).grid(row=0, column=1)
    tk.Button(frame, text="Mudar o seu outfit por completo", image=images[2], compound="top", command=lambda: processar_escolha(3), font=button_font).grid(row=0, column=2)
    tk.Button(frame, text="Fazer um desporto", image=images[3], compound="top", command=lambda: processar_escolha(4), font=button_font).grid(row=1, column=0)
    tk.Button(frame, text="Ter uma profissão à sua escolha", image=images[4], compound="top", command=lambda: processar_escolha(5), font=button_font).grid(row=1, column=1)
    tk.Button(frame, text="Participar num filme à sua escolha", image=images[5], compound="top", command=lambda: processar_escolha(6), font=button_font).grid(row=1, column=2)

    root.mainloop()

def show_photo_confirmation(foto):
    """Função para exibir a foto capturada e permitir a escolha de continuar ou tirar outra."""
    def continuar():
        filename = get_available_filename()  # Obter um nome de arquivo disponível
        img.save(filename)  # Salvar a foto confirmada
        full_path = os.path.abspath(filename)  # Obter o caminho absoluto do arquivo
        print(f"Foto capturada: {full_path}")
        root.destroy()  # Fechar a janela de confirmação
        escolher_estilo(filename)  # Chamar a função para escolher o estilo de transformação

    def tirar_outra_foto():
        root.destroy()  # Fechar a janela de confirmação
        escolher_foto()  # Chamar a função para escolher ou capturar outra foto

    # Configuração da janela principal
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Foto Capturada")

    # Rótulo para instruções ao usuário
    label = tk.Label(root, text="Ficou contente com a sua foto?", font=('Verdana', 20))
    label.pack(side=tk.TOP, pady=10)

    frame = tk.Frame(root)
    frame.pack()

    # Carregar e exibir a imagem capturada
    img = Image.open(foto)
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(frame, image=photo)
    img_label.image = photo
    img_label.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Botões para continuar ou tirar outra foto
    tk.Button(button_frame, text="Continuar", command=continuar, font=('Verdana', 14)).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Tirar outra foto", command=tirar_outra_foto, font=('Verdana', 14)).grid(row=0, column=1, padx=10)

    root.mainloop()

def escolher_foto():
    """Função para escolher ou capturar uma foto."""
    def fazer_upload():
        root.destroy()  # Fechar a janela de escolha
        arquivo = askopenfilename(
            title="Selecione uma foto",
            filetypes=[("Arquivos de imagem", "*.jpg;*.png;")]
        )
        if arquivo:
            global selected_photo
            selected_photo = arquivo
            print(f"Foto selecionada: {selected_photo}")
            escolher_estilo(selected_photo)  # Chamar a função para escolher o estilo de transformação
        else:
            print("Nenhuma foto selecionada.")
            return None

    def capturar_foto():
        root.destroy()  # Fechar a janela de escolha
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Erro: Não foi possível abrir a câmara.")
            return None

        print("A câmara foi ativada. A foto será tirada em 10 segundos.")

        # Obter largura e altura do monitor principal
        root2 = tk.Tk()
        screen_width = root2.winfo_screenwidth()
        screen_height = root2.winfo_screenheight()
        root2.destroy()

        # Definir tamanho da janela OpenCV para tela cheia
        cv2.namedWindow("Câmara", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Câmara", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.resizeWindow("Câmara", screen_width, screen_height)

        for i in range(10, 0, -1):
            ret, frame = cap.read()
            if not ret:
                print("Erro: Não foi possível capturar a imagem.")
                cap.release()
                cv2.destroyAllWindows()
                return None

            text = str(i)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(text, font, 2, 2)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = (frame.shape[0] + text_size[1]) // 2

            cv2.putText(frame, text, (text_x, text_y), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("Câmara", frame)
            cv2.waitKey(1000)

        ret, frame = cap.read()
        if not ret:
            print("Erro: Não foi possível capturar a imagem.")
            cap.release()
            cv2.destroyAllWindows()
            return None

        global selected_photo
        selected_photo = "temp.jpg"
        cv2.imwrite(selected_photo, frame)

        print(f"Foto capturada e salva temporariamente como {selected_photo}")

        cap.release()
        cv2.destroyAllWindows()

        show_photo_confirmation(selected_photo)  # Mostrar a foto capturada para confirmação

    def on_button_click(action):
        """Função para direcionar as ações dos botões de escolha de foto."""
        if action == "upload":
            fazer_upload()
        elif action == "capture":
            capturar_foto()

    # Configuração da janela principal
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Escolha uma opção:")

    # Rótulo para instruções ao usuário
    label = tk.Label(root, text="Escolha a forma como quer carregar a sua foto:", font=('Verdana', 20))
    label.pack(side=tk.TOP, pady=80)

    frame = tk.Frame(root)
    frame.pack()

    # Caminhos das imagens de escolha (ajuste conforme necessário)
    img_paths = [
        r"Icons\Upload\camera.png",
        r"Icons\Upload\upload.png",
    ]

    # Carregar e redimensionar as imagens de escolha
    images = []
    for path in img_paths:
        img = Image.open(path)
        img = img.resize((500, 500), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        images.append(photo)

    font_size = 14
    button_font = font.Font(size=font_size)

    # Botões para escolher ou capturar uma foto
    tk.Button(frame, text="Tirar uma foto com a câmara", image=images[0], compound="top", command=lambda: on_button_click("capture"), font=button_font).grid(row=0, column=0)
    tk.Button(frame, text="Fazer upload de uma foto", image=images[1], compound="top", command=lambda: on_button_click("upload"), font=button_font).grid(row=0, column=1)

    root.mainloop()

def get_user_name():
    """Função para obter o nome do usuário."""
    def submit_name():
        global user_name
        user_name = entry.get()  # Obter o nome inserido pelo usuário
        root.destroy()  # Fechar a janela de entrada de nome
        escolher_foto()  # Chamar a função para escolher ou capturar uma foto

    # Configuração da janela principal
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Digite o seu nome")

    # Rótulo para instruções ao usuário
    label = tk.Label(root, text="Digite o seu nome:", font=('Verdana', 25))
    label.pack(pady=80)

    entry = tk.Entry(root, font=('Verdana', 25))
    entry.pack(pady=80)

    button = tk.Button(root, text="Continuar", command=submit_name, font=('Verdana', 18))
    button.pack(pady=10)

    root.mainloop()

def main():
    """Função principal para iniciar o programa."""
    def start():
        root.destroy()  # Fechar a janela inicial
        get_user_name()  # Chamar a função para obter o nome do usuário

    # Configuração da janela inicial
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Photobooth AI")

    # Rótulo principal
    label = tk.Label(root, text="Photobooth AI", font=('Verdana', 60, 'bold'))
    label.pack(pady=30)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Caminhos das imagens para a janela inicial
    img_paths = [
        r"Icons\Start\3Decide.png",
        r"Icons\Start\FCUP.png",
        r"Icons\Start\FEUP.png",
        r"Icons\Start\uporto.png"
    ]

    # Redimensionar todas as imagens para exibição
    images = []
    for path in img_paths:
        img = Image.open(path)
        original_width, original_height = img.size
        new_height = 120
        new_width = int((new_height / original_height) * original_width)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        images.append(photo)

    # Exibir as imagens na janela inicial
    for i, img in enumerate(images):
        img_label = tk.Label(frame, image=img)
        img_label.grid(row=i, column=0, pady=20)
        img_label.image = img

    button = tk.Button(root, text="Iniciar", command=start, font=('Verdana', 20, 'bold'))
    button.pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    main()
