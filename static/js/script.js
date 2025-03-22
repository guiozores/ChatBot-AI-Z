document.addEventListener("DOMContentLoaded", function () {
  // Elementos do DOM
  const chatMessages = document.getElementById("chat-messages");
  const messageForm = document.getElementById("message-form");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const restartButton = document.getElementById("restart-button");
  const resumoContainer = document.getElementById("resumo-container");
  const resumoConteudo = document.getElementById("resumo-conteudo");
  const historicoConversa = document.getElementById("historico-conversa");
  const perguntaAtual = document.getElementById("pergunta-atual");
  const totalPerguntas = document.getElementById("total-perguntas");

  // Templates
  const userMessageTemplate = document.getElementById("user-message-template");
  const botMessageTemplate = document.getElementById("bot-message-template");
  const loadingTemplate = document.getElementById("loading-template");

  // Variáveis de estado
  let conversa = [];
  let contadorPerguntas = 0;
  const limitePerguntas = 3;
  let mostrandoResumo = false;

  // Atualizar o contador no início
  perguntaAtual.textContent = contadorPerguntas;
  totalPerguntas.textContent = limitePerguntas;

  // Função para mostrar mensagem do usuário
  function mostrarMensagemUsuario(mensagem) {
    const template = userMessageTemplate.content.cloneNode(true);
    template.querySelector("p").textContent = mensagem;
    chatMessages.appendChild(template);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Função para mostrar mensagem do bot
  function mostrarMensagemBot(mensagem, isHTML = false) {
    const template = botMessageTemplate.content.cloneNode(true);
    if (isHTML) {
      template.querySelector(".message-content").innerHTML = mensagem;
    } else {
      template.querySelector("p").textContent = mensagem;
    }
    chatMessages.appendChild(template);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return template;
  }

  // Função para mostrar o indicador de carregamento
  function mostrarCarregando() {
    const loadingElement = loadingTemplate.content.cloneNode(true);
    chatMessages.appendChild(loadingElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return chatMessages.lastElementChild;
  }

  // Função para enviar mensagem ao servidor
  async function enviarMensagem(mensagem) {
    // Mostrar a mensagem do usuário na interface
    mostrarMensagemUsuario(mensagem);

    // Mostrar indicador de carregamento
    const loadingElement = mostrarCarregando();

    try {
      // Enviar a mensagem para o servidor
      const response = await fetch("/enviar_mensagem", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          mensagem: mensagem,
          conversa: conversa,
          qtd_perguntas: contadorPerguntas,
        }),
      });

      // Processar a resposta
      const data = await response.json();

      // Remover o indicador de carregamento
      chatMessages.removeChild(loadingElement);

      // Atualizar contador apenas se não for um pedido de cardápio
      if (!data.e_cardapio) {
        contadorPerguntas = data.contador;
        perguntaAtual.textContent = contadorPerguntas;

        // Adicionar à lista de conversa
        conversa.push({
          pergunta: mensagem,
          resposta: data.resposta,
        });
      }

      // Mostrar a resposta do bot
      mostrarMensagemBot(data.resposta, data.e_cardapio);

      // Verificar se chegamos ao limite de perguntas
      if (contadorPerguntas >= limitePerguntas && !mostrandoResumo) {
        mostrarResumo();
        mostrandoResumo = true;
      }
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
      // Remover o indicador de carregamento
      chatMessages.removeChild(loadingElement);
      // Mostrar mensagem de erro
      mostrarMensagemBot(
        "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
      );
    }
  }

  // Função para mostrar o resumo do pedido
  async function mostrarResumo() {
    if (conversa.length === 0) return;

    try {
      // Mostrar mensagem de carregamento
      mostrarMensagemBot("Processando seu pedido... aguarde um momento.");

      const response = await fetch("/gerar_resumo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ conversa: conversa }),
      });

      const data = await response.json();

      // Preencher o conteúdo do resumo
      resumoConteudo.innerHTML = data.resumo_html;
      historicoConversa.innerHTML = data.historico_html;

      // Mostrar o container de resumo
      resumoContainer.style.display = "block";

      // Rolar para o resumo
      setTimeout(() => {
        resumoContainer.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (error) {
      console.error("Erro ao gerar resumo:", error);
      mostrarMensagemBot(
        "Não foi possível gerar o resumo do pedido. Por favor, tente novamente."
      );
    }
  }

  // Evento para envio do formulário
  messageForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const mensagem = userInput.value.trim();
    if (!mensagem) return;

    // Limpar o campo de entrada
    userInput.value = "";

    // Enviar a mensagem
    enviarMensagem(mensagem);
  });

  // Evento para o botão de reiniciar conversa
  restartButton.addEventListener("click", function () {
    // Limpar o histórico de conversa
    conversa = [];
    contadorPerguntas = 0;

    // Atualizar o contador
    perguntaAtual.textContent = contadorPerguntas;

    // Limpar as mensagens
    while (chatMessages.firstChild) {
      if (
        chatMessages.firstChild.classList.contains("message") &&
        chatMessages.firstChild.classList.contains("bot") &&
        !chatMessages.childElementCount === 1
      ) {
        break;
      }
      chatMessages.removeChild(chatMessages.firstChild);
    }

    // Esconder o resumo
    resumoContainer.style.display = "none";
    mostrandoResumo = false;

    // Mostrar mensagem inicial
    mostrarMensagemBot(
      'Olá! Bem-vindo à Hamburgueria Z! Estou aqui para ajudar com seu pedido. Digite "cardápio" se quiser ver as nossas opções. Aceitamos apenas pagamento via cartão (crédito/débito) ou PIX.'
    );
  });

  // Focar no campo de entrada ao carregar a página
  userInput.focus();
});
