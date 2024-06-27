import io
import os
import requests
from PIL import Image, ImageTk, ImageDraw  # Importar os módulos necessários
import sys
import tkinter as tk
from tkinter import font
from APIs import api_key_dreamstudio, api_key_clipdrop  # Importar as chaves de API

# Função para carregar a imagem como um objeto de bytes
def load_image(image_path):
    global image_file_object
    with Image.open(image_path) as input_image:
        image_file_object = image_to_byte_array(input_image)

# Função para converter a imagem em um array de bytes
def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

# Função para permitir ao usuário escolher até 3 cores para o traje
def escolher_cores(image_path):
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Escolha entre 1 a 3 cores para o seu fato")

    tk.Label(root, text="Escolha as cores do seu fato!", font=('Verdana', 20)).pack(side=tk.TOP, pady=10)
    tk.Label(root, text="(selecione até 3 cores)", font=('Verdana', 14)).pack(side=tk.TOP, pady=5)

    selected_colors = []

    # Função para atualizar as cores selecionadas
    def update_selected_colors(button, color):
        if color in selected_colors:
            selected_colors.remove(color)
            button.config(relief="raised")
        elif len(selected_colors) < 3:
            selected_colors.append(color)
            button.config(relief="sunken")
        else:
            print("Você só pode selecionar até 3 cores.")
        continuar_button.config(state=tk.NORMAL if selected_colors else tk.DISABLED)

    # Definir as cores disponíveis e criar botões redondos para cada cor
    colors = [
        ("Amarelo", "yellow"),
        ("Laranja", "orange"),
        ("Vermelho", "red"),
        ("Verde", "green"),
        ("Ciano", "cyan"),
        ("Azul", "blue"),
        ("Rosa", "pink"),
        ("Roxo", "purple"),
        ("Castanho", "brown"),
        ("Preto", "black"),
        ("Cinza", "gray"),
        ("Branco", "white")
    ]

    def create_round_button(frame, color_name, color_value, row, col):
        size = 200
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, size, size), fill=color_value)
        photo = ImageTk.PhotoImage(img)

        text_color = "white" if color_value == "black" or color_value == "blue" or color_value == "purple" or color_value == "brown" else "black"
        button = tk.Button(frame, text=color_name, image=photo, compound="center", font=('Verdana', 14), fg=text_color,
                           command=lambda: update_selected_colors(button, color_value))
        button.image = photo
        button.grid(row=row, column=col, padx=10, pady=10)
        return button

    frame = tk.Frame(root)
    frame.pack()

    # Criar botões para cada cor disponível
    for i, (color_name, color_value) in enumerate(colors):
        row = i // 4
        col = i % 4
        create_round_button(frame, color_name, color_value, row, col)

    continuar_button = tk.Button(root, text="Continuar", command=lambda: escolher_background(image_path, selected_colors, root), font=('Verdana', 14), state=tk.DISABLED)
    continuar_button.pack(pady=20)

    root.mainloop()

# Função para permitir ao usuário escolher o fundo para a imagem
def escolher_background(image_path, selected_colors, root):
    root.destroy()  # Fechar a janela de cores

    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Escolha o local onde quer estar")

    tk.Label(root, text="Escolha o local onde quer estar:", font=('Verdana', 20)).pack(side=tk.TOP, pady=10)

    frame = tk.Frame(root)
    frame.pack()

    # Caminhos das imagens para os novos backgrounds
    img_paths = [
        r"Icons\Background\metropolis.png",
        r"Icons\Background\hero_hideout.png",
        r"Icons\Background\battlefield.png",
        r"Icons\Background\mystical_realm.png",
        r"Icons\Background\outer_space.png",
        r"Icons\Background\underwater.png",
    ]

    # Redimensionar todas as imagens para 400x400 pixels
    images = []
    for path in img_paths:
        img = Image.open(path)
        img = img.resize((400, 400), Image.LANCZOS)  # Redimensionar para 400x400 pixels
        photo = ImageTk.PhotoImage(img)
        images.append(photo)

    font_size = 14
    button_font = font.Font(size=font_size)

    # Criar botões com as imagens redimensionadas e associar às funções correspondentes
    tk.Button(frame, text="Cidade Futurística", image=images[0], compound="top", command=lambda: fazer_fato(image_path, selected_colors, root, "Gleaming futuristic metropolis skyline with towering skyscrapers and city lights", "metropolis"), font=button_font).grid(row=0, column=0)
    tk.Button(frame, text="Esconderijo Secreto", image=images[1], compound="top", command=lambda: fazer_fato(image_path, selected_colors, root, "Secret superhero hideout with high-tech gadgets and computer displays", "hero_hideout"), font=button_font).grid(row=0, column=1)
    tk.Button(frame, text="Campo de Batalha", image=images[2], compound="top", command=lambda: fazer_fato(image_path, selected_colors, root, "Destructive battlefield with smoke, ruins, and dramatic skies", "battlefield"), font=button_font).grid(row=0, column=2)
    tk.Button(frame, text="Reino Místico", image=images[3], compound="top", command=lambda: fazer_fato(image_path, selected_colors, root, "Realistic mystical realm with floating islands, magical runes, and ethereal light", "mystical_realm"), font=button_font).grid(row=1, column=0)
    tk.Button(frame, text="Espaço Sideral", image=images[4], compound="top", command=lambda: fazer_fato(image_path, selected_colors, root, "Vast outer space with distant galaxies, nebulae, and cosmic phenomena", "outer_space"), font=button_font).grid(row=1, column=1)
    tk.Button(frame, text="Mundo marítimo", image=images[5], compound="top", command=lambda: fazer_fato(image_path, selected_colors, root, "Realistic blue underwater world with colorful coral reefs and marine life", "underwater"), font=button_font).grid(row=1, column=2)

    root.mainloop()

