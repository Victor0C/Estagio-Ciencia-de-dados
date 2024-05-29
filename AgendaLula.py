import requests
from bs4 import BeautifulSoup
import pandas as pd

def obter_agenda_presidente(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    eventos = soup.find_all('div', class_='compromisso')
    
    dados = []
    for evento in eventos:
        hora = evento.find('span', class_='horario').text.strip()
        descricao = evento.find('span', class_='descricao').text.strip()
        dados.append({"Data": url.split('/')[-1], "Hora": hora, "Evento": descricao})
    
    return pd.DataFrame(dados)

urls_presidente = [
    "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/2024-05-21",
    "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/2024-05-22",
    "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/2024-05-23"
]

df_presidente = pd.concat([obter_agenda_presidente(url) for url in urls_presidente], ignore_index=True)

df_presidente.to_excel('agenda_presidente_lula.xlsx', index=False)

print("Agenda do Presidente Lula salva em 'agenda_presidente_lula.xlsx'")
