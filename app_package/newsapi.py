import requests
from concurrent.futures import ThreadPoolExecutor
from config import NEWS_API_KEY


def fetch_general_headlines(api_key):
    url = f'https://newsapi.org/v2/top-headlines?language=en&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'ok':
            return response.json()['articles']
        else:
            raise Exception('General headlines news API returned an error')
    except Exception as e:
        print(f"Error fetching general headlines: {e}")
        return []


def fetch_google_news(api_key):
    url = f'https://newsapi.org/v2/top-headlines?sources=google-news&language=en&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'ok':
            return response.json()['articles']
        else:
            raise Exception('General headlines news API returned an error')
    except Exception as e:
        print(f'Error fetching general headlines: {e}')
        return []


def fetch_news():
    with ThreadPoolExecutor(max_workers=2) as executor:
        general_headlines = executor.submit(fetch_general_headlines, NEWS_API_KEY)
        google_news = executor.submit(fetch_google_news, NEWS_API_KEY)

        news_items = []
        news_items.extend(general_headlines.result())
        news_items.extend(google_news.result())

        selected_news = news_items[:20]

        news = []
        for article in selected_news:
            news.append(f"{article['title']}\n{article['description']}\n{article['url']}")

        return news
