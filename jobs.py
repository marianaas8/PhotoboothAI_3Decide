import io
import os
import requests
from PIL import Image, ImageTk, ImageDraw  # Importação dos módulos necessários
import sys
import tkinter as tk
from tkinter import font
from APIs import api_key_dreamstudio, api_key_clipdrop  # Importação das chaves de API

def escolher_profissao(image_path):
    # Função para escolher a profissão a ser aplicada na imagem
    root = tk.Tk()
    root.state('zoomed')  # Maximizar a janela
    root.title("Escolha uma profissão")

    tk.Label(root, text="Escolha a profissão que deseja praticar!", font=('Verdana', 20)).pack(side=tk.TOP, pady=10)

    # Caminhos das imagens das profissões para os novos backgrounds
    img_paths = [
        r"Icons\Jobs\doctor.png",
        r"Icons\Jobs\police_officer.png",
        r"Icons\Jobs\chef.png",
        r"Icons\Jobs\firefighter.png",
        r"Icons\Jobs\teacher.png",
        r"Icons\Jobs\engineer.png",
    ]

    def aplicar_fato(image_path, selected_profession):
        # Função para aplicar a profissão escolhida à imagem
        fazer_fato(image_path, selected_profession, root)

    frame = tk.Frame(root)
    frame.pack()

    # Redimensionar todas as imagens das profissões para 400x400 pixels
    images = []
    for path in img_paths:
        img = Image.open(path)
        img = img.resize((400, 400), Image.LANCZOS)  # Redimensionar para 400x400 pixels
        photo = ImageTk.PhotoImage(img)
        images.append(photo)

    font_size = 14
    button_font = font.Font(size=font_size)

    # Criar botões com as imagens redimensionadas e associar às funções correspondentes
    tk.Button(frame, text="Médico", image=images[0], compound="top", command=lambda: aplicar_fato(image_path, "doctor"), font=button_font).grid(row=0, column=0)
    tk.Button(frame, text="Polícia", image=images[1], compound="top", command=lambda: aplicar_fato(image_path, "police_officer"), font=button_font).grid(row=0, column=1)
    tk.Button(frame, text="Chef", image=images[2], compound="top", command=lambda: aplicar_fato(image_path, "chef"), font=button_font).grid(row=0, column=2)
    tk.Button(frame, text="Bombeiro", image=images[3], compound="top", command=lambda: aplicar_fato(image_path, "firefighter"), font=button_font).grid(row=1, column=0)
    tk.Button(frame, text="Professor", image=images[4], compound="top", command=lambda: aplicar_fato(image_path, "teacher"), font=button_font).grid(row=1, column=1)
    tk.Button(frame, text="Engenheiro", image=images[5], compound="top", command=lambda: aplicar_fato(image_path, "engineer"), font=button_font).grid(row=1, column=2)

    root.mainloop()

def fazer_fato(image_path, selected_profession, root):
    # Função para aplicar a profissão escolhida à imagem
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

    # Prompts para cada profissão
    prompts = {
        "doctor": "A professional doctor's outfit, including a white lab coat, stethoscope, and a name badge. The attire should reflect a medical environment.",
        "police_officer": "A police officer's uniform, featuring a navy blue shirt, matching pants, belt with necessary equipment, and a police hat. The outfit should be complete with a badge and a name tag.",
        "chef": "A chef's uniform, including a white double-breasted jacket, checkered pants, apron, and a chef's hat. The attire should be suitable for a professional kitchen.",
        "firefighter": "A firefighter's gear, consisting of a fire-resistant suit, helmet, gloves, and boots. The outfit should be suitable for emergency response.",
        "teacher": "A professional teacher's outfit, including a business casual attire with a name tag and accessories suitable for a classroom environment.",
        "engineer": "An engineer's uniform, featuring a hard hat, safety vest, and tools. The attire should be suitable for a construction or technical environment."
    }

    prompt = prompts[selected_profession]
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
        edited_image_filename = f"{os.path.splitext(image_path)[0]}_profession.jpg"
        with open(edited_image_filename, "wb") as file:
            file.write(response.content)
        print(f'Imagem salva como {edited_image_filename}')
        aplicar_background(edited_image_filename, selected_profession, root)  # Chamada para aplicar o background
    else:
        print("Error:", response.text)

def aplicar_background(image_path, selected_profession, root):
    # Função para aplicar o background baseado na profissão escolhida
    prompts = {
        "doctor": "A hospital setting with medical equipment and patient beds",
        "police_officer": "A police station or city street with police vehicles",
        "chef": "A professional kitchen with cooking equipment and ingredients",
        "firefighter": "A fire station or scene of a fire emergency",
        "teacher": "A classroom with students and a blackboard",
        "engineer": "A construction site with heavy machinery and blueprints"
    }

    prompt = prompts[selected_profession]

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
        filename_rplbackground = f"{os.path.splitext(image_path)[0]}_{selected_profession}.jpg"
        image.save(filename_rplbackground)  # Salvar a imagem com o novo background
        print(f'Imagem salva como {filename_rplbackground}')

        # Exibir a imagem salva em uma nova janela
        root2 = tk.Tk()
        root2.state('zoomed')
        root2.title("Imagem Gerada")

        # Mostrar o nome do usuário na interface Tkinter
        user_label = tk.Label(root2, text=f"{nome} na profissão à sua escolha!", font=('Verdana', 16))
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
    escolher_profissao(foto)  # Chamada para iniciar a escolha da profissão

if __name__ == "__main__":
    # Verificar se foram passados os argumentos corretos na linha de comando
    if len(sys.argv) != 3:
        print("Usage: python superhero.py <image_path> <user_name>")
    else:
        main(sys.argv[1], sys.argv[2])  # Chamada da função principal com os argumentos fornecidos
