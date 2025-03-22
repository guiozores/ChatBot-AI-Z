"""
Utilitários para formatação de texto em HTML para o chatbot
"""
import json
import re

def formatar_cardapio_html():
    """
    Retorna o cardápio formatado em HTML com classes CSS
    """
    return """<div class="cardapio-container">
<h3>🍔 NOSSO CARDÁPIO</h3>

<div class="categoria">
<h4>💯 BURGERS</h4>
<div class="item">
  <div class="item-header">
    <span class="item-numero">1</span>
    <span class="item-nome">JOINT</span>
    <span class="item-preco">R$ 46,00</span>
  </div>
  <p class="item-descricao">Queijo americano, alface, tomate, cebola roxa, picles e molho especial</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">2</span>
    <span class="item-nome">BBQ</span>
    <span class="item-preco">R$ 52,00</span>
  </div>
  <p class="item-descricao">Queijo americano, bacon, cebola crispy, picles e molho barbecue</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">3</span>
    <span class="item-nome">JALAPEÑO</span>
    <span class="item-preco">R$ 49,00</span>
  </div>
  <p class="item-descricao">Gorgonzola, bacon, pimenta jalapeño, cebola roxa e sour cream</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">4</span>
    <span class="item-nome">LOUIS</span>
    <span class="item-preco">R$ 47,00</span>
  </div>
  <p class="item-descricao">Prensado com cebola, queijo americano e picles, no pão de forma</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">5</span>
    <span class="item-nome">MINETTA</span>
    <span class="item-preco">R$ 49,00</span>
  </div>
  <p class="item-descricao">Queijo cheddar inglês e cebola caramelizada</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">6</span>
    <span class="item-nome">J.R. BURGER</span>
    <span class="item-preco">R$ 44,00</span>
  </div>
  <p class="item-descricao">Double patty, queijo americano, cebola roxa, picles e molho especial</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">7</span>
    <span class="item-nome">LAMB</span>
    <span class="item-preco">R$ 49,00</span>
  </div>
  <p class="item-descricao">Burguer de cordeiro, queijo prato, cebola roxa, picles e maionese de cominho</p>
</div>
</div>

<div class="categoria">
<h4>🍟 SNACKS & APPETIZERS</h4>
<div class="item">
  <div class="item-header">
    <span class="item-numero">8</span>
    <span class="item-nome">Z DELI FRIES</span>
    <span class="item-preco">R$ 36,00</span>
  </div>
  <p class="item-descricao">Fritas com casca, alecrim fresco e Z Powder. Servidas com maionese da casa</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">9</span>
    <span class="item-nome">PASTRAMI FRIES</span>
    <span class="item-preco">R$ 51,00</span>
  </div>
  <p class="item-descricao">Fritas com casca, pastrami desfiado, queijo fundido, sour cream e cebolinha</p>
</div>
</div>

<div class="categoria">
<h4>🥤 BEVERAGES</h4>
<div class="item">
  <div class="item-header">
    <span class="item-numero">10</span>
    <span class="item-nome">ÁGUA [350ml]</span>
    <span class="item-preco">R$ 6,00</span>
  </div>
  <p class="item-descricao">Com ou sem gás</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">11</span>
    <span class="item-nome">COCA-COLA [250ml]</span>
    <span class="item-preco">R$ 7,00</span>
  </div>
  <p class="item-descricao">Em vidro, normal ou sem açúcar</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">12</span>
    <span class="item-nome">GUARANÁ ANTÁRTICA [350ml]</span>
    <span class="item-preco">R$ 7,00</span>
  </div>
  <p class="item-descricao">Normal ou sem açúcar</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">13</span>
    <span class="item-nome">TÔNICA [350ml]</span>
    <span class="item-preco">R$ 7,00</span>
  </div>
  <p class="item-descricao">Normal ou light</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">14</span>
    <span class="item-nome">SCHWEPPES CITRUS [350ml]</span>
    <span class="item-preco">R$ 7,00</span>
  </div>
  <p class="item-descricao">Normal ou leve em açúcares</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">15</span>
    <span class="item-nome">ÇÃ CIDER [300ml]</span>
    <span class="item-preco">R$ 19,00</span>
  </div>
  <p class="item-descricao">Sidra de maçã, leve e seca</p>
</div>

<div class="item">
  <div class="item-header">
    <span class="item-numero">16</span>
    <span class="item-nome">HEINEKEN [330ml]</span>
    <span class="item-preco">R$ 17,00</span>
  </div>
  <p class="item-descricao">Normal ou zero álcool</p>
</div>
</div>

<p class="cardapio-footer">Por favor, me diga quais itens você gostaria de pedir. Aceitamos apenas pagamento via cartão (crédito/débito) ou PIX.</p>
</div>"""

