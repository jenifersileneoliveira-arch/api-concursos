from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

def buscar_concursos():

    url = "https://www.pciconcursos.com.br/concursos/"
    resposta = requests.get(url)

    soup = BeautifulSoup(resposta.text, "html.parser")

    concursos = []

    for item in soup.select(".ca")[:20]:

        texto = item.get_text(" ", strip=True)

        # ORGÃO
        orgao = texto.split(" vagas")[0].split(" Vagas")[0].strip()

        # VAGAS
        vagas = 0
        vagas_match = re.search(r"(\d+)\s*vagas", texto, re.IGNORECASE)
        if vagas_match:
            vagas = int(vagas_match.group(1))

        # SALÁRIO
        salario = "A definir"
        salario_match = re.search(r"R\$\s?[\d\.\,]+", texto)
        if salario_match:
            salario = salario_match.group(0)

        # DATA
        dataProva = "A definir"
        data_match = re.search(r"\d{2}/\d{2}/\d{4}", texto)
        if data_match:
            dataProva = data_match.group(0)

        # ESCOLARIDADE
        escolaridade = "A definir"
        if "Superior" in texto:
            escolaridade = "Superior"
        elif "Médio" in texto:
            escolaridade = "Médio"
        elif "Fundamental" in texto:
            escolaridade = "Fundamental"

        # LINK DO EDITAL
        link = "https://www.pciconcursos.com.br"

        concursos.append({
            "orgao": orgao,
            "vagas": vagas,
            "escolaridade": escolaridade,
            "dataProva": dataProva,
            "salario": salario,
            "taxa": "A definir",
            "link": link
        })

    return concursos


@app.get("/concursos")
def listar_concursos():
    return buscar_concursos()