# Função para aplicar o traje escolhido e o background à imagem
def fazer_fato(image_path, selected_colors, root, prompt_bg, name):
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

    # Descrições das cores para o prompt da API
    cores = {
        "yellow": "vibrant yellow",
        "orange": "bold orange",
        "red": "bold red",
        "green": "vibrant green",
        "cyan": "bright cyan",
        "blue": "vibrant blue",
        "pink": "bright pink",
        "purple": "bold purple",
        "brown": "earthy brown",
        "black": "sleek black",
        "gray": "modern gray",
        "white": "clean white"
    }

    # Construir a string com as descrições das cores selecionadas
    color_descriptions = [cores[color] for color in selected_colors]
    color_str = " and ".join(color_descriptions)
    prompt = f"A superhero suit combining {color_str} hues, adorned with sleek designs and metallic accents, complete with a flowing cape for added flair."
    search_prompt = "clothes and shoes"

    url = f"https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"
    headers = {
        "authorization": f"Bearer {api_key_dreamstudio}",
        "accept": "image/*"
    }

    # Enviar uma requisição POST com o arquivo de imagem e outros dados
    response = requests.post(
        url,
        headers=headers,
        files={
            "image":  open(image_path, "rb")
        },
        data={
            "prompt": prompt,
            "search_prompt": search_prompt,
            "output_format": "jpeg",  # Formato de saída da imagem
        },
    )

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        edited_image_filename = f"{os.path.splitext(image_path)[0]}_superhero.jpg"
        with open(edited_image_filename, "wb") as file:
            file.write(response.content)
        print(f'Imagem salva como {edited_image_filename}')
        aplicar_background(prompt_bg, name, edited_image_filename, root)
    else:
        # Exibir mensagem de erro se a requisição falhar
        print("Error:", response.text)

# Função para aplicar o background à imagem com a API ClipDrop
def aplicar_background(prompt, name, edited_image, root):
    load_image(edited_image)  # Carregar a imagem editada como objeto de bytes
    r = requests.post('https://clipdrop-api.co/replace-background/v1',
                      files={
                          'image_file': ('portrait.jpg', image_file_object, 'image/jpeg'),
                      },
                      data={'prompt': prompt},
                      headers={
                          'x-api-key': api_key_clipdrop
                      })

    if r.ok:
        # r.content contém os bytes da imagem retornada
        image_with_background = Image.open(io.BytesIO(r.content))
        filename_rplbackground = f"{os.path.splitext(edited_image)[0]}_{name}.jpg"
        image_with_background.save(filename_rplbackground)
        print(f'Imagem salva como {filename_rplbackground}')
        root.destroy()  # Fechar a janela de cores

        # Exibir a imagem salva em uma nova janela
        root2 = tk.Tk()
        root2.state('zoomed')  # Maximizar a janela
        root2.title("Imagem Gerada")

        # Mostrar o nome do usuário na interface Tkinter
        user_label = tk.Label(root2, text=f"{nome} como um superherói!", font=('Verdana', 16))
        user_label.pack(side=tk.BOTTOM, pady=20)

        # Redimensionar a imagem para caber na altura da tela, mantendo a proporção
        original_width, original_height = image.size
        new_height = 800
        new_width = int((new_height / original_height) * original_width)  # Calcular a largura proporcional

        resized_image = image_with_background.resize((new_width, new_height), Image.LANCZOS)
        img_display = ImageTk.PhotoImage(resized_image)

        label = tk.Label(root2, image=img_display)
        label.image = img_display
        label.pack(fill=tk.BOTH, expand=tk.YES)

        root2.mainloop()
    else:
        r.raise_for_status()

# Função principal para iniciar o processo de escolha de cores
def main(foto, user_name):
    global nome
    nome = user_name
    escolher_cores(foto)

# Verificar se o script está sendo executado diretamente
if __name__ == "__main__":
    # Verificar se os argumentos corretos foram passados na linha de comando
    if len(sys.argv) != 3:
        print("Usage: python superhero.py <image_path> <user_name>")
    else:
        main(sys.argv[1], sys.argv[2])  # Chamada da função principal com os argumentos fornecidos
