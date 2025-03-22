import os                  # Para acessar variáveis de ambiente
import openai              # Biblioteca da OpenAI para integração com a API (versão 0.28.1)
from dotenv import load_dotenv  # Para carregar variáveis de ambiente do arquivo .env

###########################################
# BLOCO DE CONFIGURAÇÃO INICIAL
###########################################

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API da OpenAI da variável de ambiente
api_key = os.getenv("OPENAI_API_KEY")

# Configurando a chave API globalmente para a biblioteca openai
openai.api_key = api_key

# Definir o modelo a ser utilizado
MODEL = "gpt-4o-mini"

# Quantidade de perguntas que o usuário poderá fazer antes de mostrar resumo
QTD_PERGUNTAS = 3

###########################################
# BLOCO DE DEFINIÇÃO DO CARDÁPIO
###########################################

# Texto do cardápio que será mostrado apenas quando solicitado
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

# Mensagem de boas-vindas concisa
MENSAGEM_BOAS_VINDAS = """Olá! Bem-vindo à Hamburgueria Z! 

Estou aqui para ajudar com seu pedido. Digite "cardápio" se quiser ver as nossas opções.

Aceitamos apenas pagamento via cartão (crédito/débito) ou PIX."""

###########################################
# BLOCO DE FUNÇÃO DE COMUNICAÇÃO COM A API
###########################################

def obter_resposta(pergunta, contexto, modelo):
    """
    Função que consulta a API da OpenAI para responder perguntas sobre um contexto específico.
    
    Parâmetros:
        pergunta (str): A pergunta ou mensagem enviada pelo usuário
        contexto (str): O contexto que define o comportamento do chatbot
        modelo (str): O modelo de IA a ser utilizado
        
    Retorno:
        str: A resposta gerada pelo modelo de IA
    """
    response = openai.ChatCompletion.create(
        model=modelo,           # Modelo de IA a ser usado (gpt-4o-mini)
        messages=[
            {"role": "system", "content": contexto},  # Instrução de sistema que define o papel do chatbot
            {"role": "user", "content": pergunta}     # Mensagem do usuário
        ],
        max_tokens=500,         # Limita o tamanho da resposta
        temperature=0.7         # Controla a aleatoriedade da resposta (0.7 é moderadamente criativo)
    )
    return response['choices'][0]['message']['content']  # Extrai o texto da resposta

###########################################
# FUNÇÃO PARA VERIFICAR SE USUÁRIO PEDE CARDÁPIO
###########################################

def usuario_pediu_cardapio(mensagem):
    ####################################
    """
    Verifica se o usuário está solicitando o cardápio.
    
    Parâmetros:
        mensagem (str): Mensagem enviada pelo usuário
        
    Retorno:
        bool: True se o usuário pediu o cardápio, False caso contrário
        
    Nota: Quando o usuário solicita o cardápio, essa interação NÃO é enviada para a OpenAI.
    O sistema exibe o cardápio pré-definido e usa 'continue' para pular o resto do loop,
    o que significa que a pergunta não é armazenada, a resposta não é armazenada,
    e nenhuma chamada à API da OpenAI é feita, economizando tokens.
    """
    ####################################
    # Converter a mensagem para minúsculas para facilitar a comparação
    mensagem = mensagem.lower()
    
    # Lista de palavras-chave que podem indicar que o usuário quer ver o cardápio
    palavras_chave = ["cardapio", "cardápio", "menu", "opcoes", "opções", 
                     "opçoes", "lista", "catalogo", "catálogo", "produtos"]
    
    # Verificar se alguma das palavras-chave está na mensagem
    for palavra in palavras_chave:
        if palavra in mensagem:
            return True
    
    return False

###########################################
# FUNÇÃO PARA GERAR RESUMO ESTRUTURADO
###########################################

def gerar_resumo_pedido(perguntas, respostas):
    """
    Gera um resumo estruturado do pedido com base nas conversas.
    
    Parâmetros:
        perguntas (list): Lista com as perguntas do usuário
        respostas (list): Lista com as respostas do chatbot
        
    Retorno:
        str: Texto formatado com o resumo do pedido
    """
    # Criar um contexto para extrair informações do pedido
    contexto_resumo = """Você é um assistente de processamento de texto especializado em extrair informações de pedidos de hambúrgueres.
    Com base nas conversas entre cliente e atendente, extraia as seguintes informações:
    1. Quais itens foram pedidos e suas quantidades
    2. O valor total do pedido (some os preços dos itens mencionados)
    3. A forma de pagamento escolhida
    
    Retorne apenas um JSON com os campos: 'itens' (lista de strings), 'valor_total' (número) e 'forma_pagamento' (string).
    Se alguma informação não estiver disponível, use o valor null."""
    
    # Combinar as conversas em um formato que facilite a extração
    conversa = ""
    for i in range(len(perguntas)):
        conversa += f"Cliente: {perguntas[i]}\nAtendente: {respostas[i]}\n\n"
    
    # Obter um resumo estruturado via API
    try:
        resumo_estruturado = obter_resposta(conversa, contexto_resumo, MODEL)
        return resumo_estruturado
    except Exception as e:
        return f"Não foi possível gerar um resumo detalhado do pedido. Erro: {str(e)}"

