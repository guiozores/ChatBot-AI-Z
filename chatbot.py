import os                  # Pra acessar variáveis de ambiente e funções do sistema
import openai              # Biblioteca da OpenAI pra falar com a IA utilizando chat completion
from dotenv import load_dotenv  # Pra carregar as variáveis do arquivo .env

# Carrega as variáveis do arquivo .env (tipo a chave da API)
load_dotenv()

# Pega a chave da API que colocamos no arquivo .env
api_key = os.getenv("OPENAI_API_KEY")  # Se não existir, vai ser None

# Configura a chave da API pra biblioteca openai usar nas chamadas
openai.api_key = api_key

# Define qual modelo da OpenAI vamos usar (esse é mais barato!)
MODEL = "gpt-4o-mini"

# Quantas perguntas o usuário pode fazer antes de mostrar o resumo
QTD_PERGUNTAS = 3

# Texto completo do cardápio que será mostrado quando o cliente pedir
CARDAPIO = """Aqui está nosso cardápio:

BURGERS:
1) JOINT - R$ 46,00 - (Queijo americano, alface, tomate, cebola roxa, picles e molho especial)
2) BBQ - R$ 52,00 - (Queijo americano, bacon, cebola crispy, picles e molho barbecue)
3) JALAPEÑO - R$ 49,00 - (Gorgonzola, bacon, pimenta jalapeño, cebola roxa e sour cream)
4) LOUIS - R$ 47,00 - (Prensado com cebola, queijo americano e picles, no pão de forma)
5) MINETTA - R$ 49,00 - (Queijo cheddar inglês e cebola caramelizada)
6) J.R. BURGER - R$ 44,00 - (Double patty, queijo americano, cebola roxa, picles e molho especial)
7) LAMB - R$ 49,00 - (Burguer de cordeiro, queijo prato, cebola roxa, picles e maionese de cominho)

SNACKS, APPETIZERS & SALADS:
8) Z DELI FRIES - R$ 36,00 - (Fritas com casca, alecrim fresco e Z Powder. Servidas com maionese da casa)
9) PASTRAMI FRIES - R$ 51,00 - (Fritas com casca, pastrami desfiado, queijo fundido, sour cream e cebolinha)

BEVERAGES:
10) ÁGUA [350ml] - R$ 6,00 - (com ou sem gás)
11) COCA-COLA [250ml] - R$ 7,00 - (em vidro, normal ou sem açúcar)
12) GUARANÁ ANTÁRTICA [350ml] - R$ 7,00 - (normal ou sem açúcar)
13) TÔNICA [350ml] - R$ 7,00 - (normal ou light)
14) SCHWEPPES CITRUS [350ml] - R$ 7,00 - (normal ou leve em açúcares)
15) ÇÃ CIDER [300ml] - R$ 19,00 - (Sidra de maçã, leve e seca)
16) HEINEKEN [330ml] - R$ 17,00 - (normal ou zero álcool)

Por favor, me diga quais itens você gostaria de pedir. Aceitamos apenas pagamento via cartão (crédito/débito) ou PIX."""

# Mensagem que aparece quando o bot inicia ou quando reinicia a conversa
MENSAGEM_BOAS_VINDAS = """Olá! Bem-vindo à Hamburgueria Z! 

Estou aqui para ajudar com seu pedido. Digite "cardápio" se quiser ver as nossas opções.

Aceitamos apenas pagamento via cartão (crédito/débito) ou PIX."""

