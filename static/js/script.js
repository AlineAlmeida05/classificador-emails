    document.getElementById('emailForm').onsubmit = async function(e) {
      e.preventDefault();

      // Mostrar spinner e barra de progresso
      document.getElementById('loadingSpinner').style.display = 'block';
      document.getElementById('progressBar').style.display = 'block';

      const formData = new FormData(this);
      try {
        const response = await fetch('/process', { method: 'POST', body: formData });
        const data = await response.json();

        // Esconder spinner e barra
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('progressBar').style.display = 'none';

        // Mostrar resultado com fade
        document.getElementById('result').innerHTML = `
          <div class="card border-info shadow-sm fade show">
            <div class="card-body">
              <h5>Categoria: <span class="badge ${data.categoria.trim().toLowerCase() === 'improdutivo' ? 'bg-danger' : 'bg-info'}">${data.categoria}</span></h5>
              <p><strong>Resposta sugerida:</strong> ${data.resposta}</p>
            </div>
          </div>
        `;
      } catch (error) {
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('progressBar').style.display = 'none';
        document.getElementById('result').innerHTML = `
          <div class="alert alert-danger" role="alert">
            Ocorreu um erro ao processar o email. Tente novamente.
          </div>
        `;
      }
    };
    document.getElementById('emailFile').addEventListener('click', () => {
  // Limpa o campo de texto
  document.getElementById('emailText').value = '';

  // Limpa o campo de arquivo
  document.getElementById('emailFile').value = '';

  // Limpa o resultado anterior
  document.getElementById('result').innerHTML = '';

  // Esconde spinner e barra de progresso
  document.getElementById('loadingSpinner').style.display = 'none';
  document.getElementById('progressBar').style.display = 'none';
});
document.getElementById('emailText').addEventListener('input', () => {
  // Limpa o campo de arquivo
  document.getElementById('emailFile').value = '';

  // Limpa o resultado anterior
  document.getElementById('result').innerHTML = '';

  // Esconde spinner e barra de progresso
  document.getElementById('loadingSpinner').style.display = 'none';
  document.getElementById('progressBar').style.display = 'none';
});
function verificarEntrada() {
  const texto = document.getElementById('emailText').value.trim();
  const arquivo = document.getElementById('emailFile').files.length > 0;
  const botao = document.getElementById('submitBtn');

  if (texto || arquivo) {
    botao.disabled = false;
  } else {
    botao.disabled = true;
  }
}

// Verifica ao digitar no campo de texto
document.getElementById('emailText').addEventListener('input', () => {
  // Limpa tudo
  document.getElementById('emailFile').value = '';
  document.getElementById('result').innerHTML = '';
  document.getElementById('loadingSpinner').style.display = 'none';
  document.getElementById('progressBar').style.display = 'none';

  verificarEntrada();
});

// Verifica ao clicar no campo de arquivo
document.getElementById('emailFile').addEventListener('click', () => {
  document.getElementById('emailText').value = '';
  document.getElementById('result').innerHTML = '';
  document.getElementById('loadingSpinner').style.display = 'none';
  document.getElementById('progressBar').style.display = 'none';
  verificarEntrada();
});

// Verifica ao selecionar um novo arquivo
document.getElementById('emailFile').addEventListener('change', verificarEntrada);