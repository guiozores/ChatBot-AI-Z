from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from chatbot import obter_resposta, gerar_resumo_pedido, usuario_pediu_cardapio, CARDAPIO, MENSAGEM_BOAS_VINDAS, contexto_chatbot
from utils.formatters import formatar_cardapio_html, formatar_resumo_html, formatar_boas_vindas_html

# Carregar variáveis de ambiente
load_dotenv()

# Configurar API da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Definir o modelo a ser utilizado
MODEL = "gpt-4o-mini"

# Configurar a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "chave_secreta_padrao")

# Rota principal - renderiza a página inicial
@app.route('/')
def index():
    return render_template('index.html', mensagem_inicial_html=formatar_boas_vindas_html(), 
                          mensagem_inicial=MENSAGEM_BOAS_VINDAS)

# Rota para processar as mensagens do usuário
@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    # Obter dados da requisição
    data = request.json
    mensagem_usuario = data.get('mensagem', '')
    conversa_anterior = data.get('conversa', [])
    qtd_perguntas = data.get('qtd_perguntas', 0)
    
    # Verificar se o usuário pediu o cardápio
    if usuario_pediu_cardapio(mensagem_usuario):
        return jsonify({
            'resposta': formatar_cardapio_html(),
            'e_cardapio': True,
            'contador': qtd_perguntas  # Não incrementa o contador
        })
    
    # Obter resposta da API da OpenAI, passando o histórico de conversa
    resposta = obter_resposta(mensagem_usuario, contexto_chatbot(), MODEL, conversa_anterior)
    
    # Atualizar a conversa
    conversa_anterior.append({
        'pergunta': mensagem_usuario,
        'resposta': resposta
    })
    
    # Incrementar o contador de perguntas
    qtd_perguntas += 1
    
    return jsonify({
        'resposta': resposta,
        'e_cardapio': False,
        'contador': qtd_perguntas
    })

# Rota para gerar o resumo do pedido
@app.route('/gerar_resumo', methods=['POST'])
def resumo_pedido():
    data = request.json
    conversa = data.get('conversa', [])
    
    if not conversa:
        return jsonify({'erro': 'Nenhuma conversa fornecida'})
    
    # Extrair perguntas e respostas
    perguntas = [item['pergunta'] for item in conversa]
    respostas = [item['resposta'] for item in conversa]
    
    # Obter resumo estruturado
    resumo_json = gerar_resumo_pedido(perguntas, respostas)
    
    # Formatar o resumo em HTML
    resumo_html = formatar_resumo_html(resumo_json)
    
    # Formatar o histórico de conversa
    historico_html = "<h4>💬 Histórico da conversa:</h4>"
    for i, item in enumerate(conversa):
        historico_html += f"""
        <div class="historico-item">
            <p><strong>Você:</strong> {item['pergunta']}</p>
            <p><strong>Atendente:</strong> {item['resposta']}</p>
        </div>
        """
    
    return jsonify({
        'resumo_html': resumo_html,
        'historico_html': historico_html
    })

# Iniciar o servidor se este arquivo for executado diretamente
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