def formatar_pedido_atual_html(itens, valor_total=None):
    """
    Formata o pedido atual em HTML no mesmo estilo do cardápio
    
    Parâmetros:
        itens: lista de dicionários com 'nome', 'quantidade' e 'preco' unitário
        valor_total: valor total do pedido (opcional)
    """
    html = """<div class="cardapio-container">
<h3>🛒 SEU PEDIDO ATUAL</h3>

<div class="categoria">
<h4>📋 ITENS SELECIONADOS</h4>
"""
    # Adicionar cada item do pedido
    for item in itens:
        nome = item.get('nome', '')
        quantidade = item.get('quantidade', 1)
        preco_unitario = item.get('preco', 0)
        preco_total = quantidade * preco_unitario
        
        html += f"""<div class="item">
  <div class="item-header">
    <span class="item-numero">{quantidade}x</span>
    <span class="item-nome">{nome}</span>
    <span class="item-preco">R$ {preco_total:.2f}</span>
  </div>
</div>
"""
    
    # Se temos um valor total, adicionar seção de total
    if valor_total:
        html += f"""</div>
<div class="categoria">
<h4>💰 TOTAL</h4>
<div class="item">
  <div class="item-header">
    <span class="item-nome">Valor Total</span>
    <span class="item-preco">R$ {valor_total:.2f}</span>
  </div>
</div>
"""

    html += """</div>
<p class="cardapio-footer">Deseja adicionar mais algum item? Digite "cardápio" para ver todas as opções.</p>
</div>"""
    
    return html

def formatar_resumo_html(resumo_json_str):
    """
    Formata o resumo do pedido em HTML usando o mesmo estilo do cardápio
    """
    try:
        # Remover backticks e marcadores de código se presentes
        resumo_json_str = re.sub(r'```(json)?|```', '', resumo_json_str).strip()
        resumo = json.loads(resumo_json_str)
        
        html = """<div class="cardapio-container">
<h3>📋 RESUMO DO PEDIDO</h3>

<div class="categoria">
<h4>📦 ITENS</h4>
"""
        for item in resumo.get('itens', []):
            nome = item.get('nome', '')
            quantidade = item.get('quantidade', 1)
            preco_unitario = item.get('preco', 0)
            preco_total = quantidade * preco_unitario
            
            html += f"""<div class="item">
  <div class="item-header">
    <span class="item-numero">{quantidade}x</span>
    <span class="item-nome">{nome}</span>
    <span class="item-preco">R$ {preco_total:.2f}</span>
  </div>
</div>
"""
        
        valor_total = resumo.get('valor_total', 0)
        html += f"""</div>
<div class="categoria">
<h4>💰 TOTAL</h4>
<div class="item">
  <div class="item-header">
    <span class="item-nome">Valor Total</span>
    <span class="item-preco">R$ {valor_total:.2f}</span>
  </div>
</div>
</div>
<p class="cardapio-footer">Obrigado por seu pedido! Em breve entraremos em contato para confirmar.</p>
</div>"""
        
        return html
    except (json.JSONDecodeError, TypeError) as e:
        return f"<p class='error'>Erro ao formatar resumo: {str(e)}</p>"