import json
import time

import requests
from io import BytesIO
import pandas as pd
from parser import models as parser_models
from bs4 import BeautifulSoup
from config.celery_app import app


def fetch_description_from_site(product_id):
    url = f"https://igrushki7.ua/advanced_search_result.php?keywords={product_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(1)
    links = soup.find_all("a", href=True)
    product_link = [link['href'] for link in links if link['href'].startswith(
        'https://igrushki7.ua/product_info.php?info=')][0]
    product_link_ru = "https://igrushki7.ua" + "/ru" + product_link.split('https://igrushki7.ua')[1]

    soup = BeautifulSoup(session.get(product_link, headers=headers).text, "html.parser")
    product_info = soup.find("div", class_="section description").text

    soup_ru = BeautifulSoup(session.get(product_link_ru, headers=headers).text, "html.parser")
    product_info_ru = soup_ru.find("div", class_="section description").text
    return product_info, product_info_ru


@app.task
def fetch_and_save_to_db(task_id):
    global product
    task = parser_models.Task.objects.get(id=task_id)
    url = 'https://igrushki7.ua/export/prom.xlsx'
    response = requests.get(url)

    with BytesIO(response.content) as f:
        product_df = pd.read_excel(f, sheet_name="Export Products Sheet")
        group_df = pd.read_excel(f, sheet_name="Export Groups Sheet")
    product_df = product_df.fillna("")
    group_df = group_df.fillna("")
    group_dict = group_df.set_index("Ідентифікатор_групи")["Назва_групи"].to_dict()
    group_dict_uk = group_df.set_index("Ідентифікатор_групи")["Назва_групи_укр"].to_dict()
    for _, row in product_df.iterrows():
        try:
            group_name = group_dict.get(row["Идентификатор_группы"], "")
            group_name_uk = group_dict_uk.get(row["Идентификатор_группы"], "")

            main_image_link = row.get("Ссылка_изображения", "")
            additional_images = row.get("Дополнительные изображения", "")
            if additional_images:
                all_images = f"{main_image_link},{additional_images.replace('|', ',')}".strip()
            else:
                all_images = main_image_link

            product, created = parser_models.Product.objects.get_or_create(
                product_id=row["Идентификатор_товара"],
                defaults={
                    'task_id': task_id,
                    'product_name': row.get("Название_позиции"),
                    'product_name_uk': row.get("Название_позиции.1"),
                    'search_requests': row.get("Наименование_категории"),
                    'search_requests_uk': row.get("Наименование_категории.1"),
                    'price': row.get("Цена"),
                    'currency': "UAH",
                    'image_link': all_images,
                    'group_name': row.get("Наименование_категории"),
                    'packing_method': row.get("Упаковка"),
                    'packing_method_uk': row.get("Упаковка"),
                    'unique_identificator': row.get("Идентификатор_товара"),
                    'product_identificator': row.get("Идентификатор_товара"),
                    'vendor': row.get("vendor"),
                    'html_header': row.get("Название_позиции"),
                    'html_header_uk': row.get("Название_позиции.1"),
                    'weight': row.get("Вес"),
                    'width': row.get("Ширина"),
                    'height': row.get("Высота"),
                    'length': row.get("Длина"),
                    'html_keywords': group_name,
                    'html_keywords_uk': group_name_uk,
                }
            )
            if created:
                product_info, product_info_ru = fetch_description_from_site(row["Идентификатор_товара"])
                product.description = product_info_ru
                product.description_uk = product_info
                product.save()

        except Exception as e:
            product.delete()
            task.errors = str(e)
            task.status = parser_models.Task.Status.FAILED
            task.save()
            return
    task.status = parser_models.Task.Status.FINISHED
    task.save()


@app.task
def create_task(periodic_task_id):
    periodic_task = parser_models.ParsePeriodicTask.objects.filter(id=periodic_task_id).first()
    parser_models.Task.objects.create(
        name=f"Periodic Task: {periodic_task.name}",
        created_at=periodic_task.created_at,
        status=parser_models.Task.Status.PROCESSING,
        periodic_task_id=periodic_task_id,
    )
