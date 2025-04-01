import os
import sys
import django
import csv
from datetime import datetime

# Garante que o Django encontre o projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Ajuste para o caminho do seu projeto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")  # Nome correto do projeto
django.setup()

from api_charts.models import SpotifyChart

# Caminho do CSV
CSV_FILE_PATH = "../data_csv/spotify_charts_2025-03-24.csv"

# Definir uma data padrão para os dados importados (já que não existe no CSV)
CHART_DATE = datetime.strptime("2025-03-24", "%Y-%m-%d").date()

def limpar_numero(valor):
    """ Remove vírgulas e converte para inteiro, tratando valores vazios """
    if valor and valor.strip():  # Verifica se o valor não está vazio
        return int(valor.replace(',', ''))
    return None

def importar_csv():
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Mapeando os nomes das colunas corretamente
        count = 0
        for row in reader:
            try:
                SpotifyChart.objects.update_or_create(
                    position=int(row['Position']),
                    chart_date=CHART_DATE,  # Definindo a data manualmente
                    defaults={
                        'change': row['Change'],
                        'artist_title': row['Artist and Title'],  # Nome corrigido
                        'days': int(row['Days']),
                        'peak': int(row['Peak']),
                        'multiplier': row.get('Multiplier', None),
                        'streams': limpar_numero(row['Streams']),
                        'streams_change': row['Streams Change'] if row['Streams Change'].strip() else "",
                        'week_streams': limpar_numero(row['7-Day Streams']),  # Nome corrigido
                        'week_streams_change': limpar_numero(row['7-Day Change']),  # Nome corrigido
                        'total_streams': limpar_numero(row['Total Streams']),
                    }
                )
                count += 1
            except Exception as e:
                print(f"Erro ao importar linha {row}: {e}")
    
    print(f"Importação concluída! {count} registros adicionados ou atualizados.")

if __name__ == "__main__":
    importar_csv()
