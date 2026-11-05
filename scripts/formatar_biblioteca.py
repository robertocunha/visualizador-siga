import json
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados"

origem = PASTA_DADOS / "biblioteca.json"
destino = PASTA_DADOS / "biblioteca_legivel.json"

# Primeira decodificação: remove a camada externa de JSON.
texto = origem.read_text(encoding="utf-8")
conteudo = json.loads(texto)

# Segunda decodificação: transforma a string interna em objeto JSON.
dados = json.loads(conteudo)


def corrigir_codificacao(texto):

    bytes_originais = bytearray()

    for caractere in texto:
        try:
            bytes_originais.extend(caractere.encode("cp1252"))

        except UnicodeEncodeError:
            codigo = ord(caractere)

            if 0x80 <= codigo <= 0x9F:
                bytes_originais.append(codigo)
            else:
                return texto

    try:
        return bytes_originais.decode("utf-8")

    except UnicodeDecodeError:
        return texto


def corrigir_texto(valor):

    if isinstance(valor, dict):
        return {
            chave: corrigir_texto(item)
            for chave, item in valor.items()
        }

    if isinstance(valor, list):
        return [corrigir_texto(item) for item in valor]

    if isinstance(valor, str):
        if any(marca in valor for marca in ("Ã", "Â", "â")):
            return corrigir_codificacao(valor)

    return valor


dados = corrigir_texto(dados)

# Garante que a pasta de destino exista.
PASTA_DADOS.mkdir(parents=True, exist_ok=True)

# Salva com indentação e acentuação preservada.
destino.write_text(
    json.dumps(dados, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Arquivo formatado com sucesso!")
print("Registros:", len(dados["features"]))
print("Salvo em:", destino.resolve())
