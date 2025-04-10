import os, openai, json
from dotenv import load_dotenv

# Configuração inicial
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
QTD_PERGUNTAS = 3

# Mensagens e cardápio
MENSAGEM_BOAS_VINDAS = "Olá! Bem-vindo à Hamburgueria Z! Estou aqui para ajudar com seu pedido. Digite 'cardápio' para ver opções."
CARDAPIO = """Aqui está nosso cardápio:
BURGERS:
1) JOINT - R$ 46,00 - (Queijo americano, alface, tomate, cebola roxa, picles e molho especial)
2) BBQ - R$ 52,00 - (Queijo americano, bacon, cebola crispy, picles e molho barbecue)
3) JALAPEÑO - R$ 49,00 - (Gorgonzola, bacon, pimenta jalapeño, cebola roxa e sour cream)
4) LOUIS - R$ 47,00 - (Prensado com cebola, queijo americano e picles, no pão de forma)
5) MINETTA - R$ 49,00 - (Queijo cheddar inglês e cebola caramelizada)
6) J.R. BURGER - R$ 44,00 - (Double patty, queijo americano, cebola roxa, picles e molho especial)
7) LAMB - R$ 49,00 - (Burguer de cordeiro, queijo prato, cebola roxa, picles e maionese de cominho)
SNACKS:
8) Z DELI FRIES - R$ 36,00 - (Fritas com casca, alecrim fresco e Z Powder)
9) PASTRAMI FRIES - R$ 51,00 - (Fritas com casca, pastrami desfiado, queijo fundido)
BEVERAGES: [10] ÁGUA - R$6 | [11] COCA-COLA - R$7 | [12] GUARANÁ - R$7 | [13] TÔNICA - R$7 | [14] SCHWEPPES - R$7 | [15] CIDER - R$19 | [16] HEINEKEN - R$17"""  # Fim da variável do cardápio, tem todos os produtos e preços!!

# Funções do chatbot
def obter_resposta(pergunta, contexto, historico=None):  # Função pra falar com a IA - recebe pergunta do usuário, contexto e histórico anterior
    mensagens = [{"role": "system", "content": contexto}]  # Cria uma lista e põe o contexto como primeira mensagem de sistema pra IA saber o que fazer
    
    if historico:  # Se tiver histórico de conversa anterior (nas primeiras vezes não tem!)
        for i, msg in enumerate(historico):  # Vai passando por cada mensagem do histórico (loop)
            mensagens.append({"role": "user", "content": msg["pergunta"]})  # Coloca a pergunta do usuário na lista de mensagens
            mensagens.append({"role": "assistant", "content": msg["resposta"]})  # Coloca a resposta do bot na lista também
    
    mensagens.append({"role": "user", "content": pergunta})  # Adiciona a pergunta atual no final da lista de mensagens
    
    # Faz a chamada à API
    response = openai.ChatCompletion.create(model=MODEL, messages=mensagens, max_tokens=500, temperature=0.7)
    
    return response['choices'][0]['message']['content']

def contexto_chatbot(ultima_pergunta=False):  # Função que cria o prompt pro bot - se for última pergunta muda o comportamento
    contexto = f"""Você é um atendente virtual de hamburgueria. Seu objetivo é: 1) Receber o pedido, 2) Perguntar forma de entrega e endereço, 3) Confirmar forma de pagamento (APENAS cartão ou PIX). Calcule o valor total antes de perguntar pagamento. Seja objetivo e direto.
    
Utilize APENAS os produtos e preços do cardápio abaixo para cálculos:

{CARDAPIO}

Calcule o valor total somando os preços dos itens escolhidos e informe ao cliente o valor a ser pago."""  # Texto base com instruções pro bot incluindo o cardápio
    if ultima_pergunta:  # Se for a última das 3 perguntas permitidas (true/false)
        contexto += " IMPORTANTE: Esta é a última pergunta permitida. Você DEVE perguntar sobre forma de pagamento, confirmar endereço e fazer um resumo do pedido com valor total."  # Adiciona instrução especial pra última pergunta
    return contexto  # Devolve o texto completo com as instruções pro bot

