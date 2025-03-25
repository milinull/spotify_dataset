import requests # type: ignore
import csv
import os
from bs4 import BeautifulSoup # type: ignore
import re
import html

def fix_encoding(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except UnicodeEncodeError:
        return text

def get_spotify_charts():
    url = "https://kworb.net/spotify/country/global_daily.html"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Obtendo a data
    title_text = soup.find("span", class_="pagetitle").text
    date_match = re.search(r"(\d{4}/\d{2}/\d{2})", title_text)
    date_str = date_match.group(1) if date_match else "unknown_date"
    filename = f"spotify_charts_{date_str.replace('/', '-')}.csv"
    
    # Criando diretório data_csv se não existir
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data_csv")
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)
    
    # Obtendo os dados da tabela
    table_rows = soup.find_all("tr")[1:]  # Pulando o cabeçalho
    data = []
    
    for row in table_rows:
        columns = row.find_all("td")
        if len(columns) < 10:
            continue  # Evita linhas incompletas
        
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
        
        data.append([pos, change, artist_title, days, peak, multiplier, streams, streams_change, week_streams, week_streams_change, total_streams])
    
    # Salvando no CSV
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Position", "Change", "Artist and Title", "Days", "Peak", "Multiplier", "Streams", "Streams Change", "7-Day Streams", "7-Day Change", "Total Streams"])
        writer.writerows(data)
    
    print(f"Arquivo salvo: {filepath}")

if __name__ == "__main__":
    get_spotify_charts()
