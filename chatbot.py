import os                  # Fornece funções para interagir com o sistema operacional, usado para acessar variáveis de ambiente
import openai              # Biblioteca oficial da OpenAI para comunicação com a API GPT
from dotenv import load_dotenv  # Permite carregar variáveis de ambiente de um arquivo .env

###########################################
# BLOCO DE CONFIGURAÇÃO INICIAL
# Este bloco configura os parâmetros iniciais do chatbot, incluindo
# autenticação com a API da OpenAI e definição de configurações básicas
###########################################

# Carregar variáveis de ambiente do arquivo .env
# O arquivo .env deve estar no mesmo diretório que este script e conter OPENAI_API_KEY=<sua_chave>
load_dotenv()

# Obter a chave da API da OpenAI da variável de ambiente
# Esta chave é necessária para autenticar solicitações à API da OpenAI
# e é obtida através do site https://platform.openai.com
api_key = os.getenv("OPENAI_API_KEY")  # Retorna None se a variável não existir

# Configurando a chave API globalmente para a biblioteca openai
# Esta configuração afeta todas as chamadas subsequentes à API
openai.api_key = api_key

# Definir o modelo a ser utilizado
# gpt-4o-mini é um modelo mais econômico que equilibra custo e desempenho
# Outros modelos possíveis: gpt-3.5-turbo, gpt-4, etc.
MODEL = "gpt-4o-mini"

# Quantidade de perguntas que o usuário poderá fazer antes de mostrar resumo
# Define quantas interações o usuário terá com o chatbot antes de ver o resumo do pedido
# Esse número pode ser ajustado conforme necessidade de uso
QTD_PERGUNTAS = 3

###########################################
# BLOCO DE DEFINIÇÃO DO CARDÁPIO
# Define os textos estáticos que serão apresentados ao usuário
# Estas constantes evitam repetição de texto no código
###########################################

# Texto do cardápio que será mostrado apenas quando solicitado
# O formato do cardápio é importante pois impacta como o modelo de IA
# entenderá e processará os pedidos posteriormente
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
# Esta mensagem é apresentada logo no início da execução do programa
# e também quando o usuário limpa a conversa
MENSAGEM_BOAS_VINDAS = """Olá! Bem-vindo à Hamburgueria Z! 

Estou aqui para ajudar com seu pedido. Digite "cardápio" se quiser ver as nossas opções.

Aceitamos apenas pagamento via cartão (crédito/débito) ou PIX."""

###########################################
# BLOCO DE FUNÇÃO DE COMUNICAÇÃO COM A API
# Este bloco contém a função responsável por enviar solicitações para a API
# da OpenAI e retornar as respostas geradas pelo modelo
###########################################

def obter_resposta(pergunta, contexto, modelo, historico=None):
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
    # Detalhamento dos parâmetros:
    # - pergunta: vem do input do usuário na função main()
    # - contexto: vem da função contexto_chatbot() que retorna instruções para o modelo
    # - modelo: vem da constante MODEL definida no início do arquivo
    # - historico: lista de dicionários com chaves 'pergunta' e 'resposta', gerada na função main()
    
    # Preparar as mensagens para a API
    # A mensagem segue o formato exigido pela API da OpenAI
    # com chaves 'role' e 'content'
    messages = []
    
    # Adicionar o contexto como mensagem de sistema apenas na primeira chamada
    # A mensagem de sistema (role: system) define o comportamento geral do assistente
    messages.append({"role": "system", "content": contexto})
    
    # Adicionar o histórico de mensagens se fornecido
    # O histórico mantém a conversa coerente permitindo que o modelo
    # tenha conhecimento das interações anteriores
    # Verifica se o parâmetro 'historico' está definido e não está vazio
    if historico:
        # Percorre a lista de mensagens existentes para manter o contexto da conversa
        for msg in historico:
            # Se houver registro de pergunta, adiciona ao histórico como mensagem do usuário
            if 'pergunta' in msg:
                messages.append({"role": "user", "content": msg['pergunta']})
            # Se houver registro de resposta, adiciona ao histórico como mensagem do assistente
            if 'resposta' in msg:
                messages.append({"role": "assistant", "content": msg['resposta']})
    
    # Adicionar a pergunta atual
    # Esta é a mensagem mais recente do usuário que será respondida pelo modelo
    messages.append({"role": "user", "content": pergunta})
    
    # Fazer a chamada para a API
    # Aqui acontece a comunicação HTTP com a API da OpenAI
    # Essa chamada consome tokens da conta e gera custos
    response = openai.ChatCompletion.create(
        model=modelo,           # Modelo de IA a ser usado (passado como parâmetro)
        messages=messages,      # Lista de mensagens incluindo contexto, histórico e pergunta atual
        max_tokens=500,         # Limita o tamanho da resposta (controla custos)
        temperature=0.7         # Controla a aleatoriedade da resposta (0=determinístico, 1=criativo)
    )
    # O retorno é um objeto JSON complexo, do qual extraímos apenas o conteúdo da mensagem
    return response['choices'][0]['message']['content']  # Extrai o texto da resposta que será exibido ao usuário

