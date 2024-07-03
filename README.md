# Photobooth AI

A Photobooth AI, implementada no estágio realizado na 3Decide, trata-se de uma aplicação interativa que permite aos utilizadores transformar as suas fotos através de diversos modelos de IA e APIs. Esta aplicação no estilo de cabine fotográfica oferece opções de transportação para diferentes países, transformação em super-heróis, troca de outfit, realização de desportos ou diferentes profissões, e ainda a participação num mundo cinematográfico à escolha.

## Recursos

- **Escolher Estilo**: Selecione entre diferentes estilos de transformação, incluindo destinos de viagem, super-heróis, roupa, desportos, profissões e filmes.
- **Carregar ou Capturar Fotos**: Faça upload de fotos existentes ou capture novas utilizando a sua webcam.
- **Processamento de Imagem em Tempo Real**: Utiliza a API ClipDrop para substituição de fundo e a API DreamStudio para outras transformações.
- **Interface Amigável ao Utilizador**: Interface gráfica simples e intuitiva construída com Tkinter para navegação e interação fáceis.

## Passos para execução

1. **Obter API's**:
   
   - Antes de começar, necessitará de criar contas e obter chaves de API tanto do DreamStudio como do ClipDrop.
   - **DreamStudio**: Registe-se em [DreamStudio](https://dreamstudio.com) e obtenha a sua chave de API. DreamStudio fornece 25 créditos iniciais que podem ser utilizados para adquirir transformações adicionais.
   - **ClipDrop**: Registe-se em [ClipDrop](https://clipdrop.co) e obtenha a sua chave de API. ClipDrop oferece 100 créditos iniciais que podem ser utilizados para substituição de fundo e outras funcionalidades.
   - Depois de obter as API's, substitua-as em `API'S.py`, em "your_clipdrop_api" e "your_dreamstudio_api".

3. **Instalação**

   ```bash
   git clone https://github.com/seu-nome-de-utilizador/photobooth-ai.git
   cd photobooth-ai
   pip install -r requirements.txt
   ```

4. **Executar a Aplicação**
   
   ```bash
   python main.py
   ```

## Utilização

1. **Iniciar**: Execute a aplicação e siga as instruções no ecrã.
2. **Escolher Estilo**: Selecione o estilo de transformação desejado (por exemplo, destinos de viagem, super-heróis).
3. **Carregar ou Capturar**: Carregue uma foto existente ou capture uma nova utilizando as opções fornecidas.
4. **Guardar e Partilhar**: Guarde a imagem transformada e partilhe com os seus amigos!

## Avaliação de Reconhecimento Facial

Para avaliar se os rostos nas imagens transformadas foram preservados, utilizou-se o script `evaluate_face_recognition.py`. Este script compara os rostos nas imagens originais com as imagens transformadas e calcula a taxa de preservação dos rostos.

## Resultados

Imagens de alguns resultados podem ser encontrados na pasta `Resultados`. Exemplos:

#### Imagem Original:

<td><img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/a2506496-3f12-4e5c-a036-2405dc35ba97" alt="man" style="width: 200px;"/></td>

#### Imagens Geradas:

<table>
  <tr>
    <td><img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/64fa7298-19fe-4bf7-9dff-67a72465b176" alt="man_china" style="width: 200px;"/></td>
    <td><img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/59ee82b8-090a-408e-b30e-89c2ef41b4e4" alt="man_superhero_underwater" style="width: 200px;"/></td>
         <td><img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/54782870-97af-4f9e-8613-917922ee0ab6" alt="man_outfit_background" style="width: 200px;"/></td>

  </tr>
  <tr>
    <td><img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/b5673a1d-50b9-4d47-858d-46e826a7b036" alt="man_movie_harry_potter" style="width: 200px;"/></td>
    <td><img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/39c73ea3-0907-4821-a046-c1a8849ecaa6" alt="man_profession_doctor" style="width: 200px;"/></td>
    <td><img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/318dc6d9-e3a4-4c7c-81ef-b66bc546a8b1" alt="man_sport_running" style="width: 200px;"/></td>
  </tr>
</table>

## Vídeo Demonstrativo

Clique na imagem abaixo para assistir a um vídeo demonstrativo da utilização do Photobooth AI:

<td>
  <a href="https://vimeo.com/974645542">
    <img src="https://github.com/marianaas8/PhotoboothAI_3Decide/assets/126023917/50f812ff-498d-4277-a94c-6cb678e73d68" alt="video" style="width: 600px;"/>
  </a>
</td>


## Tecnologias Utilizadas

- Python
- Tkinter
- OpenCV
- Pillow (PIL)
- Requests
- Scikit-Image
- Matplotlib

## Créditos

Este projeto utiliza APIs do ClipDrop e DreamStudio para processamento e transformação de imagens.

## Licença

Este projeto é licenciado sob os termos da [GNU GPLv3](./LICENSE.txt).

