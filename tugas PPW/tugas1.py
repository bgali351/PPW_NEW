from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

def replace_text(txt):
    txt = txt.replace('Baca berita tanpa iklan.', '')
    txt = txt.replace('\xa0', '')
    txt = txt.replace('\n', '')
    return txt

def scraping(soup):
    isi_berita = {}

    title = soup.find('h1', {'class': 'read__title'})
    isi_berita["judul"] = title.text.strip() if title else "Title not found"

    rplc = []
    berita = soup.find('div', {'class': 'read__content'})
    if berita:
        for paragraph in berita.find_all('p'):
            rplc.append(replace_text(paragraph.text))
        isi_berita["isi"] = " ".join(rplc)
    else:
        isi_berita["isi"] = "Content not found"

    date = soup.find('div', {'class': 'read__time'})
    isi_berita["tanggal"] = date.text.strip() if date else "Date not found"

    category = soup.select_one('body > div.wrap > div.container.clearfix > div:nth-child(3) > div > h3 > ul > li:nth-child(3) > a > span')
    isi_berita["kategori"] = category.text.strip() if category else "Category not found"
    return isi_berita

def linked_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return bs(response.text, "html5lib")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def link_berita(soup):
    if soup:
        konten = soup.find('div', {'class': 'articleList -list'})
        if konten:
            articles = konten.find_all("div", class_="articleItem")
            print(f"Found {len(articles)} articles on this page.")  # Debugging print
            return articles
    print("No articles found.")  # Debugging print
    return []

def start(page=1):
    base_url = 'https://indeks.kompas.com/?site=news&page='
    news = []

    for current_page in range(1, page + 1):
        url = base_url + str(current_page)
        print(f"Fetching page: {url}")  # Debugging print
        soup = linked_news(url)
        if soup:
            articles = link_berita(soup)
            for article in articles:
                new_link = article.find('a')['href']
                soup_berita = linked_news(new_link)
                if soup_berita:
                    hasil = scraping(soup_berita)
                    news.append(hasil)
        time.sleep(1)
    return news

page = int(input('Masukkan jumlah halaman: '))
berita = start(page)

if berita:
    # Create a DataFrame and display it
    dataFrame = pd.DataFrame(berita)
    print(dataFrame)
    
    # Save DataFrame to a CSV file
    csv_filename = 'berita_kompas.csv'
    dataFrame.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"Data has been saved to {csv_filename}")
else:
    print("No news data was collected.")