###########################################
# FUNÇÃO PARA VERIFICAR SE USUÁRIO PEDE CARDÁPIO
# Esta função analisa a entrada do usuário para determinar
# se ele está solicitando ver o cardápio
###########################################

def usuario_pediu_cardapio(mensagem):
    """
    Verifica se o usuário está solicitando o cardápio.
    
    Parâmetros:
        mensagem (str): Mensagem enviada pelo usuário
        
    Retorno:
        bool: True se o usuário pediu o cardápio, False caso contrário
    """
    # Detalhamento dos parâmetros:
    # - mensagem: vem diretamente do input do usuário na função main()
    # O retorno é usado para decidir se mostra o cardápio ou envia a mensagem para a API
    
    # Converter a mensagem para minúsculas para facilitar a comparação
    # Isso torna a detecção insensível a maiúsculas/minúsculas
    mensagem = mensagem.lower()
    
    # Lista de palavras-chave que podem indicar que o usuário quer ver o cardápio
    # Esta lista pode ser expandida para capturar mais variações de pedidos
    palavras_chave = ["cardapio", "cardápio", "menu", "opcoes", "opções", 
                     "opçoes", "lista", "catalogo", "catálogo", "produtos"]
    
    # Verificar se alguma das palavras-chave está na mensagem
    # Basta encontrar uma das palavras para confirmar o pedido de cardápio
    for palavra in palavras_chave:
        if palavra in mensagem:
            return True  # O usuário pediu o cardápio
    
    return False  # Nenhuma palavra-chave encontrada, o usuário não pediu o cardápio

###########################################
# FUNÇÃO PARA GERAR RESUMO ESTRUTURADO
# Esta função processa todo o histórico da conversa e extrai
# informações relevantes sobre o pedido
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
    # Detalhamento dos parâmetros:
    # - perguntas: lista de strings com todas as mensagens do usuário, coletadas na função main()
    # - respostas: lista de strings com todas as respostas do chatbot, também coletadas na função main()
    # O retorno é uma string em formato JSON com detalhes do pedido para exibição ao usuário
    
    # Criar um contexto para extrair informações do pedido
    # Este contexto é uma instrução específica para o modelo processar 
    # as conversas e extrair dados estruturados
    contexto_resumo = """Você é um assistente de processamento de texto especializado em extrair informações de pedidos de hambúrgueres.
    Com base nas conversas entre cliente e atendente, extraia as seguintes informações:
    1. Quais itens foram pedidos e suas quantidades
    2. O valor total do pedido (some os preços dos itens mencionados)
    3. A forma de pagamento escolhida
    4. A forma de entrega, se vai ser entrega ou retirada. E o nome do cliente.
    
    Retorne apenas um JSON com os campos: 'itens' (lista de objetos com 'nome', 'quantidade' e 'preco'), 'valor_total' (número) e 'forma_pagamento' (string).
    Se alguma informação não estiver disponível, use o valor null."""
    
    # Combinar as conversas em um formato que facilite a extração
    # Formata as mensagens como uma conversa entre cliente e atendente
    conversa = ""
    for i in range(len(perguntas)):
        conversa += f"Cliente: {perguntas[i]}\nAtendente: {respostas[i]}\n\n"
    
    # Obter um resumo estruturado via API
    # Usa a mesma função obter_resposta() com um contexto diferente
    # específico para a extração de informações
    try:
        resumo_estruturado = obter_resposta(conversa, contexto_resumo, MODEL)
        return resumo_estruturado  # Retorna o resumo formatado (JSON como string)
    except Exception as e:
        # Tratamento de erros para evitar que problemas na API interrompam o programa
        return f"Não foi possível gerar um resumo detalhado do pedido. Erro: {str(e)}"

