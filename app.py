from flask import Flask, render_template, request, jsonify  # Framework web pra criar o site e lidar com requisições
import openai  # Biblioteca da OpenAI pra falar com a IA
import os  # Pra acessar variáveis de ambiente
from dotenv import load_dotenv  # Pra carregar as variáveis do arquivo .env
from chatbot import obter_resposta, gerar_resumo_pedido, usuario_pediu_cardapio, CARDAPIO, MENSAGEM_BOAS_VINDAS, contexto_chatbot  # Importa funções do nosso arquivo chatbot.py
from utils.formatters import formatar_cardapio_html, formatar_resumo_html, formatar_boas_vindas_html  # Funções pra deixar o texto bonito em HTML

# Carrega as variáveis do arquivo .env (tipo a chave da API)
load_dotenv()

# Pega a chave da API que colocamos no arquivo .env
api_key = os.getenv("OPENAI_API_KEY")
# Configura a chave da API pra biblioteca openai usar nas chamadas
openai.api_key = api_key

# Define qual modelo da OpenAI vamos usar (esse é mais barato!)
MODEL = "gpt-4o-mini"

# Cria a aplicação Flask que vai rodar nosso site
app = Flask(__name__)
# Define uma chave secreta pra proteger a sessão (pega do .env ou usa uma padrão)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "chave_secreta_padrao")

# Define a rota principal do site (quando alguém acessa o endereço sem nada depois)
@app.route('/')
def index():  # Função que é executada quando alguém acessa a página inicial
    # Renderiza o arquivo HTML da página inicial, passando as mensagens de boas-vindas
    return render_template('index.html', mensagem_inicial_html=formatar_boas_vindas_html(), 
                          mensagem_inicial=MENSAGEM_BOAS_VINDAS)

# Define a rota que processa as mensagens enviadas pelo usuário via AJAX
@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():  # Função que recebe a mensagem do usuário e devolve a resposta do bot
    # Pega os dados enviados pelo JavaScript no formato JSON
    data = request.json
    mensagem_usuario = data.get('mensagem', '')  # Texto que o usuário digitou
    conversa_anterior = data.get('conversa', [])  # Lista com o histórico de conversa
    qtd_perguntas = data.get('qtd_perguntas', 0)  # Número de perguntas já feitas
    
    # Verifica se o usuário pediu pra ver o cardápio
    if usuario_pediu_cardapio(mensagem_usuario):
        # Se sim, retorna o cardápio formatado em HTML sem contar como pergunta
        return jsonify({
            'resposta': formatar_cardapio_html(),  # Formata o cardápio pra ficar bonito
            'e_cardapio': True,  # Flag pra dizer que é cardápio (não conta como pergunta)
            'contador': qtd_perguntas  # Mantém o contador igual (não incrementa)
        })
    
    # Obtém resposta da API da OpenAI usando nossa função do chatbot.py
    resposta = obter_resposta(mensagem_usuario, contexto_chatbot(), MODEL, conversa_anterior)
    
    # Adiciona a pergunta e resposta ao histórico
    conversa_anterior.append({
        'pergunta': mensagem_usuario,
        'resposta': resposta
    })
    
    # Aumenta o contador de perguntas em +1
    qtd_perguntas += 1
    
    # Retorna a resposta em formato JSON pro JavaScript processar
    return jsonify({
        'resposta': resposta,  # Texto da resposta da IA
        'e_cardapio': False,  # Não é cardápio
        'contador': qtd_perguntas  # Contador atualizado
    })

# Rota pra gerar o resumo final quando a conversa acabar
@app.route('/gerar_resumo', methods=['POST'])
def resumo_pedido():  # Função que processa todo o histórico e gera um resumo do pedido
    # Pega os dados enviados pelo JavaScript
    data = request.json
    conversa = data.get('conversa', [])  # Lista com todo o histórico de conversa
    
    # Verifica se tem algo no histórico
    if not conversa:
        return jsonify({'erro': 'Nenhuma conversa fornecida'})  # Retorna erro se estiver vazio
    
    # Separa as perguntas e respostas em listas separadas
    perguntas = [item['pergunta'] for item in conversa]  # Lista só com as perguntas
    respostas = [item['resposta'] for item in conversa]  # Lista só com as respostas
    
    # Chama nossa função do chatbot.py pra gerar o resumo em formato JSON
    resumo_json = gerar_resumo_pedido(perguntas, respostas)
    
    # Formata o resumo em HTML pra ficar bonito na página
    resumo_html = formatar_resumo_html(resumo_json)
    
    # Formata o histórico de conversa em HTML também
    historico_html = "<h4>💬 Histórico da conversa:</h4>"
    for i, item in enumerate(conversa):
        historico_html += f"""
        <div class="historico-item">
            <p><strong>Você:</strong> {item['pergunta']}</p>
            <p><strong>Atendente:</strong> {item['resposta']}</p>
        </div>
        """
    
    # Retorna o resumo e o histórico formatados em HTML pro JavaScript
    return jsonify({
        'resumo_html': resumo_html,  # Resumo bonito em HTML
        'historico_html': historico_html  # Histórico formatado em HTML
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
