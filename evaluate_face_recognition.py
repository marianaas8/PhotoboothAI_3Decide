import os
import cv2
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

def resize_image(image, target_size):
    """Redimensiona uma imagem para o tamanho da original."""
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

def compare_faces(original_image_path, transformed_image_path):
    # Carregar as imagens
    original = cv2.imread(original_image_path)
    transformed = cv2.imread(transformed_image_path)

    # Redimensionar a imagem transformada para o tamanho da imagem original
    transformed_resized = resize_image(transformed, (original.shape[1], original.shape[0]))

    # Pré-processamento - conversão para tons de cinzento
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    transformed_gray = cv2.cvtColor(transformed_resized, cv2.COLOR_BGR2GRAY)

    # Detectar rostos usando um detector de faces pré-treinado (Haar Cascade)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Ajustar os parâmetros scaleFactor e minNeighbors conforme necessário
    scaleFactor = 1.1
    minNeighbors = 16
    original_faces = face_cascade.detectMultiScale(original_gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    transformed_faces = face_cascade.detectMultiScale(transformed_gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

    print(f"Número de rostos na foto {os.path.basename(original_image_path)}:",  len(original_faces))
    print(f"Número de rostos na foto {os.path.basename(transformed_image_path)}:", len(transformed_faces))

    # Verificar o número de rostos detectados
    if len(original_faces) != len(transformed_faces):
        print("Número diferente de rostos detectados.")
        return False

    # Calcular a similaridade estrutural (SSIM) para cada rosto detectado
    all_faces_preserved = True
    i = 0
    for (x, y, w, h) in original_faces:
        original_face = original_gray[y:y+h, x:x+w]
        transformed_face = transformed_gray[y:y+h, x:x+w]
        sim, _ = ssim(original_face, transformed_face, full=True)
        if sim < 0.5:  # Threshold de similaridade, ajuste conforme necessário
            print(f"Rosto {i+1}: Alteração significativa detectada em {os.path.basename(transformed_image_path)}")
            all_faces_preserved = False
        else:
            print(f"Rosto {i+1}: Rosto preservado em {os.path.basename(transformed_image_path)}")
        i += 1

    return all_faces_preserved

def process_images_in_directory(directory):
    # Listar todas as imagens no diretório
    images = os.listdir(directory)

    total_images = 0
    preserved_faces = []
    altered_faces = []

    categories = {
        "filmes": 0,
        "países": 0,
        "outfits": 0,
        "superheróis": 0,
        "desportos": 0,
        "profissões": 0
    }

    for image in images:
        # Verificar se é uma imagem original (não contém "_")
        if "_" not in image:
            original_image_path = os.path.join(directory, image)

            # Procurar imagens geradas correspondentes
            base_name = os.path.splitext(image)[0]
            generated_images = [img for img in images if img.startswith(base_name + "_")]

            for generated_image in generated_images:
                generated_image_path = os.path.join(directory, generated_image)

                # Realizar o teste de preservação das caras
                print(f"\nComparando: {image} -> {generated_image}")
                if compare_faces(original_image_path, generated_image_path):
                    preserved_faces.append(generated_image_path)
                    print(f"Resultado: Rostos preservados em {generated_image}")
                else:
                    altered_faces.append(generated_image_path)
                    print(f"Resultado: Alterações detectadas em {generated_image}")

                # Atualizar contagem de categorias
                if "movie" in generated_image:
                    categories["filmes"] += 1
                elif "place" in generated_image or any(country in generated_image for country in ["greece", "japan", "uk", "usa", "italy", "china", "france", "brasil"]):
                    categories["países"] += 1
                elif "outfit" in generated_image:
                    categories["outfits"] += 1
                elif "superhero" in generated_image:
                    categories["superheróis"] += 1
                elif "sport" in generated_image:
                    categories["desportos"] += 1
                elif "profession" in generated_image:
                    categories["profissões"] += 1

                total_images += 1

    # Calcular estatísticas
    preservation_rate = len(preserved_faces) / total_images * 100 if total_images > 0 else 0

    # Exibir estatísticas
    print(f"\nEstatísticas:")
    print(f"Total de imagens processadas: {total_images}")
    print(f"Imagens com rostos preservados: {len(preserved_faces)}")
    print(f"Imagens com rostos alterados: {len(altered_faces)}")
    print(f"Nome das imagens com rostos alterados:")
    for image in altered_faces:
        print(f"   {os.path.basename(image)}")
    print(f"Taxa de preservação de rostos: {preservation_rate:.2f}%")

    # Exibir contagem por estilo
    print(f"\nContagem por estilo:")
    for category, count in categories.items():
        print(f"   Número de {category}: {count}")

    return total_images, len(preserved_faces), len(altered_faces), preservation_rate, categories

# Diretório onde estão as imagens
directory = "Resultados"

# Processar imagens no diretório
total_images, preserved_faces_count, altered_faces_count, preservation_rate, categories = process_images_in_directory(directory)

# Gerar gráfico
def generate_preservation_chart(total_images, preserved_faces_count, altered_faces_count, preservation_rate):
    labels = ['Rostos Preservados', 'Rostos Alterados']
    sizes = [preserved_faces_count, altered_faces_count]
    colors = ['#4CAF50', '#FF5733']
    explode = (0.1, 0)  # Explodir o 1º segmento

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Taxa de Preservação de Rostos')
    plt.axis('equal')  # Assegura que o gráfico seja desenhado como um círculo

    # Adicionar taxa de preservação no gráfico
    plt.text(-1.5, -1.5, f'Taxa de Preservação: {preservation_rate:.2f}%', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.show()

generate_preservation_chart(total_images, preserved_faces_count, altered_faces_count, preservation_rate)
