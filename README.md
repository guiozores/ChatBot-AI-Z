# ChatBot-AI

Um chatbot simples que utiliza a API da OpenAI com o modelo GPT-4o-mini para manter conversas baseadas em um papel e contexto específicos.

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
   pip install -r requirements.txt
   ```
5. Configure sua chave API da OpenAI no arquivo `.env`

## Uso - Chatbot de Pizzaria Napolitana

Execute o script principal:

```
python chatbot.py
```

Siga as instruções para definir:

- O papel do chatbot (ex: pizzaiolo, atendente)
- O contexto em que o chatbot deve operar

Comandos especiais durante a conversa:

- `limpar`: Inicia uma nova conversa, mantendo o papel e contexto
- `sair`: Encerra o programa

## Uso - Especialista em Diabetes

O projeto também inclui um chatbot especializado em endocrinologia/diabetes que avalia o risco do usuário desenvolver diabetes:

```
python diabetes_specialist.py
```

### Recursos do Especialista em Diabetes

- Simula uma consulta com o Dr. IA, um médico endocrinologista especializado em diabetes
- Coleta informações relevantes como:
  - Exames de sangue (glicemia e hemoglobina glicada)
  - Peso e altura (para cálculo de IMC)
  - Histórico familiar de diabetes
  - Hábitos alimentares semanais (especialmente consumo de alimentos de risco)
- Permite três interações com o usuário
- Fornece uma avaliação de risco percentual ao final da consulta
- Baseia suas análises nas diretrizes da American Diabetes Association e da Sociedade Brasileira de Diabetes

### Como funciona a consulta

1. O Dr. IA (chatbot) fará perguntas específicas para coletar informações
2. Responda às perguntas fornecendo seus dados de saúde e hábitos alimentares
3. Após três interações, o médico fornecerá um resumo completo com:
   - Análise dos fatores de risco identificados
   - Estimativa percentual da chance de você ter ou desenvolver diabetes
   - Recomendações personalizadas baseadas nos seus dados

## Uso - Interface Web do Especialista em Diabetes

Para uma experiência mais amigável, você pode utilizar a interface web para interagir com o Dr. IA:

1. Certifique-se de que todas as dependências estão instaladas:

   ```
   pip install flask python-dotenv
   ```

2. Execute a aplicação Flask:

   ```
   python app.py
   ```

3. Abra seu navegador e acesse:
   ```
   http://127.0.0.1:5000
   ```

### Recursos da Interface Web

- Interface moderna e intuitiva para a consulta virtual
- Indicador visual de quando o Dr. IA está digitando
- Contador de respostas mostrando o progresso da consulta
- Formatação clara das respostas com títulos e destaques
- Destaque especial para o resumo final da consulta
- Botão para iniciar uma nova consulta a qualquer momento

A versão web oferece a mesma análise médica profissional da versão de terminal, mas com uma experiência de usuário aprimorada e melhor apresentação visual das informações.
