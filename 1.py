import os
import json
from bs4 import BeautifulSoup
from collections import Counter

def parse_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    book = {}
    book['category'] = soup.find('span').text.split(':')[1].strip()
    book['title'] = soup.find('h1', class_='book-title').text
    book['author'] = soup.find('p', class_='author-p').text
    book['pages'] = int(soup.find('span', class_='pages').text.split(':')[1].split()[0])
    book['year'] = int(soup.find('span', class_='year').text.split()[2])
    isbn_span = soup.find('span', text=lambda text: "ISBN:" in text)
    book['isbn'] = isbn_span.text.split(':')[1].strip() if isbn_span else "N/A"
    book['description'] = soup.find('p').text.strip()  #Simplified description handling
    book['rating'] = float(soup.find('span', text=lambda text: "Рейтинг:" in text).text.split(':')[1].strip())
    book['views'] = int(soup.find('span', text=lambda text: "Просмотры:" in text).text.split(':')[1].strip())
    return book

def process_data(data):
  # Сортировка по рейтингу
  sorted_data = sorted(data, key=lambda x: x['rating'])

  # Фильтрация по количеству страниц (более 500 страниц)
  filtered_data = [book for book in data if book['pages'] > 500]

  # Статистические характеристики для поля "pages"
  pages = [book['pages'] for book in data]
  pages_stats = {
      'sum': sum(pages),
      'min': min(pages),
      'max': max(pages),
      'avg': sum(pages) / len(pages) if pages else 0,
  }

  # Частота меток для поля "category"
  categories = [book['category'] for book in data]
  category_counts = Counter(categories)

  return sorted_data, filtered_data, pages_stats, category_counts


if __name__ == "__main__":
    data = []
    for filename in os.listdir('./resources/1'):
        if filename.endswith('.html'):
            filepath = os.path.join('./resources/1', filename)
            data.append(parse_html(filepath))


    sorted_data, filtered_data, pages_stats, category_counts = process_data(data)

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump({'all_books': data, 'sorted_books': sorted_data, 'filtered_books': filtered_data,
                   'pages_stats': pages_stats, 'category_counts': dict(category_counts)}, f, indent=4, ensure_ascii=False)

    print("Данные успешно записаны в output.json")