def obter_resposta(pergunta, contexto, modelo, historico=None):  # Função pra falar com a IA - recebe a pergunta, o contexto, o modelo e o histórico de mensagens
    """
    Função que consulta a API da OpenAI para responder perguntas sobre um contexto específico.
    
    Parâmetros:
        pergunta (str): A pergunta ou mensagem enviada pelo usuário
        contexto (str): O contexto que define o comportamento do chatbot
        modelo (str): O modelo de IA a ser utilizado
        historico (list): Lista de mensagens anteriores (opcional)
        
    Retorno:
        str: A resposta gerada pelo modelo de IA
    """
    # Prepara a lista de mensagens pra mandar pra API da OpenAI
    messages = []
    
    # Coloca o contexto como primeira mensagem (tipo sistema) pra dizer pra IA como se comportar
    messages.append({"role": "system", "content": contexto})
    
    # O parâmetro 'historico' é uma lista de dicionários onde cada dicionário 
    # contém uma pergunta do usuário e sua respectiva resposta da IA.
    # Formato: [{'pergunta': 'texto pergunta 1', 'resposta': 'texto resposta 1'}, 
    #           {'pergunta': 'texto pergunta 2', 'resposta': 'texto resposta 2'}, ...]
    
    # Se tiver histórico, adiciona as mensagens anteriores pra IA lembrar da conversa
    if historico:
        # Passa por cada mensagem do histórico e adiciona na lista
        for msg in historico:
            # Adiciona as perguntas como mensagens do usuário
            # Cada pergunta anterior é marcada com role "user" para a API entender
            # que foi uma mensagem enviada pelo usuário
            if 'pergunta' in msg:
                messages.append({"role": "user", "content": msg['pergunta']})
            
            # Adiciona as respostas como mensagens do assistente
            # Cada resposta anterior é marcada com role "assistant" para a API
            # entender que foi gerada pelo próprio assistente anteriormente
            if 'resposta' in msg:
                messages.append({"role": "assistant", "content": msg['resposta']})
    
    # Adiciona a pergunta atual no final da lista
    messages.append({"role": "user", "content": pergunta})
    
    # Faz a chamada pra API e pega a resposta
    # Essa é a parte que consome tokens e custa dinheiro
    response = openai.ChatCompletion.create(
        model=modelo,           # Qual modelo usar (passado como parâmetro)
        messages=messages,      # A lista de mensagens que montamos
        max_tokens=500,         # Limita o tamanho da resposta (pra economizar)
        temperature=0.7         # Controla a criatividade da resposta (0.7 é um equilíbrio bom)
    )
    
    # COMENTÁRIO DETALHADO DA EXTRAÇÃO DE CONTEÚDO DA RESPOSTA DA API:
    # response = objeto completo retornado pela API OpenAI (um dicionário com vários dados)
    # ['choices'] = lista de respostas geradas pela IA (geralmente apenas uma)
    # [0] = pegamos apenas a primeira resposta da lista (índice zero)
    # ['message'] = acessamos o objeto message que contém a resposta do assistente
    # ['content'] = finalmente extraímos apenas o texto da resposta
    
    # A estrutura completa da resposta da API é algo como:
    # {
    #   "id": "chatcmpl-123XYZ",
    #   "object": "chat.completion",
    #   "created": 1677858242,
    #   "model": "gpt-4o-mini",
    #   "usage": {"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
    #   "choices": [
    #     {
    #       "message": {
    #         "role": "assistant", 
    #         "content": "Texto da resposta da IA"
    #       },
    #       "finish_reason": "stop",
    #       "index": 0
    #     }
    #   ]
    # }
    #
    # Extraímos apenas choices[0].message.content pois só precisamos do texto da resposta,
    # ignorando todos os metadados como tokens usados, ID da resposta, etc.
    
    return response['choices'][0]['message']['content']

def usuario_pediu_cardapio(mensagem):  # Função que checa se o usuário pediu pra ver o cardápio
    """
    Verifica se o usuário está solicitando o cardápio.
    
    Parâmetros:
        mensagem (str): Mensagem enviada pelo usuário
        
    Retorno:
        bool: True se o usuário pediu o cardápio, False caso contrário
    """
    # Converte a mensagem pra minúsculo pra não se preocupar com letras maiúsculas
    mensagem = mensagem.lower()
    
    # Lista de palavras que indicam que o usuário quer ver o cardápio
    palavras_chave = ["cardapio", "cardápio", "menu", "opcoes", "opções", 
                     "opçoes", "lista", "catalogo", "catálogo", "produtos"]
    
    # Checa se alguma dessas palavras aparece na mensagem do usuário
    for palavra in palavras_chave:
        if palavra in mensagem:
            return True  # Achou uma palavra, então o usuário pediu o cardápio
    
    return False  # Não encontrou nenhuma palavra, então não pediu o cardápio

