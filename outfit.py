import io
import os
import requests
from PIL import Image, ImageTk, ImageDraw
import sys
import tkinter as tk
from tkinter import font
from APIs import api_key_dreamstudio, api_key_clipdrop  # Importar as chaves da API

class OutfitDesignerApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.state('zoomed')  # Maximizar a janela principal
        self.root.title("Outfit Designer")  # Definir título da janela

        self.image_path = image_path  # Caminho da imagem fornecida pelo usuário
        self.hairstyle = None  # Inicializar variáveis para as escolhas do usuário
        self.hair_color = "None"
        self.shirt = None
        self.pants = None
        self.shoes = None
        self.background = None

        self.create_hairstyle_buttons()  # Chamar método para criar botões de escolha de estilo de cabelo

    def clear_frame(self):
        # Método para limpar todos os widgets da janela
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_buttons_from_paths(self, img_paths, command, texts, title):
        # Método para criar botões a partir de imagens e textos fornecidos
        tk.Label(self.root, text=title, font=('Verdana', 20)).pack(side=tk.TOP, pady=10)  # Título da seção

        frame = tk.Frame(self.root)  # Frame para organizar os botões
        frame.pack()

        # Redimensionar todas as imagens para 400x400 pixels
        images = []
        for path in img_paths:
            img = Image.open(path)
            img = img.resize((400, 400), Image.LANCZOS)  # Redimensionar para 400x400 pixels
            photo = ImageTk.PhotoImage(img)
            images.append(photo)

        font_size = 14
        button_font = font.Font(size=font_size)

        lista_chaves = list(texts.keys())

        # Criar botões com as imagens redimensionadas e associar às funções correspondentes
        tk.Button(frame, text=lista_chaves[0], image=images[0], compound="top", command=lambda: command(texts[lista_chaves[0]]), font=button_font).grid(row=0, column=0)
        tk.Button(frame, text=lista_chaves[1], image=images[1], compound="top", command=lambda: command(texts[lista_chaves[1]]), font=button_font).grid(row=0, column=1)
        tk.Button(frame, text=lista_chaves[2], image=images[2], compound="top", command=lambda: command(texts[lista_chaves[2]]), font=button_font).grid(row=0, column=2)
        tk.Button(frame, text=lista_chaves[3], image=images[3], compound="top", command=lambda: command(texts[lista_chaves[3]]), font=button_font).grid(row=1, column=0)
        tk.Button(frame, text=lista_chaves[4], image=images[4], compound="top", command=lambda: command(texts[lista_chaves[4]]), font=button_font).grid(row=1, column=1)
        tk.Button(frame, text=lista_chaves[5], image=images[5], compound="top", command=lambda: command(texts[lista_chaves[5]]), font=button_font).grid(row=1, column=2)

        self.root.mainloop()

    def create_hairstyle_buttons(self):
        # Método para criar botões de escolha de estilo de cabelo
        img_paths = [
            r"Icons\Outfits\Hair\long.png",
            r"Icons\Outfits\Hair\short.png",
            r"Icons\Outfits\Hair\bald.png",
            r"Icons\Outfits\Hair\afro.png",
            r"Icons\Outfits\Hair\braids.png",
            r"Icons\Outfits\Hair\mullet.png"
        ]

        hairstyles = {
            "Comprido": "Cabelo longo e elegante.",
            "Curto": "Cabelo curto e prático.",
            "Careca": "Look moderno e careca, fácil de manter.",
            "Afro": "Estilo afro naturalmente volumoso e encaracolado.",
            "Tranças": "Tranças elegantes, tradicionais e protetoras.",
            "Mullet": "Estilo mullet distintivo, negócios na frente, festa atrás."
        }
        self.create_buttons_from_paths(img_paths, self.set_hairstyle, hairstyles, "Selecione o estilo de cabelo")

    def set_hairstyle(self, hairstyle):
        # Método para definir o estilo de cabelo escolhido pelo usuário
        self.hairstyle = hairstyle
        self.clear_frame()
        if self.hairstyle != "Look moderno e careca, fácil de manter.":
            self.create_hair_color_buttons()  # Se não for careca, escolher cor do cabelo
        else:
            self.create_shirt_buttons()  # Caso contrário, escolher camisola

    def create_hair_color_buttons(self):
        # Método para criar botões de escolha de cor de cabelo
        img_paths = [
            r"Icons\Outfits\HairColors\blonde.png",
            r"Icons\Outfits\HairColors\brunette.png",
            r"Icons\Outfits\HairColors\redhead.png",
            r"Icons\Outfits\HairColors\black.png",
            r"Icons\Outfits\HairColors\gray.png",
            r"Icons\Outfits\HairColors\purple.png"
        ]

        hair_colors = {
            "Loiro": "Cabelo loiro claro e luminoso.",
            "Moreno": "Cabelo castanho escuro e rico.",
            "Ruivo": "Ruivo vibrante e ardente.",
            "Preto": "Cabelo preto clássico e ousado.",
            "Cinzento": "Cabelo grisalho sofisticado e maduro.",
            "Roxo": "Cabelo roxo único e aventureiro."
        }
        self.create_buttons_from_paths(img_paths, self.set_hair_color, hair_colors, "Selecione a cor do cabelo")

    def set_hair_color(self, hair_color):
        # Método para definir a cor do cabelo escolhida pelo usuário
        self.hair_color = hair_color
        self.clear_frame()
        self.create_shirt_buttons()

    def create_shirt_buttons(self):
        # Método para criar botões de escolha de camisola
        img_paths = [
            r"Icons\Outfits\Shirts\tshirt.png",
            r"Icons\Outfits\Shirts\sweatshirt.png",
            r"Icons\Outfits\Shirts\shirt.png",
            r"Icons\Outfits\Shirts\sweaters.png",
            r"Icons\Outfits\Shirts\polo.png",
            r"Icons\Outfits\Shirts\tanktop.png"
        ]
        shirts = {
            "T-Shirt": "T-Shirt casual e confortável.",
            "Sweatshirt": "Camisolas aconchegantes.",
            "Camisa": "Camisa versátil para ocasiões casuais e formais.",
            "Sweater": "Vestuário quente para inverno.",
            "Polo": "Camisa polo elegante.",
            "Tank Top": "Top de tanque fresco e arejado para clima quente."
        }
        self.create_buttons_from_paths(img_paths, self.set_shirt, shirts, "Selecione o tipo de camisola que deseja.")

    def set_shirt(self, shirt):
        # Método para definir o tipo de camisola escolhido pelo usuário
        self.shirt = shirt
        self.clear_frame()
        self.create_pants_buttons()

    def create_pants_buttons(self):
        # Método para criar botões de escolha de calças
        img_paths = [
            r"Icons\Outfits\Pants\jeans.png",
            r"Icons\Outfits\Pants\shorts.png",
            r"Icons\Outfits\Pants\sweatpants.png",
            r"Icons\Outfits\Pants\skirt.png",
            r"Icons\Outfits\Pants\trousers.png",
            r"Icons\Outfits\Pants\leggings.png"
        ]

        pants = {
            "Calças de Ganga": "Calças de ganga clássicas e duráveis.",
            "Calções": "Calções confortáveis para clima quente.",
            "Calças de fato de treino": "Calças de fato de treino ideais para descanso ou exercício.",
            "Saia": "Saia versátil e feminina.",
            "Calças": "Calças formais adequadas para o escritório.",
            "Leggings": "Leggings elásticas e confortáveis para treinos ou uso casual."
        }
        self.create_buttons_from_paths(img_paths, self.set_pants, pants, "Selecione o tipo de calças que deseja.")

    def set_pants(self, pants):
        # Método para definir o tipo de calças escolhido pelo usuário
        self.pants = pants
        self.clear_frame()
        self.create_shoes_buttons()

    def create_shoes_buttons(self):
        # Método para criar botões de escolha de calçado
        img_paths = [
            r"Icons\Outfits\Shoes\sneakers.png",
            r"Icons\Outfits\Shoes\boots.png",
            r"Icons\Outfits\Shoes\heels.png",
            r"Icons\Outfits\Shoes\sandals.png",
            r"Icons\Outfits\Shoes\flipflops.png",
            r"Icons\Outfits\Shoes\slippers.png"
        ]
        shoes = {
            "Sapatilhas": "Sapatilhas casuais e confortáveis para uso diário.",
            "Botas": "Botas elegantes e robustas para várias condições.",
            "Saltos Altos": "Saltos altos elegantes adequados para ocasiões formais.",
            "Sandálias": "Sandálias leves perfeitas para clima mais quente.",
            "Chinelos": "Chinelos confortáveis e práticos para uso diário.",
            "Pantufas": "Pantufas acolhedoras e confortáveis para o inverno."
        }
        self.create_buttons_from_paths(img_paths, self.set_shoes, shoes, "Selecione o tipo de calçado.")

    def set_shoes(self, shoes):
        # Método para definir o tipo de calçado escolhido pelo usuário
        self.shoes = shoes
        self.clear_frame()
        self.create_background_buttons()

    def create_background_buttons(self):
        # Método para criar botões de escolha de fundo
        img_paths = [
            r"Icons\Outfits\Backgrounds\ballroom.png",
            r"Icons\Outfits\Backgrounds\park.png",
            r"Icons\Outfits\Backgrounds\beach.png",
            r"Icons\Outfits\Backgrounds\mountains.png",
            r"Icons\Outfits\Backgrounds\city.png",
            r"Icons\Outfits\Backgrounds\forest.png"
        ]
        backgrounds = {
            "Salão de baile": "Salão de baile com lustres e decoração elegante.",
            "Parque": "Parque tranquilo com vegetação e caminhos para passeio.",
            "Praia": "Praia ensolarada com areia e ondas do oceano.",
            "Montanhas": "Montanhas cênicas com vistas deslumbrantes.",
            "Cidade": "Paisagem urbana movimentada com arranha-céus e ruas movimentadas.",
            "Floresta": "Floresta densa com árvores altas e vida selvagem."
        }
        self.create_buttons_from_paths(img_paths, self.set_background, backgrounds, "Selecione o fundo para a sua imagem")

    def set_background(self, background):
        # Método para definir o fundo escolhido pelo usuário e gerar a imagem final
        self.background = background
        self.generate_outfit()

    def generate_outfit(self):
        # Método para gerar a imagem final com o outfit selecionado pelo usuário
        self.root.destroy()  # Fechar a janela principal

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

        self.root = root

        # Montar o prompt com as escolhas do usuário
        prompt = f"Hairstyle: {self.hairstyle}, {self.hair_color}, {self.shirt}, {self.pants}, Shoes: {self.shoes}"
        search_prompt = "hair, clothes, shoes"  # Prompt de pesquisa para a API

        url = f"https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"
        headers = {
            "authorization": f"Bearer {api_key_dreamstudio}",  # Chave de API para autorização
            "accept": "image/*"
        }

        # Enviar solicitação POST para a API de edição de imagem
        response = requests.post(
            url,
            headers=headers,
            files={
                "image": open(self.image_path, "rb")  # Imagem original do usuário
            },
            data={
                "prompt": prompt,
                "search_prompt": search_prompt,
                "output_format": "jpeg",  # Formato de saída desejado
            },
        )

        if response.status_code == 200:
            edited_image_filename = f"{os.path.splitext(self.image_path)[0]}_outfit.jpg"
            with open(edited_image_filename, "wb") as file:
                file.write(response.content)  # Salvar imagem editada localmente
            print(f'Imagem salva como {edited_image_filename}')
            self.apply_background(edited_image_filename)  # Aplicar o fundo à imagem editada
        else:
            print("Error:", response.text)

    def apply_background(self, image_path):
        # Método para aplicar o fundo à imagem editada
        prompt = self.background

        # Carregar imagem editada para aplicação de fundo
        load_image(image_path)

        # Enviar solicitação POST para a API ClipDrop para substituição de fundo
        r = requests.post('https://clipdrop-api.co/replace-background/v1',
                          files={
                              'image_file': ('portrait.jpg', image_file_object, 'image/jpeg'),
                          },
                          data={'prompt': prompt},
                          headers={
                              'x-api-key': api_key_clipdrop  # Chave de API para autorização
                          })
        if r.ok:
            self.root.destroy()  # Fechar janela atual
            image = Image.open(io.BytesIO(r.content))  # Abrir imagem resultante
            filename_rplbackground = f"{os.path.splitext(image_path)[0]}_background.jpg"
            image.save(filename_rplbackground)  # Salvar imagem com fundo substituído
            print(f'Imagem salva como {filename_rplbackground}')

            # Exibir a imagem salva em uma nova janela
            root2 = tk.Tk()
            root2.state('zoomed')
            root2.title("Imagem Gerada")

            # Mostrar o nome do usuário na interface Tkinter
            user_label = tk.Label(root2, text=f"{nome} com um outfit à sua escolha!", font=('Verdana', 16))
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

            root2.mainloop()  # Iniciar loop principal da janela
        else:
            r.raise_for_status()  # Lidar com erros de solicitação

def load_image(image_path):
    # Função para carregar a imagem do usuário
    global image_file_object
    with Image.open(image_path) as input_image:
        image_file_object = image_to_byte_array(input_image)

def image_to_byte_array(image: Image):
    # Função para converter imagem PIL em array de bytes
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def main(image_path, user_name):
    # Função principal para iniciar a aplicação
    global nome
    nome = user_name
    root = tk.Tk()
    app = OutfitDesignerApp(root, image_path)
    root.mainloop()  # Iniciar loop principal da interface

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python superhero.py <image_path> <user_name>")
    else:
        main(sys.argv[1], sys.argv[2])  # Chamar função principal com argumentos da linha de comando