def gerar_e_formatar_resumo(historico):  # Função que faz o resumo final do pedido - recebe todo histórico de conversa
    try:  # Tenta fazer tudo dentro desse bloco, se der erro vai pro "except"
        prompt = "Baseado na conversa abaixo, extraia: 1) itens pedidos e quantidades, 2) valor total, 3) forma de pagamento, 4) entrega/endereço, 5) nome do cliente. Responda APENAS em JSON válido: {'itens':[{'nome':str,'quantidade':int,'preco':float}],'valor_total':float,'forma_pagamento':str,'entrega':{'tipo':str,'endereco':str},'cliente':str}"  # Instrução pro bot extrair dados estruturados
        for msg in historico:  # Loop passando por todas as mensagens trocadas
            prompt += f"\nCliente: {msg['pergunta']}\nAtendente: {msg['resposta']}\n"  # Vai montando o texto da conversa pra mandar pra IA analisar
        
        resumo_json = obter_resposta(prompt, "Você é um assistente técnico que extrai dados de conversas e retorna apenas JSON válido.")  # Pede pra IA extrair os dados em formato JSON
        if "```json" in resumo_json:  # Se a IA colocou o JSON dentro de blocos de código markdown
            resumo_json = resumo_json.split("```json")[1].split("```")[0].strip()  # Tira os delimitadores markdown ```json e ``` do começo e fim
        
        resumo = json.loads(resumo_json)  # Converte a string JSON em um dicionário Python pra poder acessar os dados
        texto = "📋 RESUMO DO PEDIDO\n" + "="*30 + "\n\n"  # Começa a formatar o texto bonito do resumo com emojis e separadores
        
        # Itens pedidos
        texto += "🍔 ITENS:\n"  # Titulo da seção de itens com emoji de hamburguer
        if "itens" in resumo and resumo["itens"]:  # Verifica se o JSON tem a chave "itens" e se não está vazia
            for item in resumo["itens"]:  # Loop pelos itens pedidos
                texto += f"  • {item.get('quantidade', 1)}x {item.get('nome', 'Item')} - R$ {item.get('preco', 0)}\n"  # Adiciona cada item no texto formatado
        
        # Outras informações
        texto += f"\n💰 TOTAL: R$ {resumo.get('valor_total', 'Não calculado')}\n"  # Adiciona o total calculado
        texto += f"💳 PAGAMENTO: {resumo.get('forma_pagamento', 'Não informado')}\n"  # Adiciona a forma de pagamento
        
        if "entrega" in resumo and resumo["entrega"]:  # Verifica se tem informações de entrega
            texto += f"🚚 ENTREGA: {resumo['entrega'].get('tipo', 'Não especificado')}\n"  # Adiciona tipo de entrega
            texto += f"📍 ENDEREÇO: {resumo['entrega'].get('endereco', 'Não especificado')}\n"  # Adiciona endereço
        
        texto += f"👤 CLIENTE: {resumo.get('cliente', 'Não informado')}\n\n"  # Adiciona nome do cliente
        
        # Histórico de conversa
        texto += "💬 HISTÓRICO:\n" + "="*30 + "\n"  # Titulo da seção de histórico
        for i, msg in enumerate(historico, 1):  # Loop enumerado pelo histórico
            texto += f"{i}) Você: {msg['pergunta']}\n   Bot: {msg['resposta']}\n\n"  # Adiciona cada troca de mensagens no texto
        
        return texto  # Devolve o texto formatado
    except Exception as e:  # Se der erro
        return f"Erro ao processar resumo: {str(e)}\n\nHistórico da conversa:\n" + "\n".join([f"Você: {m['pergunta']}\nBot: {m['resposta']}" for m in historico])  # Devolve erro e histórico bruto

def main():  # Função principal que faz tudo funcionar junto!!
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela do terminal pra ficar bonito (funciona no Windows e Linux)
    print("\n🍔 Chatbot da Hamburgueria Z - (Digite 'sair' ou 'limpar')")  # Mostra o título do programa com emoji de hambúrguer
    print(f"\n🤖 Bot: {MENSAGEM_BOAS_VINDAS}")  # Mostra a mensagem de boas vindas que definimos lá no começo
    
    historico = []  # Cria uma lista vazia pra guardar todas as perguntas e respostas (começa sem nada)
    contador = 0  # Contador pra saber quantas perguntas já foram feitas (começa com zero)
    
    while contador < QTD_PERGUNTAS:  # Loop que vai rodar até atingir o limite de perguntas (definido lá em cima como 3)
        pergunta_atual = contador + 1  # Calcula número da pergunta atual (para exibição começando em 1)
        print(f"\n[{pergunta_atual}/{QTD_PERGUNTAS}] ", end="")  # Mostra o contador de perguntas tipo [1/3], [2/3], etc
        pergunta = input("Você: ")  # Pega o que o usuário digitar e guarda na variável "pergunta"
        
        if pergunta.lower() == 'sair':  # Se o usuário digitar "sair" (não importa se maiúsculo/minúsculo)
            print("Até logo!")  # Mensagem de despedida
            return  # Sai da função main e termina o programa!
        elif pergunta.lower() == 'limpar':  # Se o usuário digitar "limpar"
            historico = []  # Apaga todo o histórico de conversa
            contador = 0  # Reseta o contador de perguntas pra zero
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela do terminal de novo
            print("\n🤖 Bot: Conversa reiniciada. " + MENSAGEM_BOAS_VINDAS)  # Mostra que reiniciou e a mensagem de boas vindas
            continue  # Volta pro começo do loop sem executar o resto do código
        elif any(palavra in pergunta.lower() for palavra in ["cardapio", "cardápio", "menu"]):  # Verifica se perguntou pelo cardápio
            print(f"\n🤖 Bot: {CARDAPIO}")  # Mostra o cardápio que definimos lá no início
            continue  # Volta pro começo do loop (importante: não conta como pergunta!)
        
        ultima_pergunta = contador == QTD_PERGUNTAS - 1  # Checa se essa é a última pergunta permitida (true/false)
        contador += 1  # Aumenta o contador de perguntas em +1 (só conta perguntas normais, não cardápio)
        
        try:  # Tenta fazer a parte que pode dar erro (conexão com API)
            resposta = obter_resposta(pergunta, contexto_chatbot(ultima_pergunta), historico)  # Chama a IA e guarda a resposta
            historico.append({"pergunta": pergunta, "resposta": resposta})  # Adiciona a pergunta e resposta no histórico
            print(f"\n🤖 Bot: {resposta}")  # Mostra a resposta da IA pro usuário
        except Exception as e:  # Se der algum erro
            print(f"\n❌ Erro: {str(e)}")  # Mostra a mensagem de erro pro usuário
            contador -= 1  # Diminui o contador pra não contar essa tentativa com erro
    
    if historico:  # Depois que acabar as 3 perguntas, se tiver algo no histórico
        print("\n" + "="*30 + "\n🧾 FINALIZANDO PEDIDO...\n" + "="*30)  # Mostra um separador bonito
        print(gerar_e_formatar_resumo(historico))  # Chama a função que gera o resumo e mostra pro usuário

if __name__ == "__main__":  # Verifica se o arquivo está sendo executado diretamente (não importado)
    main()  # Chama a função principal quando executamos o script