def gerar_resumo_pedido(perguntas, respostas):  # Função que pega tudo que foi conversado e extrai as informações importantes para gerar o resumo do pedido no final
    """
    Gera um resumo estruturado do pedido com base nas conversas.
    
    Parâmetros:
        perguntas (list): Lista com as perguntas do usuário
        respostas (list): Lista com as respostas do chatbot
        
    Retorno:
        str: Texto formatado com o resumo do pedido
    """
    # Cria um prompt especial pra extrair as informações do pedido
    contexto_resumo = """Você é um assistente de processamento de texto especializado em extrair informações de pedidos de hambúrgueres.
    Com base nas conversas entre cliente e atendente, extraia as seguintes informações:
    1. Quais itens foram pedidos e suas quantidades
    2. O valor total do pedido (some os preços dos itens mencionados)
    3. A forma de pagamento escolhida
    4. A forma de entrega, se vai ser entrega ou retirada. E o nome do cliente.
    
    Retorne apenas um JSON com os campos: 'itens' (lista de objetos com 'nome', 'quantidade' e 'preco'), 'valor_total' (número) e 'forma_pagamento' (string).
    Se alguma informação não estiver disponível, use o valor null."""
    
    # Junta toda a conversa em um texto só, alternando entre cliente e atendente
    conversa = ""
    for i in range(len(perguntas)):
        conversa += f"Cliente: {perguntas[i]}\nAtendente: {respostas[i]}\n\n"
    
    # Pede pra IA analisar a conversa e extrair as informações em formato JSON
    try:
        resumo_estruturado = obter_resposta(conversa, contexto_resumo, MODEL)
        return resumo_estruturado  # Retorna o JSON como texto
    except Exception as e:
        # Se der erro, retorna uma mensagem amigável
        return f"Não foi possível gerar um resumo detalhado do pedido. Erro: {str(e)}"

def contexto_chatbot():  # Função que cria o prompt pro bot se comportar como atendente de hamburgueria
    # Texto com instruções detalhadas sobre como o bot deve se comportar
    return """Você é um atendente virtual de uma hamburgueria que faz delivery.
    Você oferece os seguintes itens:
    
    BURGERS:
    1) JOINT - R$ 46,00 - (Queijo americano, alface, tomate, cebola roxa, picles e molho especial)
    2) BBQ - R$ 52,00 - (Queijo americano, bacon, cebola crispy, picles e molho barbecue)
    3) JALAPEÑO - R$ 49,00 - (Gorgonzola, bacon, pimenta jalapeño, cebola roxa e sour cream)
    4) LOUIS - R$ 47,00 - (Prensado com cebola, queijo americano e picles, no pão de forma)
    5) MINETTA - R$ 49,00 - (Queijo cheddar inglês e cebola caramelizada)
    6) J.R. BURGER - R$ 44,00 - (Double patty, queijo americano, cebola roxa, picles e molho especial)
    7) LAMB - R$ 49,00 - (Burguer de cordeiro, queijo prato, cebola roxa, picles e maionese de cominho)
    
    SNACKS, APPETIZERS & SALADS:
    8) Z DELI FRIES - R$ 36,00 - (Fritas com casca, alecrim fresco e Z Powder. Servidas com maionese da casa)
    9) PASTRAMI FRIES - R$ 51,00 - (Fritas com casca, pastrami desfiado, queijo fundido, sour cream e cebolinha)
    
    BEVERAGES:
    10) ÁGUA [350ml] - R$ 6,00 - (com ou sem gás)
    11) COCA-COLA [250ml] - R$ 7,00 - (em vidro, normal ou sem açúcar)
    12) GUARANÁ ANTÁRTICA [350ml] - R$ 7,00 - (normal ou sem açúcar)
    13) TÔNICA [350ml] - R$ 7,00 - (normal ou light)
    14) SCHWEPPES CITRUS [350ml] - R$ 7,00 - (normal ou leve em açúcares)
    15) ÇÃ CIDER [300ml] - R$ 19,00 - (Sidra de maçã, leve e seca)
    16) HEINEKEN [330ml] - R$ 17,00 - (normal ou zero álcool)
    
    Todos os hambúrgueres são preparados artesanalmente com carne premium de 180g.
    Seu objetivo é:
    1) Receber o pedido do cliente (quais itens e quantidade)
    2) Se o cliente pedir o cardápio ou menu, mostre todas as opções disponíveis
    3) A forma de entrega, se vai ser entrega ou retirada, solicitar o endereço. E o nome do cliente.
    4) Perguntar a forma de pagamento, informando que aceitamos APENAS cartão (crédito/débito) ou PIX. 
       NÃO aceitamos dinheiro vivo/em espécie.
    5) Caso o cliente demore em decidir, na terceira mensagem sempre pergunte a forma de pagamento (cartão ou PIX) 
       caso ele já tenha escolhido algum item. E tambem confirmar o endereço e forma de entrega, caso ele ainda não tenha escolhido ou solicitado.
    6)Confirmar o pedido e informar que foi colocado na fila de preparo somente após o cliente confirmar
    
    É importante calcular e informar o valor total do pedido antes de perguntar a forma de pagamento.
    
    Limite-se APENAS a esse contexto e a essas 3 interações. Não ofereça outros produtos ou serviços.
    Seja educado e cordial, mas direto e objetivo nas respostas."""

