import re
import os
from google.cloud import vision
from google.cloud.vision import types
import csv
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


def detect_labels_uri(uri):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri
    response = client.web_detection(image=image)
    web_detection = response.web_detection
    clear_list = []

    for urls in web_detection.pages_with_matching_images:
        clear_list.append(urls.url)

    # По моему тут оно лишнее
    # image = vision.types.Image(content=content)
    # response = client.label_detection(image=image)

    print(response)
    return clear_list


if __name__ == '__main__':
    # Домен сайта который проверяем
    checked_site = 'cook.me'
    # Ссылки на изображения с проверямого сайта
    urls_checked_site_images = 'linksfile.txt'
    # Файл с результатами проверки
    files_csv_result = 'imagessteal.csv'

    with open(urls_checked_site_images, 'r+', encoding='utf-8') as f:
        keywords = [line.strip() for line in f]

    for pictures in keywords:
        time.sleep(2)
        print("работаю над " + pictures)
        result = detect_labels_uri(pictures)

        for urls_google_pictures in result:
            if checked_site not in urls_google_pictures:
                with open(files_csv_result, 'a', encoding='utf-8') as csv_file:
                    final_string = [pictures, urls_google_pictures]
                    writer = csv.writer(csv_file)
                    writer.writerow(final_string)

    print("Сбор по заданному списку закончен")
