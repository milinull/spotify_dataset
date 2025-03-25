# Script para extração de dados dos Charts Globais do Spotify
# Descrição: Realiza web scraping do site Kworb.net para coletar dados diários dos charts do Spotify

import requests # type: ignore
import csv
import os
from bs4 import BeautifulSoup # type: ignore
import re
import html

def fix_encoding(text):
    """
    Corrige problemas de codificação, convertendo texto de Latin-1 para UTF-8.
    Útil para lidar com caracteres especiais em títulos de músicas.
    """
    try:
        return text.encode('latin1').decode('utf-8')
    except UnicodeEncodeError:
        return text

def get_spotify_charts():
    """
    Função principal que extrai os charts do Spotify:
    - Faz scraping do site Kworb.net
    - Extrai dados da tabela de músicas
    - Salva informações em arquivo CSV
    - Gera nome de arquivo com data do chart
    """
    # URL dos charts globais diários do Spotify
    url = "https://kworb.net/spotify/country/global_daily.html"
    
    # Realiza requisição e parseia o HTML
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extrai data do chart para nomear o arquivo
    title_text = soup.find("span", class_="pagetitle").text
    date_match = re.search(r"(\d{4}/\d{2}/\d{2})", title_text)
    date_str = date_match.group(1) if date_match else "unknown_date"
    filename = f"spotify_charts_{date_str.replace('/', '-')}.csv"
    
    # Configura diretório para salvar o arquivo
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data_csv")
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)
    
    # Processa dados da tabela de charts
    table_rows = soup.find_all("tr")[1:]  # Pula cabeçalho
    data = []
    
    for row in table_rows:
        columns = row.find_all("td")
        if len(columns) < 10:
            continue  # Pula linhas incompletas
        
        # Extrai e limpa dados de cada coluna
        pos = columns[0].text.strip()
        change = columns[1].text.strip()
        artist_title = fix_encoding(html.unescape(columns[2].text.strip()))
        days = columns[3].text.strip()
        peak = columns[4].text.strip()
        multiplier = columns[5].text.strip()
        streams = columns[6].text.strip().replace(',', '')
        streams_change = columns[7].text.strip()
        week_streams = columns[8].text.strip().replace(',', '')
        week_streams_change = columns[9].text.strip()
        total_streams = columns[10].text.strip().replace(',', '')
        
        # Adiciona linha de dados
        data.append([pos, change, artist_title, days, peak, multiplier, 
                     streams, streams_change, week_streams, 
                     week_streams_change, total_streams])
    
    # Salva dados em arquivo CSV
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Position", "Change", "Artist and Title", "Days", 
                         "Peak", "Multiplier", "Streams", "Streams Change", 
                         "7-Day Streams", "7-Day Change", "Total Streams"])
        writer.writerows(data)
    
    print(f"Arquivo salvo: {filepath}")

# Executa script apenas quando rodado diretamente
if __name__ == "__main__":
    get_spotify_charts()