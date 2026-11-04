# Visualizador SIGA

Projeto pessoal e experimental para explorar os dados públicos disponibilizados pelo [catálogo SIGA da Prefeitura de Santo André](https://siga.santoandre.sp.gov.br/Catalogo).

A ideia inicial é investigar maneiras de consultar e apresentar essas informações de forma mais acessível. O projeto ainda está em fase exploratória: funcionalidades, arquitetura e tecnologias da aplicação final não estão definidas.

Este repositório reúne, por enquanto, scripts auxiliares usados para obter e preparar dados do catálogo.

## Estrutura do projeto

- **`scripts/`** — programas usados para coletar e preparar os dados.
- **`dados/`** — arquivos produzidos pelos scripts. O conteúdo dessa pasta não é versionado.
- **`README.md`** — documentação e instruções do projeto.

## Scripts disponíveis

- **`scripts/baixar_siga.py`** — acessa o catálogo SIGA, seleciona a camada **Biblioteca** (identificada no catálogo pelo ID 90) e solicita o arquivo GeoJSON.
- **`scripts/formatar_biblioteca.py`** — decodifica e formata o arquivo obtido, além de tentar corrigir problemas comuns de codificação de caracteres.

O fluxo atual produz dois arquivos locais na pasta `dados/`:

- `biblioteca.json` — resposta original recebida do SIGA.
- `biblioteca_legivel.json` — versão decodificada e formatada.

Esses arquivos de dados não são versionados neste repositório.

## Requisitos

- Python 3
- Biblioteca Python [Requests](https://requests.readthedocs.io/)

## Como executar

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/robertocunha/visualizador-siga.git
cd visualizador-siga
```

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale a dependência:

```bash
python3 -m pip install requests
```

Execute primeiro o script de coleta e, em seguida, o de formatação:

```bash
python3 scripts/baixar_siga.py
python3 scripts/formatar_biblioteca.py
```

Ao final, os arquivos JSON serão criados na pasta `dados/`.

## Observações

- Os scripts localizam a pasta do projeto a partir de seus próprios caminhos. Assim, podem ser executados a partir de outros diretórios.
- O script de coleta reproduz o fluxo de requisições atualmente observado no catálogo SIGA. Alterações no site podem exigir ajustes no código.
- A camada Biblioteca é apenas o primeiro conjunto de dados investigado; não representa uma decisão definitiva sobre o escopo do projeto.
- Os arquivos JSON são ignorados pelo Git. Além de evitar versionar dados derivados, isso impede que informações de contato presentes nos registros sejam publicadas inadvertidamente.
- Este é um projeto independente, sem vínculo institucional com a Prefeitura de Santo André.

## Situação

Em desenvolvimento exploratório. As próximas etapas incluem compreender melhor a estrutura e a atualização dos dados e experimentar formas de apresentá-los em uma aplicação web.
