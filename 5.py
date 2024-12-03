import os
import json
from bs4 import BeautifulSoup
import statistics

# Cайт каталог банкнот
def parse_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            product = {}
            # Извлечение данных из разных элементов HTML
            name_element = soup.find('a', class_='name')
            if name_element:
                product['name'] = name_element.text.strip()
            price_element = soup.find('span', class_='price')
            if price_element:
                try:
                    product['price'] = int(price_element.text.strip().split()[0])
                except (ValueError, IndexError):
                    product['price'] = None #обработка ошибки если цена не число
            img_element = soup.find('img', class_='img front')
            if img_element:
                product['image_src'] = img_element['src']

            # Добавление других полей по необходимости,  адаптируя селекторы к вашей HTML структуре


            return product
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при парсинге файла {filepath}: {e}")
        return None


def process_data(data):
    # Сортировка по цене
    sorted_data = sorted(data, key=lambda x: x['price'] if x['price'] is not None else float('inf'))

    # Фильтрация по цене (например, товары дороже 400 руб.)
    filtered_data = [item for item in data if item['price'] and item['price'] > 400]

    # Статистика для числового поля (цена)
    prices = [item['price'] for item in data if item['price'] is not None]
    if prices:
        stats = {
            'mean': statistics.mean(prices),
            'median': statistics.median(prices),
            'stdev': statistics.stdev(prices) if len(prices) > 1 else 0
        }
    else:
        stats = {'mean': None, 'median': None, 'stdev': None}


    # Подсчет частоты слов в текстовом поле (название)
    name_counts = {}
    for item in data:
      if 'name' in item:
        words = item['name'].lower().split()
        for word in words:
          name_counts[word] = name_counts.get(word, 0) + 1

    return {
        'sorted_data': sorted_data,
        'filtered_data': filtered_data,
        'price_statistics': stats,
        'name_word_counts': name_counts
    }

html_dir = './resources/5'

all_product_data = []
for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(html_dir, filename)
        product = parse_html(filepath)
        if product:
            all_product_data.append(product)

results = process_data(all_product_data)

with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print("Данные успешно записаны в файл output.json")