# Função para retornar o contexto do chatbot
def contexto_chatbot():
    """
    Define o contexto e as instruções para o modelo de IA.
    
    Retorno:
        str: Uma string contendo todas as instruções e o contexto que o modelo deve seguir
    
    Esta função retorna um prompt de sistema detalhado que:
    1. Define o papel do chatbot como atendente de uma hamburgueria
    2. Lista todos os produtos disponíveis e seus preços
    3. Estabelece os objetivos e comportamentos esperados do chatbot
    4. Define limites para o que o chatbot deve e não deve fazer
    
    O contexto retornado por esta função é usado em todas as chamadas à API
    como a mensagem de sistema (role: system) que define o comportamento do chatbot.
    """
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
    5) Caso o cliente demore em decidir, na última mensagem sempre pergunte a forma de pagamento (cartão ou PIX) 
       caso ele já tenha escolhido algum item. E tambem confirmar o endereço e forma de entrega, caso ele ainda não tenha escolhido ou solicitado.
    6)Confirmar o pedido e informar que foi colocado na fila de preparo somente após o cliente confirmar
    
    É importante calcular e informar o valor total do pedido antes de perguntar a forma de pagamento.
    
    Limite-se APENAS a esse contexto e a essas 3 interações. Não ofereça outros produtos ou serviços.
    Seja educado e cordial, mas direto e objetivo nas respostas."""

###########################################
# BLOCO DA FUNÇÃO PRINCIPAL
# Este bloco contém a função principal que orquestra
# todo o fluxo de funcionamento do chatbot
###########################################

def main():
    """
    Função principal que controla o fluxo do chatbot da hamburgueria.
    Gerencia as interações, mostra o cardápio apenas quando solicitado e exibe o resumo do pedido.
    
    Esta função não recebe parâmetros e não retorna valores.
    Ela controla todo o fluxo de execução do programa, desde a apresentação
    inicial até a finalização com o resumo do pedido.
    
    O fluxo principal é:
    1. Apresentar a mensagem de boas-vindas
    2. Entrar em um loop de conversação por QTD_PERGUNTAS interações
    3. Processar comandos especiais (sair, limpar, cardápio)
    4. Armazenar o histórico de perguntas e respostas
    5. Gerar e apresentar um resumo do pedido
    """
    # Cabeçalho do programa
    # Primeira mensagem exibida quando o programa inicia
    print("🍔 Bem-vindo ao Chatbot da Hamburgueria Z!")
    
    # Instruções para o usuário
    # Informa os comandos especiais disponíveis
    print("Digite 'sair' para encerrar ou 'limpar' para iniciar uma nova conversa.")
    
    # Listas para armazenar o histórico da conversa
    # Estas listas são preenchidas durante a interação e usadas para:
    # 1. Manter contexto nas chamadas à API
    # 2. Gerar o resumo final do pedido
    perguntas = []  # Armazena as mensagens do usuário
    respostas = []  # Armazena as respostas do chatbot

    ###########################################
    # BLOCO DE APRESENTAÇÃO DA MENSAGEM INICIAL
    ###########################################
    
    # Apresenta a mensagem de boas-vindas concisa no início da conversa
    # Esta mensagem está definida na constante MENSAGEM_BOAS_VINDAS
    print(f"\n🍔 Atendente: {MENSAGEM_BOAS_VINDAS}")
    
    ###########################################
    # BLOCO DE LOOP PRINCIPAL DE INTERAÇÃO
    ###########################################
    
    # Loop para processar as perguntas do usuário
    # O número de iterações é definido pela constante QTD_PERGUNTAS
    for i in range(QTD_PERGUNTAS):
        # Obtém a entrada do usuário
        # A função input bloqueia a execução até que o usuário digite algo
        pergunta = input(f"\nVocê: ")
        
        # Verifica se o usuário deseja sair
        # Comando especial para encerrar o programa imediatamente
        if pergunta.lower() == 'sair':
            print("Encerrando o chatbot. Até logo!")
            return  # Encerra a função main() e consequentemente o programa
            
        # Verifica se o usuário deseja limpar a conversa
        # Comando especial para reiniciar o chatbot mantendo a sessão
        elif pergunta.lower() == 'limpar':
            perguntas = []  # Reseta o histórico de perguntas
            respostas = []  # Reseta o histórico de respostas
            print("Histórico de conversa limpo. Vamos começar um novo pedido!")
            print(f"\n🍔 Atendente: {MENSAGEM_BOAS_VINDAS}")
            continue  # Pula para a próxima iteração do loop
            
        # Verifica se o usuário está pedindo o cardápio
        # Usa a função usuario_pediu_cardapio() para detectar pedidos de cardápio
        elif usuario_pediu_cardapio(pergunta):
            print(f"\n🍔 Atendente: {CARDAPIO}")
            # IMPORTANTE: Quando o usuário solicita o cardápio, essa interação NÃO é enviada para a OpenAI.
            # O sistema usa 'continue' para pular o resto do loop, economizando tokens da API.
            continue  # Não conta como uma das perguntas principais
        
        # Armazena a pergunta atual
        # Adiciona a pergunta do usuário ao histórico para contexto e resumo
        perguntas.append(pergunta)
        
        # Obtém a resposta do modelo de IA
        # Chama a função obter_resposta() passando:
        # 1. A pergunta atual do usuário
        # 2. O contexto do chatbot (retornado por contexto_chatbot())
        # 3. O modelo de IA a ser usado (definido na constante MODEL)
        # 4. O histórico de mensagens convertido para o formato esperado
        resposta = obter_resposta(pergunta, contexto_chatbot(), MODEL, historico=[{'pergunta': p, 'resposta': r} for p, r in zip(perguntas, respostas)])
        
        # Armazena a resposta atual
        # Adiciona a resposta do chatbot ao histórico para contexto e resumo
        respostas.append(resposta)
        
        # Exibe a resposta para o usuário
        # Mostra na tela a resposta gerada pelo modelo de IA
        print(f"\n🍔 Atendente: {resposta}")
    
    ###########################################
    # BLOCO DE RESUMO FINAL DO PEDIDO
    # Este bloco é executado após completar QTD_PERGUNTAS interações
    # ou quando o usuário decide finalizar o pedido
    ###########################################
    
    # Gera um resumo formatado da conversa
    print("\n🧾 RESUMO DO SEU PEDIDO:")
    
    # Tenta gerar um resumo estruturado do pedido
    # Usa a função gerar_resumo_pedido() que processa todo o histórico
    print("\nProcessando detalhes do pedido...")
    resumo_estruturado = gerar_resumo_pedido(perguntas, respostas)
    print(f"\n📋 Detalhes do pedido:\n{resumo_estruturado}")
    
    # Mostra cada interação da conversa no resumo
    # Apresenta o histórico completo em formato de conversa
    print("\n💬 Histórico da conversa:")
    for i in range(len(perguntas)):
        print(f"\nVocê: {perguntas[i]}")
        print(f"Atendente: {respostas[i]}")
        
    # Mensagem final de agradecimento
    print("\nObrigado por escolher nossa hamburgueria! Seu pedido está sendo preparado e será entregue em breve.")

# Verifica se o script está sendo executado diretamente
# Esta verificação permite que o módulo seja importado sem executar main()
if __name__ == "__main__":
    main()  # Executa a função principal quando o script é rodado diretamente
