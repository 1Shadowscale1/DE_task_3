import xml.etree.ElementTree as ET
import json
import os
import statistics

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    all_clothing = []
    for clothing in root.findall('clothing'):
        clothing_data = {}
        for element in clothing:
            clothing_data[element.tag] = element.text.strip()
        all_clothing.append(clothing_data)
    return all_clothing

def process_xml_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            filepath = os.path.join(directory, filename)
            try:
                all_data.extend(parse_xml(filepath))
            except ET.ParseError:
                print(f"Ошибка парсинга файла: {filepath}")
    return all_data

def main():
    xml_directory = "./resources/4"
    all_clothing_data = process_xml_files(xml_directory)

    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(all_clothing_data, json_file, ensure_ascii=False, indent=4)

    # Сортировка по price (числовое поле)
    sorted_data = sorted(all_clothing_data, key=lambda x: float(x['price']) if 'price' in x and x['price'] else 0)

    # Фильтрация по category (текстовое поле) - например, только Shirt
    filtered_data = [item for item in all_clothing_data if 'category' in item and item['category'] == "Shirt"]

    # Статистический анализ price
    prices = [float(item['price']) for item in all_clothing_data if 'price' in item and item['price']]
    price_stats = {}
    if prices:
        price_stats = {
            "sum": sum(prices),
            "min": min(prices),
            "max": max(prices),
            "mean": statistics.mean(prices),
            "median": statistics.median(prices),
            "stdev": statistics.stdev(prices)
        }

    # Подсчет частоты меток в category
    category_counts = {}
    for item in all_clothing_data:
        if 'category' in item:
            category = item['category']
            category_counts[category] = category_counts.get(category, 0) + 1

    output_data = {
        "all_data": all_clothing_data,
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "price_stats": price_stats,
        "category_counts": category_counts
    }

    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()