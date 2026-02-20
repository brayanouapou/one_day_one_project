import requests
import pandas as pd
from datetime import datetime

API_KEY = '21169b8202df436db806d0859b11d3fc'
QUERY = 'artificial intelligence Africa OR "Big Data" Africa'
URL = f'https://newsapi.org/v2/everything?q={QUERY}&sortBy=publishedAt&apiKey={API_KEY}'

def fetch_news():
    response = requests.get(URL)
    data = response.json()
    
    if data['status'] == 'ok':
        articles = data['articles']
        news_list = []
        for art in articles[:10]: # On prend les 10 derniers
            news_list.append({
                'Titre': art['title'],
                'Source': art['source']['name'],
                'Lien': art['url'],
                'Date': art['publishedAt'][:10]
            })
        return news_list
    else:
        print("Erreur lors de la récupération")
        return []

def save_to_markdown(news):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"Veille_IA_Afrique_{date_str}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 🌍 Veille IA & Data en Afrique - {date_str}\n\n")
        for i, item in enumerate(news, 1):
            f.write(f"### {i}. {item['Titre']}\n")
            f.write(f"- **Source:** {item['Source']} ({item['Date']})\n")
            f.write(f"- [Lire l'article]({item['Lien']})\n\n")
    print(f"✅ Rapport généré : {filename}")

if __name__ == "__main__":
    articles = fetch_news()
    if articles:
        save_to_markdown(articles)