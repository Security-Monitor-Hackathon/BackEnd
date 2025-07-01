# 1. Imagem Base: imagem oficial do Python, versão 3.13.
# A tag '-slim' indica uma versão mais leve, ideal para produção.
FROM python:3.13.5

# 2. Diretório de Trabalho: Define o diretório de trabalho dentro do container.
# Todos os comandos a seguir serão executados a partir de /app.
WORKDIR /app

# 3. Instalação de Dependências:
# Copia apenas o arquivo de requisitos primeiro. Isso aproveita o cache do Docker.
# Se o requirements.txt não mudar, o Docker não reinstalará as dependências em builds futuros.
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt.
# --no-cache-dir economiza espaço na imagem final.
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiando o Código-Fonte:
# Copia todo o resto do código do projeto para o diretório de trabalho no container.
COPY . .

# 5. Comando de Execução:
# Define o comando padrão que será executado quando o container iniciar.
# Neste caso, ele rodará nosso pipeline completo.
CMD ["python", "pipeline.py"]