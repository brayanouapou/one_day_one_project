from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = '21169b8202df436db806d0859b11d3fc'

# Dictionnaire nettoyé (un seul exemplaire par pays)
COUNTRIES = {
    "SEN": ["Sénégal", "Dakar", "Senegal"],
    "CIV": ["Côte d'Ivoire", "Abidjan", "Ivory Coast"],
    "CAR": ["Central African Republic", "Bangui", "Centrafrique"],
    "CMR": ["Cameroon", "Yaoundé", "Cameroun"],
    "COD": ["Congo", "Kinshasa", "DRC", "RDC"],
    "EGY": ["Egypt", "Cairo", "Égypte"],
    "ETH": ["Ethiopia", "Addis Ababa", "Éthiopie"],
    "GAB": ["Gabon", "Libreville"],
    "GHA": ["Ghana", "Accra"],
    "GMB": ["Gambia", "Banjul", "Gambie"],
}

def get_africa_news():
    query = 'Africa AND (AI OR "Big Data" OR "Machine Learning" OR "Intelligence Artificielle")'
    url = f'https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={API_KEY}'
    
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
    except Exception as e:
        print(f"Erreur API : {e}")
        return []
    
    processed_news = []
    
    for art in articles[:15]:
        title = art.get('title', '')
        description = art.get('description', '')
        content_to_scan = f"{title} {description}" # On scanne titre + description pour plus de précision
        
        # --- LOGIQUE DE FILTRAGE AMÉLIORÉE ---
        detected_country = None
        is_local = False
        
        for code, names in COUNTRIES.items():
            if any(name.lower() in content_to_scan.lower() for name in names):
                is_local = True
                detected_country = code
                break # On s'arrête au premier pays trouvé
        
        processed_news.append({
            "title": title,
            "source": art['source']['name'],
            "url": art['url'],
            "is_local": is_local,
            "country_code": detected_country,
            "description": description
        })
    return processed_news

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    news = get_africa_news()
    return templates.TemplateResponse("index.html", {"request": request, "news": news})

@app.get("/api/news")
async def get_json_news():
    return {"data": get_africa_news()}