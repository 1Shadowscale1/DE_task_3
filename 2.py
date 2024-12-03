import os
import json
import re
from bs4 import BeautifulSoup
from collections import Counter

def parse_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    products = []
    for product_item in soup.find_all('div', class_='product-item'):
        product = {}
        product['id'] = product_item.find('a', class_='add-to-favorite')['data-id']

        try:
          product['name'] = product_item.find('span').text.strip()
        except:
          product['name'] = "Название отсутствует"

        try:
          product['price'] = int(re.sub(r'\D', '', product_item.find('price').text))
        except:
          product['price'] = 0


        for li in product_item.find_all('li'):
            type_ = li['type']
            value = li.text.strip()
            product[type_] = value

        products.append(product)
    return products


def process_data(data):
    # Сортировка по цене
    sorted_data = sorted(data, key=lambda x: x['price'])

    # Фильтрация по объему оперативной памяти (при наличии)
    filtered_data = [x for x in data if 'acc' in x and '6280' in x['acc']]

    # Статистический анализ цены
    prices = [item['price'] for item in data if 'price' in item]
    if prices:
        price_stats = {
            'sum': sum(prices),
            'min': min(prices),
            'max': max(prices),
            'avg': sum(prices) / len(prices)
        }
    else:
        price_stats = {'sum':0,'min':0,'max':0,'avg':0}

    # Частота меток для поля "processor"
    processor_counts = Counter([item['processor'] for item in data if 'processor' in item])

    return sorted_data, filtered_data, price_stats, processor_counts


directory = './resources/2'
all_products = []
for filename in os.listdir(directory):
  if filename.endswith(".html"):
    filepath = os.path.join(directory, filename)
    all_products.extend(parse_html(filepath))

sorted_data, filtered_data, price_stats, processor_counts = process_data(all_products)

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump({
        'all_products': all_products,
        'sorted_by_price': sorted_data,
        'filtered_by_acc': filtered_data,
        'price_stats': price_stats,
        'processor_counts': dict(processor_counts)
    }, f, ensure_ascii=False, indent=4)

print("Данные успешно записаны в output.json")
