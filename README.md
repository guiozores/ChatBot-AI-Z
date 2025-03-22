# ChatBot-AI-Z

Um chatbot simples que utiliza a API da OpenAI com o modelo GPT-4o-mini para manter conversas como atendente virtual de uma hamburgueria.

## Configuração

1. Clone este repositório
2. Crie um ambiente virtual Python:
   ```
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências:
   ```
   pip install openai==0.28.1 python-dotenv
   ```
5. Configure sua chave API da OpenAI no arquivo `.env`:
   ```
   OPENAI_API_KEY=sua_chave_aqui
   ```

## Uso - Chatbot de Hamburgueria

Execute o script principal:

```
python chatbot.py
```

### Recursos do Chatbot

- Atendente virtual de uma hamburgueria que oferece:
  - Diversos tipos de hambúrgueres
  - Snacks e acompanhamentos
  - Bebidas
- Pode mostrar o cardápio completo quando solicitado
- Processa pedidos e formas de pagamento (cartão ou PIX)
- Gera um resumo estruturado do pedido ao final da interação

### Comandos especiais durante a conversa

- `cardápio`: Exibe o menu completo com produtos e preços
- `limpar`: Inicia uma nova conversa, mantendo o mesmo contexto
- `sair`: Encerra o programa
