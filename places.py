import io
import os
import requests
import cv2
import numpy as np
import sys
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from APIs import api_key_dreamstudio, api_key_clipdrop  # Importar chaves de API

global image_file_object  # Variável global para armazenar a imagem como array de bytes

def load_image(image_path):
    global image_file_object
    # Função para carregar a imagem do usuário e convertê-la em array de bytes
    with Image.open(image_path) as input_image:
        image_file_object = image_to_byte_array(input_image)

def image_to_byte_array(image: Image):
    # Função para converter imagem PIL em array de bytes
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def escolha_pais(image_path, prompt, place, root):
    # Função para escolher o país e aplicar o fundo correspondente à imagem
    # Fechar a janela anterior
    root.destroy()

    # Mostrar a mensagem "a gerar imagem..."
    root = tk.Tk()
    root.title("Gerando Imagem")
    root.state('zoomed')

    # Criar um frame para centralizar o texto
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Adicionar o texto ao frame
    tk.Label(frame, text="A gerar imagem...", font=('Verdana', 30)).pack()

    # Atualizar a janela para aplicar as mudanças
    root.update()

    load_image(image_path)

    # Enviar solicitação POST para a API ClipDrop para substituição de fundo
    r = requests.post('https://clipdrop-api.co/replace-background/v1',
                      files={'image_file': ('portrait.jpg', image_file_object, 'image/jpeg')},
                      data={'prompt': prompt},
                      headers={'x-api-key': api_key_clipdrop})

    if r.ok:
        # r.content contém os bytes da imagem retornada
        image_data = r.content

        # Fechar a janela Tkinter
        root.destroy()

        # Abrir a imagem resultante
        image = Image.open(io.BytesIO(image_data))

        # Salvar a imagem com o fundo substituído localmente
        filename_rplbackground = f"{os.path.splitext(image_path)[0]}_{place}.jpg"
        image.save(filename_rplbackground)
        print(f'Imagem salva como {filename_rplbackground}')

        # Exibir a imagem salva em uma nova janela
        root2 = tk.Tk()
        root2.state('zoomed')
        root2.title("Imagem Gerada")

        # Mostrar o nome do usuário na interface Tkinter
        user_label = tk.Label(root2, text=f"{nome} num país à sua escolha!", font=('Verdana', 16))
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

        root2.mainloop()  # Iniciar loop principal da janela Tkinter
    else:
        r.raise_for_status()  # Lidar com erros de solicitação HTTP

def main(foto, user_name):
    global nome
    nome = user_name

    root = tk.Tk()
    root.state('zoomed')
    root.title("Escolha o país")

    tk.Label(root, text="Escolha o país onde pretende estar:", font=('Verdana', 20)).pack(side=tk.TOP, pady=10)

    # Funções para escolher cada país e aplicar o fundo correspondente à imagem
    def escolher_franca():
        escolha_pais(foto, "A romantic evening stroll along the Seine River, with the sparkling lights of the Eiffel Tower illuminating the skyline, couples sharing kisses beneath the shadow of Notre-Dame Cathedral, and the aroma of freshly baked baguettes drifting from nearby boulangeries.", "france", root)

    def escolher_uk():
        escolha_pais(foto, "A bright and sunny morning in London, with the streets filled with people, the London Eye and Big Ben glistening in the sunlight against a backdrop of clear blue skies.", "uk", root)

    def escolher_china():
        escolha_pais(foto, "A sunny day in Beijing's Forbidden City, with the ancient palace complex gleaming in the sunlight, tourists exploring the grand courtyards and intricate architecture, and traditional Chinese dragons adorning the rooftops.", "china", root)

    def escolher_usa():
        escolha_pais(foto, "A sunny afternoon in Times Square, New York City, with the hustle and bustle of pedestrians, vibrant billboards lighting up the streets, and the iconic yellow taxis zipping through the bright cityscape", "usa", root)

    def escolher_grecia():
        escolha_pais(foto, "A sunny afternoon in Santorini, Greece, with whitewashed buildings perched on cliffs overlooking the azure sea, colorful bougainvillea blooming in the sunlight, and tourists soaking up the warmth while sipping on cool drinks at seaside cafes.", "greece", root)

    def escolher_brasil():
        escolha_pais(foto, "A sunny day on Rio de Janeiro's Copacabana Beach, with golden sands stretching along the coastline, beachgoers lounging under colorful umbrellas, and the iconic Christ the Redeemer statue standing against a backdrop of clear, blue skies.", "brasil", root)

    def escolher_japao():
        escolha_pais(foto, "A serene morning in Kyoto, Japan, with cherry blossom trees in full bloom, traditional wooden temples standing amidst lush gardens, and the tranquil Kinkaku-ji reflecting in the peaceful waters of its surrounding pond.", "japan", root)

    def escolher_italia():
        escolha_pais(foto, "A romantic evening in Venice, Italy, with gondolas gliding through the picturesque canals, historic buildings illuminated by soft lights, and the sounds of musicians playing classical melodies echoing through narrow streets.", "italy", root)

    frame = tk.Frame(root)
    frame.pack()

    # Caminhos das imagens dos países (ajuste conforme necessário)
    img_paths = [
        r"Icons\Country\france.png",
        r"Icons\Country\uk.png",
        r"Icons\Country\china.png",
        r"Icons\Country\usa.png",
        r"Icons\Country\greece.png",
        r"Icons\Country\brasil.png",
        r"Icons\Country\japan.png",
        r"Icons\Country\italy.png",
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

    # Criar botões com as imagens redimensionadas
    tk.Button(frame, text="França", image=images[0], compound="top", command=escolher_franca, font=button_font).grid(row=0, column=0)
    tk.Button(frame, text="Inglaterra", image=images[1], compound="top", command=escolher_uk, font=button_font).grid(row=0, column=1)
    tk.Button(frame, text="China", image=images[2], compound="top", command=escolher_china, font=button_font).grid(row=0, column=2)
    tk.Button(frame, text="EUA", image=images[3], compound="top", command=escolher_usa, font=button_font).grid(row=0, column=3)
    tk.Button(frame, text="Grécia", image=images[4], compound="top", command=escolher_grecia, font=button_font).grid(row=1, column=0)
    tk.Button(frame, text="Brasil", image=images[5], compound="top", command=escolher_brasil, font=button_font).grid(row=1, column=1)
    tk.Button(frame, text="Japão", image=images[6], compound="top", command=escolher_japao, font=button_font).grid(row=1, column=2)
    tk.Button(frame, text="Itália", image=images[7], compound="top", command=escolher_italia, font=button_font).grid(row=1, column=3)

    root.mainloop()  # Iniciar loop principal da interface gráfica

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python superhero.py <image_path> <user_name>")
    else:
        main(sys.argv[1], sys.argv[2])
