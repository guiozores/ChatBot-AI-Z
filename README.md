# ChatBot-AI-Z 🍔

Um chatbot de atendimento para hamburgueria usando a API da OpenAI.

## Pré-requisitos

- Python 3.8 ou superior
- Uma conta na OpenAI com chave de API válida

## Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/ChatBot-AI-Z.git
cd ChatBot-AI-Z
```

2. Crie um ambiente virtual (recomendado):

```bash
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` na raiz do projeto com sua chave da API da OpenAI:

```
OPENAI_API_KEY=sua_chave_api_aqui
```

## Como Usar

1. Ative o ambiente virtual (caso não esteja ativado):

```bash
# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

2. Execute o chatbot:

```bash
python chatbot.py
```

3. Interaja com o chatbot:

- Digite "cardápio" para ver as opções disponíveis
- Digite "limpar" para começar uma nova conversa
- Digite "sair" para encerrar o programa

## Funcionalidades

- Mostra o cardápio quando solicitado
- Processa pedidos de hambúrgueres e bebidas
- Calcula o valor total do pedido
- Aceita pagamentos via cartão (crédito/débito) ou PIX
- Gera um resumo do pedido ao final da interação

## Observações

- O chatbot está limitado a 3 interações antes de mostrar o resumo do pedido
- O sistema utiliza o modelo GPT-4 da OpenAI
- É necessário ter uma chave de API válida da OpenAI para funcionar
