    // Função para limpar spinner, barra de progresso e resultado
function limparInterface() {
  document.getElementById('loadingSpinner').style.display = 'none';
  document.getElementById('progressBar').style.display = 'none';
  document.getElementById('result').innerHTML = '';
}

// Função para verificar se há entrada válida
function verificarEntrada() {
  const texto = document.getElementById('emailText').value.trim();
  const arquivo = document.getElementById('emailFile').files.length > 0;
  const botaoProcessar = document.getElementById('submitBtn');
  botaoProcessar.disabled = !(texto || arquivo);
}

// Evento de envio do formulário
document.getElementById('emailForm').onsubmit = async function (e) {
  e.preventDefault();

  const botaoProcessar = document.getElementById('submitBtn');
  botaoProcessar.disabled = true;

  document.getElementById('loadingSpinner').style.display = 'block';
  document.getElementById('progressBar').style.display = 'block';

  const formData = new FormData(this);

  try {
    const response = await fetch('/process', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    limparInterface();
    botaoProcessar.disabled = false;

    const corBadge =
      data.categoria.trim().toLowerCase() === 'improdutivo'
        ? 'bg-danger'
        : 'bg-info';

    document.getElementById('result').innerHTML = `
      <div class="card border-info shadow-sm fade show">
        <div class="card-body">
          <h5>Categoria: <span class="badge ${corBadge}">${data.categoria}</span></h5>
          <p><strong>Resposta sugerida:</strong> ${data.resposta}</p>
        </div>
      </div>
    `;
  } catch (error) {
    limparInterface();
    botaoProcessar.disabled = false;

    document.getElementById('result').innerHTML = `
      <div class="alert alert-danger" role="alert">
        Ocorreu um erro ao processar o email. Tente novamente.
      </div>
    `;
  }
};

// Evento ao clicar no campo de arquivo
document.getElementById('emailFile').addEventListener('click', () => {
  document.getElementById('emailText').value = '';
  document.getElementById('emailFile').value = '';
  limparInterface();
  verificarEntrada();
});

// Evento ao digitar no campo de texto
document.getElementById('emailText').addEventListener('input', () => {
  document.getElementById('emailFile').value = '';
  limparInterface();
  verificarEntrada();
});

// Evento ao selecionar um novo arquivo
document.getElementById('emailFile').addEventListener('change', verificarEntrada);
