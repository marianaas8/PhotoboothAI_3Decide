import io
import os
import requests
from PIL import Image, ImageTk
import sys
import tkinter as tk
from tkinter import font
from APIs import api_key_dreamstudio, api_key_clipdrop  # Importação das chaves de API

def escolher_filme(image_path):
    # Função para escolher o mundo cinematográfico para participar
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Escolha um filme")

    tk.Label(root, text="Escolha o mundo cinematográfico em que quer participar!", font=('Verdana', 20)).pack(side=tk.TOP, pady=10)

    # Caminhos das imagens dos filmes para os novos backgrounds
    img_paths = [
        r"Icons\Movies\harry_potter.png",
        r"Icons\Movies\star_wars.png",
        r"Icons\Movies\marvel.png",
        r"Icons\Movies\twilight.png",
        r"Icons\Movies\pirates_of_the_caribbean.png",
        r"Icons\Movies\matrix.png",
    ]

    def aplicar_fato(image_path, selected_movie):
        # Função para aplicar o fato baseado no filme escolhido
        fazer_fato(image_path, selected_movie, root)

    frame = tk.Frame(root)
    frame.pack()

    # Redimensionar todas as imagens dos filmes para 400x400 pixels
    images = []
    for path in img_paths:
        img = Image.open(path)
        img = img.resize((400, 400), Image.LANCZOS)  # Redimensionar para 400x400 pixels
        photo = ImageTk.PhotoImage(img)
        images.append(photo)

    font_size = 14
    button_font = font.Font(size=font_size)

    # Criar botões com as imagens redimensionadas e associar às funções correspondentes
    tk.Button(frame, text="Harry Potter", image=images[0], compound="top", command=lambda: aplicar_fato(image_path, "harry_potter"), font=button_font).grid(row=0, column=0)
    tk.Button(frame, text="Star Wars", image=images[1], compound="top", command=lambda: aplicar_fato(image_path, "star_wars"), font=button_font).grid(row=0, column=1)
    tk.Button(frame, text="Marvel", image=images[2], compound="top", command=lambda: aplicar_fato(image_path, "marvel"), font=button_font).grid(row=0, column=2)
    tk.Button(frame, text="Twilight", image=images[3], compound="top", command=lambda: aplicar_fato(image_path, "twilight"), font=button_font).grid(row=1, column=0)
    tk.Button(frame, text="Piratas das Caraíbas", image=images[4], compound="top", command=lambda: aplicar_fato(image_path, "pirates_of_the_caribbean"), font=button_font).grid(row=1, column=1)
    tk.Button(frame, text="Matrix", image=images[5], compound="top", command=lambda: aplicar_fato(image_path, "matrix"), font=button_font).grid(row=1, column=2)

    root.mainloop()

def fazer_fato(image_path, selected_movie, root):
    # Função para aplicar o fato baseado no filme escolhido
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

    # Prompts para cada filme
    prompts = {
        "harry_potter": "A wizard outfit, including a robe, wand, and Hogwarts emblem. The outfit should reflect a magical environment.",
        "star_wars": "A Star Wars character outfit, featuring a lightsaber, futuristic clothing, and accessories. The attire should be suitable for a sci-fi environment.",
        "marvel": "A superhero outfit, including a costume with the emblem of a popular Marvel character. The attire should be dynamic and heroic.",
        "twilight": "A modern, dark outfit suitable for a vampire. The attire should reflect a mysterious and romantic environment.",
        "pirates_of_the_caribbean": "A pirate's outfit, featuring a tricorn hat, coat, and accessories. The attire should be suitable for a pirate adventure.",
        "matrix": "A futuristic outfit, including a long black trench coat, sunglasses, and a sleek, modern look. The attire should reflect a cyberpunk environment."
    }

    prompt = prompts[selected_movie]
    search_prompt = "clothes and shoes"

    # URL e cabeçalhos para a API DreamStudio
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
        edited_image_filename = f"{os.path.splitext(image_path)[0]}_movie.jpg"
        with open(edited_image_filename, "wb") as file:
            file.write(response.content)
        print(f'Imagem salva como {edited_image_filename}')
        aplicar_background(edited_image_filename, selected_movie, root)  # Chamada para aplicar o background
    else:
        print("Error:", response.text)

def aplicar_background(image_path, selected_movie, root):
    # Função para aplicar o background baseado no filme escolhido
    prompts = {
        "harry_potter": "A Hogwarts setting with magical elements and castle.",
        "star_wars": "A space setting with spaceships and futuristic elements.",
        "marvel": "A superhero cityscape with tall buildings and action.",
        "twilight": "A dark, forest setting with a mysterious atmosphere.",
        "pirates_of_the_caribbean": "A pirate ship or island with ocean and treasure.",
        "matrix": "A futuristic cityscape with neon lights and cyberpunk elements."
    }

    prompt = prompts[selected_movie]

    load_image(image_path)  # Carregar a imagem para ser usada
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
        filename_rplbackground = f"{os.path.splitext(image_path)[0]}_{selected_movie}.jpg"
        image.save(filename_rplbackground)  # Salvar a imagem com o novo background
        print(f'Imagem salva como {filename_rplbackground}')

        # Exibir a imagem salva em uma nova janela
        root2 = tk.Tk()
        root2.state('zoomed')
        root2.title("Imagem Gerada")

        # Mostrar o nome do usuário na interface Tkinter
        user_label = tk.Label(root2, text=f"{nome} num mundo cinematográfico à sua escolha!", font=('Verdana', 16))
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
    # Função principal para iniciar o programa
    global nome
    nome = user_name
    escolher_filme(foto)  # Chamada para iniciar a escolha do filme

if __name__ == "__main__":
    # Verificar se foram passados os argumentos corretos na linha de comando
    if len(sys.argv) != 3:
        print("Usage: python superhero.py <image_path> <user_name>")
    else:
        main(sys.argv[1], sys.argv[2])  # Chamada da função principal com os argumentos fornecidos
