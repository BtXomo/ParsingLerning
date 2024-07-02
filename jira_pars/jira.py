import requests
import csv
import json
from bs4 import BeautifulSoup
import os



# URL = "https://project.samokat.ru/browse/MA-7607?jql=project%20%3D%20MA%20AND%20assignee%20in%20(currentUser())%20ORDER%20BY%20created%20DESC"
URL = "https://project.samokat.ru"
HEADERS = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}


def st1():
    for i in range(0, 250, 50):
        url = f"{URL} + {i}"
        q = requests.get(url)
        result = q.content
        soup = BeautifulSoup(result, "lxml")
        task_number = soup.find_all(class_="issue-link-key").text
        st2(task_number)


def st2(task_number):
    for i in task_number:
        q = requests.get(f"{URL} + i")
        result = q.content
        soup = BeautifulSoup(result, "lxml")
        task_name = soup.find(class_="issue-link-summary").text
        task_description = soup.find().text
        task_date = soup.find().text

        if  # проверка на комментарии
            task_comments = soup.find().text
        else:
            continue

        os.makedirs(f"C:/{task_number}_{task_date}/")
        with open(f"C:/{task_number}/{task_name}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                "Описание:" + task_description,
            )
        with open(f"C:/{task_number}/{task_name}_Комментарии.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                "Комментарии:" + task_comments
            )

            # скачивание файлов
            # получаем содержимое файла
            url = 'https://www.example.com/example.pdf'
            response = requests.get(url)

            # проверяем успешность запроса
            if response.status_code == 200:
                with open('example.pdf', 'wb') as file:
                    file.write(response.content)
                print('Файл успешно скачан')
            else:
                continue


if __name__ == '__main__':
    st1()