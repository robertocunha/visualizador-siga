
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

    const detalhes = document.createElement('details');

    const resumo = document.createElement('summary');
    resumo.textContent = biblioteca.NOME;

    detalhes.appendChild(resumo);

    adicionarCampo(detalhes, 'Endereço', biblioteca.ENDERECO);
    adicionarCampo(detalhes, 'Bairro', biblioteca.BAIRRO);
    adicionarCampo(detalhes, 'Funcionamento', biblioteca.FUNCIONAMENTO);
    adicionarCampo(detalhes, 'Telefone', biblioteca.TELEFONE);

    container.appendChild(detalhes);
  });

}

carregarBibliotecas();
