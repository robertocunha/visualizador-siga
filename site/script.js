
function adicionarCampo(artigo, rotulo, valor) {
  if (valor === null || valor === undefined || valor.trim() === '') {
    return;
  }

  const paragrafo = document.createElement('p');
  const destaque = document.createElement('strong');

  destaque.textContent = `${rotulo}: `;
  paragrafo.appendChild(destaque);
  paragrafo.append(valor);

  artigo.appendChild(paragrafo);
}

async function carregarBibliotecas() {
  const resposta = await fetch('../dados/biblioteca_legivel.json');
  const dados = await resposta.json();

  const container = document.querySelector('#bibliotecas');

  container.innerHTML = '';

  dados.features.forEach(feature => {
    const biblioteca = feature.properties;

    const artigo = document.createElement('article');

    const titulo = document.createElement('h2');
    titulo.textContent = biblioteca.NOME;
    artigo.appendChild(titulo);

    adicionarCampo(artigo, 'Endereço', biblioteca.ENDERECO);
    adicionarCampo(artigo, 'Bairro', biblioteca.BAIRRO);
    adicionarCampo(artigo, 'Funcionamento', biblioteca.FUNCIONAMENTO);
    adicionarCampo(artigo, 'Telefone', biblioteca.TELEFONE);

    container.appendChild(artigo);
  });
}

carregarBibliotecas();
