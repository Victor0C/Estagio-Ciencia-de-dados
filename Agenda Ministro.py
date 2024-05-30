import requests
from bs4 import BeautifulSoup
import re
import html
import json
import pandas as pd

#Decodifica o caracteres HTML e sequências unicode.
def decode_dict(d):
    for k, v in d.items():
        if isinstance(v, str):
            d[k] = html.unescape(v.encode().decode('unicode_escape'))
        elif isinstance(v, dict):
            d[k] = decode_dict(v)
    return d

def obter_agenda_ministro(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Procuro a tag <div> com o atributo 'ng-init' que contém 'events', é onde está os eventos do ministro
    eventos_div = soup.find('div', attrs={'ng-init': re.compile(r'^events')})
    
    # Pego o conteúdo do atributo 'ng-init'
    ng_init_content = eventos_div.get('ng-init', '')
    
    # Expressão regular para pegar o conteúdo que representa os eventos em JSON
    padrao = r'events=(\[.*?\])'
    match = re.search(padrao, ng_init_content)
    
    if match:
        #Aqui estou pegando todo o conteúdo JSON de dentro do 'events' pelo primeiro grupo que re.search() encontrou
        eventos_json = match.group(1)
        
        # Aqui estou convertendo a string JSON para uma lista de dicionários Python
        eventos = json.loads(eventos_json)
        
        # Decodifica caracteres unicode e entidades HTML para cada evento
        decoded_data = [decode_dict(evento) for evento in eventos]
        
        # Aqui seleciono somente os eventos dos dias 29, 28 e 27
        eventos_filtrados = [
            evento for evento in decoded_data 
            if evento.get('start', '').startswith('2024-05-29') or evento.get('start', '').startswith('2024-05-28') or evento.get('start', '').startswith('2024-05-27')
        ]

        dados =[]
        for evento in eventos_filtrados:
            data, hora = evento['start'].split('T')
            dados.append({"Data": data, "Hora": hora, "Evento": evento['title']})
    
        pd.DataFrame(dados).to_excel('agenda_ministro_fazenda.xlsx', index=False)
        print("Agenda do Ministro da Fazenda salva em 'agenda_ministro_fazenda.xlsx'")

    else:
        print("Nenhum evento encontrado.")

url_ministro = "https://eagendas.cgu.gov.br/?_token=2LL4g4Z10hKNCjonNfqsfcxcv8bmygmyWNMADkBI&filtro_orgaos_ativos=on&filtro_orgao=1384&filtro_cargos_ativos=on&filtro_cargo=MINISTRO%28A%29+DA+FAZENDA&filtro_apos_ativos=on&filtro_servidor=14641&cargo_confianca_id=&is_cargo_vago=false#divcalendar"

obter_agenda_ministro(url_ministro)