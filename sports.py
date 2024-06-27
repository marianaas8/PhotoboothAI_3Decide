import io
import os
import requests
from PIL import Image, ImageTk, ImageDraw  # Importação dos módulos necessários
import sys
import tkinter as tk
from tkinter import font
from APIs import api_key_dreamstudio, api_key_clipdrop  # Importação das chaves de API

def escolher_desporto(image_path):
    # Função para permitir ao usuário escolher um desporto e aplicar o traje à imagem
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Escolha um desporto")

    tk.Label(root, text="Escolha o desporto que deseja praticar!", font=('Verdana', 20)).pack(side=tk.TOP, pady=10)

    # Caminhos das imagens dos desportos para os novos backgrounds
    img_paths = [
        r"Icons\Sports\soccer.png",
        r"Icons\Sports\basketball.png",
        r"Icons\Sports\running.png",
        r"Icons\Sports\swimming.png",
        r"Icons\Sports\cycling.png",
        r"Icons\Sports\tennis.png",
    ]

    def aplicar_fato(image_path, selected_sport):
        # Função para aplicar o traje escolhido à imagem
        fazer_fato(image_path, selected_sport, root)

    frame = tk.Frame(root)
    frame.pack()

    # Redimensionar todas as imagens dos desportos para 400x400 pixels
    images = []
    for path in img_paths:
        img = Image.open(path)
        img = img.resize((400, 400), Image.LANCZOS)  # Redimensionar para 400x400 pixels
        photo = ImageTk.PhotoImage(img)
        images.append(photo)

    font_size = 14
    button_font = font.Font(size=font_size)

    # Criar botões com as imagens redimensionadas e associar às funções correspondentes
    tk.Button(frame, text="Futebol", image=images[0], compound="top", command=lambda: aplicar_fato(image_path, "soccer"), font=button_font).grid(row=0, column=0)
    tk.Button(frame, text="Basquetebol", image=images[1], compound="top", command=lambda: aplicar_fato(image_path, "basketball"), font=button_font).grid(row=0, column=1)
    tk.Button(frame, text="Corrida", image=images[2], compound="top", command=lambda: aplicar_fato(image_path, "running"), font=button_font).grid(row=0, column=2)
    tk.Button(frame, text="Natação", image=images[3], compound="top", command=lambda: aplicar_fato(image_path, "swimming"), font=button_font).grid(row=1, column=0)
    tk.Button(frame, text="Ciclismo", image=images[4], compound="top", command=lambda: aplicar_fato(image_path, "cycling"), font=button_font).grid(row=1, column=1)
    tk.Button(frame, text="Ténis", image=images[5], compound="top", command=lambda: aplicar_fato(image_path, "tennis"), font=button_font).grid(row=1, column=2)

    root.mainloop()

def fazer_fato(image_path, selected_sport, root):
    # Função para aplicar o traje escolhido à imagem
    root.destroy()  # Fechar a janela anterior

    # Mostrar mensagem "A gerar imagem..."
    root = tk.Tk()
    root.title("Gerando Imagem")
    root.state('zoomed')

    # Criar um frame para centralizar o texto
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Adicionar texto ao frame
    tk.Label(frame, text="A gerar imagem...", font=('Verdana', 30)).pack()

    # Atualizar a janela para aplicar as mudanças
    root.update()

    # Prompts para cada desporto
    prompts = {
        "soccer": "A vibrant soccer uniform, featuring a moisture-wicking jersey with team colors, matching shorts, high socks, and cleats. The uniform should include the player's number and team logo on the chest.",
        "basketball": "A sleek basketball uniform, consisting of a lightweight, breathable jersey and shorts with team colors and player number. The outfit is completed with high-top sneakers designed for ankle support.",
        "running": "A dynamic running outfit, including a moisture-wicking, aerodynamic singlet and shorts, high-performance running shoes, and a sweat-absorbing headband. The outfit should be lightweight and designed for optimal movement.",
        "swimming": "A modern swimsuit, featuring a streamlined, hydrodynamic design with bold colors and patterns. The swimmer should also have a swimming cap and goggles for a complete, professional look.",
        "cycling": "A professional cycling kit, including a form-fitting, aerodynamic jersey with bold colors and sponsor logos, padded cycling shorts, and a helmet. The outfit should also feature cycling shoes with cleats.",
        "tennis": "A stylish tennis outfit, including a breathable, moisture-wicking shirt and shorts or skirt, with matching wristbands, headband, and tennis shoes. The outfit should be designed for comfort and performance on the court."
    }

    prompt = prompts[selected_sport]
    search_prompt = "clothes and shoes"

    url = f"https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"
    headers = {
        "authorization": f"Bearer {api_key_dreamstudio}",
        "accept": "image/*"
    }

    # Enviar solicitação POST para DreamStudio API
    response = requests.post(
        url,
        headers=headers,
        files={
            "image": open(image_path, "rb")
        },
        data={
            "prompt": prompt,
            "search_prompt": search_prompt,
            "output_format": "jpeg",
        },
    )

    if response.status_code == 200:
        edited_image_filename = f"{os.path.splitext(image_path)[0]}_sport.jpg"
        with open(edited_image_filename, "wb") as file:
            file.write(response.content)
        print(f'Imagem salva como {edited_image_filename}')
        aplicar_background(edited_image_filename, selected_sport, root)  # Chamada para aplicar o background
    else:
        print("Error:", response.text)

