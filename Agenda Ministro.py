import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import html
import unicodedata

def obter_agenda_ministro(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    eventos = soup.find('div', attrs={'ng-init': re.compile(r'^events')})

    padrao = r'\[(.*?)\]'
    eventos = re.findall(padrao, str(eventos))
    eventos = html.unescape(eventos[0])
    eventos = unicodedata.normalize('NFC', eventos)

    with open('pagina.html', 'w', encoding='utf-8') as file:
        file.write(str(eventos))

#     dados = []
#     for evento in eventos:
#         data = evento.get('data_date')
#         hora = evento.find('div', class_='fc-event-time').text.strip()
#         descricao = evento.find('div', class_='fc-event-title').text.strip()
#         dados.append({"Data": data, "Hora": hora, "Evento": descricao})
    
#     return pd.DataFrame(dados)

url_ministro = "https://eagendas.cgu.gov.br/?_token=2LL4g4Z10hKNCjonNfqsfcxcv8bmygmyWNMADkBI&filtro_orgaos_ativos=on&filtro_orgao=1384&filtro_cargos_ativos=on&filtro_cargo=MINISTRO%28A%29+DA+FAZENDA&filtro_apos_ativos=on&filtro_servidor=14641&cargo_confianca_id=&is_cargo_vago=false#divcalendar"
obter_agenda_ministro(url_ministro)   

# df_ministro = obter_agenda_ministro(url_ministro)

# df_ministro.to_excel('agenda_ministro_fazenda.xlsx', index=False)

# print("Agenda do Ministro da Fazenda salva em 'agenda_ministro_fazenda.xlsx'")
