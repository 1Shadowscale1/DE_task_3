import xml.etree.ElementTree as ET
import json
import os
import statistics

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = {}
    for element in root:
        data[element.tag] = element.text.strip()
    return data

def process_xml_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            filepath = os.path.join(directory, filename)
            all_data.append(parse_xml(filepath))
    return all_data

def main():
    xml_directory = "./resources/3"
    all_star_data = process_xml_files(xml_directory)

    # Сортировка по radius
    sorted_data = sorted(all_star_data, key=lambda x: float(x['radius'].replace(' ', '')) if 'radius' in x and x['radius'] else 0)

    # Фильтрация по constellation (только Овен)
    filtered_data = [star for star in all_star_data if 'constellation' in star and star['constellation'] == "Овен"]

    # Статистический анализ radius
    radii = [float(star['radius'].replace(' ', '')) for star in all_star_data if 'radius' in star and star['radius']]
    radius_stats = {}
    if radii:
        radius_stats = {
            "sum": sum(radii),
            "min": min(radii),
            "max": max(radii),
            "mean": statistics.mean(radii),
            "median": statistics.median(radii),
            "stdev": statistics.stdev(radii)
        }

    # Подсчет частоты меток в constellation
    constellation_counts = {}
    for star in all_star_data:
        if 'constellation' in star:
            constellation = star['constellation']
            constellation_counts[constellation] = constellation_counts.get(constellation, 0) + 1

    output_data = {
        "all_data": all_star_data,
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "radius_stats": radius_stats,
        "constellation_counts": constellation_counts
    }

    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()