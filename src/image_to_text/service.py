from openai import OpenAI
from src import config

def _build_image_message(image_url: str, question: str) -> list:
  """
  (Função auxiliar) Constrói a estrutura da mensagem para a API 
  com uma imagem e um texto.
  """
  return [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": question},
        {"type": "image_url", "image_url": {"url": image_url}}
      ]
    }
  ]

def generate_description_from_image(client: OpenAI, image_url: str, question: str) -> str | None:
  """
  Envia uma imagem e uma pergunta para a API da Kluster e retorna a descrição gerada.

  Args:
      client (OpenAI): O cliente da API já inicializado.
      image_url (str): A URL da imagem a ser analisada.
      question (str): A pergunta ou instrução para o modelo.

  Returns:
      A descrição em texto gerada pelo modelo, ou None em caso de erro.
  """
  if not client:
      print("Erro: Cliente da API não foi inicializado.")
      return None

  messages = _build_image_message(image_url, question)
  
  try:
    completion = client.chat.completions.create(
      model=config.KUSTER_MODEL_NAME,
      messages=messages
    )
    return completion.choices[0].message.content
  except Exception as e:
    print(f"Ocorreu um erro ao chamar a API de imagem para texto: {e}")
    return None