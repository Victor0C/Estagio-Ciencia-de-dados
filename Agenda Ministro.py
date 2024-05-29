import requests
from bs4 import BeautifulSoup
import pandas as pd

def obter_agenda_ministro(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    eventos = soup.find_all('div', class_='evento')
    
    dados = []
    for evento in eventos:
        data = evento.find('span', class_='data').text.strip()
        hora = evento.find('span', class_='hora').text.strip()
        descricao = evento.find('span', class_='descricao').text.strip()
        dados.append({"Data": data, "Hora": hora, "Evento": descricao})
    
    return pd.DataFrame(dados)

url_ministro = "https://eagendas.cgu.gov.br/?_token=2LL4g4Z10hKNCjonNfqsfcxcv8bmygmyWNMADkBI&filtro_orgaos_ativos=on&filtro_orgao=1384&filtro_cargos_ativos=on&filtro_cargo=MINISTRO%28A%29+DA+FAZENDA&filtro_apos_ativos=on&filtro_servidor=14641&cargo_confianca_id=&is_cargo_vago=false#divcalendar"

df_ministro = obter_agenda_ministro(url_ministro)

df_ministro.to_excel('agenda_ministro_fazenda.xlsx', index=False)

print("Agenda do Ministro da Fazenda salva em 'agenda_ministro_fazenda.xlsx'")