###########################################
# BLOCO DA FUNÇÃO PRINCIPAL
###########################################

def main():
    """
    Função principal que controla o fluxo do chatbot da hamburgueria.
    Gerencia as interações, mostra o cardápio apenas quando solicitado e exibe o resumo do pedido.
    """
    # Cabeçalho do programa
    print("🍔 Bem-vindo ao Chatbot da Hamburgueria Z!")
    
    # Define o contexto que o chatbot deve seguir
    contexto = """Você é um atendente virtual de uma hamburgueria que faz delivery.
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
    3) Confirmar o pedido e informar que foi colocado na fila de preparo
    4) Perguntar a forma de pagamento, informando que aceitamos APENAS cartão (crédito/débito) ou PIX. 
       NÃO aceitamos dinheiro vivo/em espécie.
    5) Caso o cliente demore em decidir, na última mensagem sempre pergunte a forma de pagamento (cartão ou PIX) 
       caso ele já tenha escolhido algum item.
    
    É importante calcular e informar o valor total do pedido antes de perguntar a forma de pagamento.
    
    Limite-se APENAS a esse contexto e a essas 3 interações. Não ofereça outros produtos ou serviços.
    Seja educado e cordial, mas direto e objetivo nas respostas."""
    
    # Instruções para o usuário
    print("Digite 'sair' para encerrar ou 'limpar' para iniciar uma nova conversa.")
    
    # Listas para armazenar o histórico da conversa
    perguntas = []
    respostas = []

    ###########################################
    # BLOCO DE APRESENTAÇÃO DA MENSAGEM INICIAL
    ###########################################
    
    # Apresenta a mensagem de boas-vindas concisa no início da conversa
    print(f"\n🍔 Atendente: {MENSAGEM_BOAS_VINDAS}")
    
    ###########################################
    # BLOCO DE LOOP PRINCIPAL DE INTERAÇÃO
    ###########################################
    
    # Loop para processar as perguntas do usuário
    for i in range(QTD_PERGUNTAS):
        # Obtém a entrada do usuário
        pergunta = input(f"\nVocê: ")
        
        # Verifica se o usuário deseja sair
        if pergunta.lower() == 'sair':
            print("Encerrando o chatbot. Até logo!")
            return
            
        # Verifica se o usuário deseja limpar a conversa
        elif pergunta.lower() == 'limpar':
            perguntas = []
            respostas = []
            print("Histórico de conversa limpo. Vamos começar um novo pedido!")
            print(f"\n🍔 Atendente: {MENSAGEM_BOAS_VINDAS}")
            continue
            
        # Verifica se o usuário está pedindo o cardápio
        elif usuario_pediu_cardapio(pergunta):
            print(f"\n🍔 Atendente: {CARDAPIO}")
            # IMPORTANTE: Quando o usuário solicita o cardápio, essa interação NÃO é enviada para a OpenAI.
            # O sistema usa 'continue' para pular o resto do loop, economizando tokens da API.
            continue  # Não conta como uma das perguntas principais
        
        # Armazena a pergunta atual
        perguntas.append(pergunta)
        
        # Obtém a resposta do modelo de IA
        resposta = obter_resposta(pergunta, contexto, MODEL)
        
        # Armazena a resposta atual
        respostas.append(resposta)
        
        # Exibe a resposta para o usuário
        print(f"\n🍔 Atendente: {resposta}")
    
    ###########################################
    # BLOCO DE RESUMO FINAL DO PEDIDO
    ###########################################
    
    # Gera um resumo formatado da conversa
    print("\n🧾 RESUMO DO SEU PEDIDO:")
    
    # Tenta gerar um resumo estruturado do pedido
    print("\nProcessando detalhes do pedido...")
    resumo_estruturado = gerar_resumo_pedido(perguntas, respostas)
    print(f"\n📋 Detalhes do pedido:\n{resumo_estruturado}")
    
    # Mostra cada interação da conversa no resumo
    print("\n💬 Histórico da conversa:")
    for i in range(len(perguntas)):
        print(f"\nVocê: {perguntas[i]}")
        print(f"Atendente: {respostas[i]}")
        
    print("\nObrigado por escolher nossa hamburgueria! Seu pedido está sendo preparado e será entregue em breve.")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()  # Executa a função principal