def main():  # Função principal que faz tudo funcionar junto
    """
    Função principal que controla o fluxo do chatbot da hamburgueria.
    Gerencia as interações, mostra o cardápio apenas quando solicitado e exibe o resumo do pedido.
    """
    # Mostra o título do programa com emoji de hambúrguer
    print("🍔 Bem-vindo ao Chatbot da Hamburgueria Z!")
    
    # Mostra as instruções pros comandos especiais
    print("Digite 'sair' para encerrar ou 'limpar' para iniciar uma nova conversa.")
    
    # Cria listas vazias pra guardar o histórico da conversa
    perguntas = []  # Guarda as perguntas do usuário
    respostas = []  # Guarda as respostas do bot

    # Mostra a mensagem de boas-vindas definida lá em cima
    print(f"\n🍔 Atendente: {MENSAGEM_BOAS_VINDAS}")
    
    # Loop que roda o número de vezes definido em QTD_PERGUNTAS
    for i in range(QTD_PERGUNTAS):
        # Pega o que o usuário digitou e guarda na variável pergunta
        pergunta = input(f"\nVocê: ")
        
        # Se o usuário digitou "sair", termina o programa
        if pergunta.lower() == 'sair':
            print("Encerrando o chatbot. Até logo!")
            return  # Sai da função e encerra o programa
            
        # Se o usuário digitou "limpar", reseta a conversa
        elif pergunta.lower() == 'limpar':
            perguntas = []  # Limpa a lista de perguntas
            respostas = []  # Limpa a lista de respostas
            print("Histórico de conversa limpo. Vamos começar um novo pedido!")
            print(f"\n🍔 Atendente: {MENSAGEM_BOAS_VINDAS}")
            continue  # Volta pro começo do loop
            
        # Se o usuário pediu o cardápio, mostra sem gastar uma pergunta
        elif usuario_pediu_cardapio(pergunta):
            print(f"\n🍔 Atendente: {CARDAPIO}")
            continue  # Volta pro começo do loop sem contar como pergunta
        
        # 1. ARMAZENAMENTO: Aqui a pergunta do usuário é guardada na lista de perguntas
        perguntas.append(pergunta)
        
        # 2. ENVIANDO PARA A IA: Aqui é feita a chamada para a IA
        resposta = obter_resposta(pergunta, contexto_chatbot(), MODEL, 
                                 historico=[{'pergunta': p, 'resposta': r} for p, r in zip(perguntas, respostas)])
        # ↑ A função obter_resposta envia a pergunta e o histórico para a API da OpenAI
        
        # 3. ARMAZENAMENTO: A resposta que voltou da IA é guardada na lista de respostas
        respostas.append(resposta)
        
        # 4. EXIBIÇÃO: A resposta é mostrada para o usuário
        print(f"\n🍔 Atendente: {resposta}")
    
    # Depois que acabar as perguntas, mostra o resumo do pedido
    print("\n🧾 RESUMO DO SEU PEDIDO:")
    
    # Avisa que está processando o pedido
    print("\nProcessando detalhes do pedido...")
    # Chama a função pra gerar o resumo estruturado
    resumo_estruturado = gerar_resumo_pedido(perguntas, respostas)
    # Mostra o resumo pro usuário
    print(f"\n📋 Detalhes do pedido:\n{resumo_estruturado}")
    
    # Mostra todo o histórico da conversa
    print("\n💬 Histórico da conversa:")
    for i in range(len(perguntas)):
        print(f"\nVocê: {perguntas[i]}")
        print(f"Atendente: {respostas[i]}")
        
    # Mensagem final de agradecimento
    print("\nObrigado por escolher nossa hamburgueria! Seu pedido está sendo preparado e será entregue em breve.")

# Verifica se o arquivo está sendo executado diretamente (e não importado)
if __name__ == "__main__":
    main()  # Chama a função principal
