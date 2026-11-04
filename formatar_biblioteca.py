
import json
from pathlib import Path


origem = Path("biblioteca.json")
destino = Path("biblioteca_legivel.json")

# Primeira decodificação: remove a camada externa de JSON.
texto = origem.read_text(encoding="utf-8")
conteudo = json.loads(texto)

# Segunda decodificação: transforma a string interna em objeto JSON.
dados = json.loads(conteudo)


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
            try:
                return valor.encode("cp1252").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass

    return valor


dados = corrigir_texto(dados)

# Salva com indentação e acentuação preservada.
destino.write_text(
    json.dumps(dados, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Arquivo formatado com sucesso!")
print("Registros:", len(dados["features"]))
print("Salvo em:", destino.resolve())
