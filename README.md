# Photobooth AI

Bem-vindo ao Photobooth AI, uma aplicação interativa que permite aos utilizadores transformar as suas fotos utilizando diversos modelos de IA e APIs. Esta aplicação no estilo de cabine fotográfica oferece opções para transportar-se para diferentes lugares, transformar-se em super-heróis, trocar de roupa, praticar desportos, assumir diferentes profissões ou estrelar os seus filmes favoritos.

## Recursos

- **Escolha o seu Estilo**: Selecione entre diferentes estilos de transformação, incluindo destinos de viagem, super-heróis, roupa, desportos, profissões e filmes.
- **Carregar ou Capturar Fotos**: Faça upload de fotos existentes ou capture novas utilizando a sua webcam.
- **Processamento de Imagem em Tempo Real**: Utiliza a API ClipDrop para substituição de fundo e a API DreamStudio para outras transformações.
- **Interface Amigável ao Utilizador**: Interface gráfica simples e intuitiva construída com Tkinter para navegação e interação fáceis.

## Primeiros Passos

Antes de começar, necessitará de criar contas e obter chaves de API tanto do DreamStudio como do ClipDrop:

1. **Criar Contas**:
   - **DreamStudio**: Registe-se em [DreamStudio](https://dreamstudio.com) e obtenha a sua chave de API. DreamStudio fornece 25 créditos iniciais que podem ser usados para adquirir transformações adicionais.
   - **ClipDrop**: Registe-se em [ClipDrop](https://clipdrop.co) e obtenha a sua chave de API. ClipDrop oferece 100 créditos iniciais que podem ser utilizados para substituição de fundo e outras funcionalidades.

2. **Instalação**

   ```bash
   git clone https://github.com/seu-nome-de-utilizador/photobooth-ai.git
   cd photobooth-ai
   pip install -r requirements.txt
   ```

3. **Executar a Aplicação**
   ```bash
   python main.py
   ```

## Utilização

1. **Iniciar**: Execute a aplicação e siga as instruções no ecrã.
2. **Escolher Estilo**: Selecione o estilo de transformação desejado (por exemplo, destinos de viagem, super-heróis).
3. **Carregar ou Capturar**: Carregue uma foto existente ou capture uma nova utilizando as opções fornecidas.
4. **Guardar e Partilhar**: Guarde a imagem transformada e partilhe com os seus amigos!

## Tecnologias Utilizadas

- Python
- Tkinter
- OpenCV
- Pillow (PIL)
- Requests

## Créditos

Este projeto utiliza APIs do ClipDrop e DreamStudio para processamento e transformação de imagens.
