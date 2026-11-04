
import requests
from html.parser import HTMLParser
from pathlib import Path

URL = "https://siga.santoandre.sp.gov.br/Catalogo"


class HiddenInputParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.fields = {}

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "input":
            return

        attributes = dict(attrs)

        if attributes.get("type", "").lower() == "hidden":
            name = attributes.get("name")
            value = attributes.get("value", "")

            if name:
                self.fields[name] = value


with requests.Session() as session:

    # ETAPA 1: carregar o catálogo.
    print("1. Carregando o catálogo...")

    pagina = session.get(URL, timeout=30)
    pagina.raise_for_status()

    parser = HiddenInputParser()
    parser.feed(pagina.text)

    dados = parser.fields.copy()

    # Selecionar a camada Biblioteca (ID 90).
    dados["ctl00$ContentPlaceHolder1$hfAcao1"] = "ver"
    dados["ctl00$ContentPlaceHolder1$hfIdRegistro1"] = "90"
    dados["ctl00$ContentPlaceHolder1$btnTabelaDados1"] = ""

    # ETAPA 2: abrir os metadados.
    print("2. Abrindo os metadados da Biblioteca...")

    metadados = session.post(
        URL,
        data=dados,
        headers={"Referer": URL},
        timeout=30
    )
    metadados.raise_for_status()

    if "btnGeoJson" not in metadados.text:
        print("Não encontrei o botão GeoJSON na página.")
        raise SystemExit

    # ETAPA 3: extrair os campos ocultos atualizados.
    parser = HiddenInputParser()
    parser.feed(metadados.text)

    dados = parser.fields.copy()

    # Acionar o ImageButton GeoJSON.
    # As coordenadas indicam um ponto dentro do ícone.
    dados["ctl00$ContentPlaceHolder1$btnGeoJson.x"] = "30"
    dados["ctl00$ContentPlaceHolder1$btnGeoJson.y"] = "35"

    print("3. Solicitando o arquivo GeoJSON...")

    arquivo = session.post(
        URL,
        data=dados,
        headers={"Referer": URL},
        timeout=30
    )
    arquivo.raise_for_status()

    content_type = arquivo.headers.get("Content-Type", "")
    content_disposition = arquivo.headers.get("Content-Disposition", "")

    print("\n--- RESULTADO ---")
    print("Status:", arquivo.status_code)
    print("Content-Type:", content_type)
    print("Content-Disposition:", content_disposition)
    print("Tamanho:", len(arquivo.content), "bytes")

    # Só salvar se o servidor confirmar que devolveu JSON.
    if "application/json" in content_type.lower():

        destino = Path("biblioteca.json")
        destino.write_bytes(arquivo.content)

        print("\nArquivo salvo em:")
        print(destino.resolve())

    else:
        print("\nO servidor não retornou JSON.")
        print("Início da resposta:")
        print(arquivo.text[:500])