def aplicar_background(image_path, selected_sport, root):
    # Função para aplicar o background baseado no desporto escolhido
    prompts = {
        "soccer": "Vibrant green soccer field with stadium and fans",
        "basketball": "Indoor basketball court with wooden floor and hoop",
        "running": "Athletics track field with lanes and starting blocks",
        "swimming": "Olympic-size swimming pool with lanes and clear blue water",
        "cycling": "Professional cycling track with velodrome",
        "tennis": "Grass tennis court with net and baseline"
    }

    prompt = prompts[selected_sport]

    load_image(image_path)
    r = requests.post('https://clipdrop-api.co/replace-background/v1',
                      files={
                          'image_file': ('portrait.jpg', image_file_object, 'image/jpeg'),
                      },
                      data={'prompt': prompt},
                      headers={
                          'x-api-key': api_key_clipdrop
                      })

    if r.ok:
        root.destroy()  # Fechar a janela atual
        image = Image.open(io.BytesIO(r.content))  # Abrir a imagem retornada pela API ClipDrop
        filename_rplbackground = f"{os.path.splitext(image_path)[0]}_{selected_sport}.jpg"
        image.save(filename_rplbackground)  # Salvar a imagem com o novo background
        print(f'Imagem salva como {filename_rplbackground}')

        # Exibir a imagem salva em uma nova janela
        root2 = tk.Tk()
        root2.state('zoomed')
        root2.title("Imagem Gerada")

        # Mostrar o nome do usuário na interface Tkinter
        user_label = tk.Label(root2, text=f"{nome} a praticar um desporto à sua escolha!", font=('Verdana', 16))
        user_label.pack(side=tk.BOTTOM, pady=20)

        # Redimensionar a imagem para caber na altura da tela, mantendo a proporção
        original_width, original_height = image.size
        new_height = 800
        new_width = int((new_height / original_height) * original_width)  # Calcular a largura proporcional

        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        img_display = ImageTk.PhotoImage(resized_image)

        label = tk.Label(root2, image=img_display)
        label.image = img_display
        label.pack(fill=tk.BOTH, expand=tk.YES)

        root2.mainloop()
    else:
        r.raise_for_status()

def load_image(image_path):
    # Função para carregar a imagem como um objeto de bytes
    global image_file_object
    with Image.open(image_path) as input_image:
        image_file_object = image_to_byte_array(input_image)

def image_to_byte_array(image: Image):
    # Função para converter a imagem para um array de bytes
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def main(foto, user_name):
    # Função principal que inicia o processo de seleção do desporto
    global nome
    nome = user_name
    escolher_desporto(foto)

if __name__ == "__main__":
    # Verificar se foram passados os argumentos corretos na linha de comando
    if len(sys.argv) != 3:
        print("Usage: python superhero.py <image_path> <user_name>")
    else:
        main(sys.argv[1], sys.argv[2])  # Chamada da função principal com os argumentos fornecidos
