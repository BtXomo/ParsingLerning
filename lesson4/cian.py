import json
from bs4 import BeautifulSoup
import requests



URL = f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&floornl=1&is_first_floor=0&maxprice=12000000&offer_type=flat"
HEADERS = {"Accept" : "*/*", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
}


def count():          #считаем колличество страниц по нашему запросу
    num = 1
    while True:
        url = f"{URL} + {num}&region=&room2=1"
        req = requests.get(url)
        if req.status_code == 200:
            num += 1
        else:
            return num


def st1():           # Считаем сколько на странице вкладок и собираем ссылки и названия для всех предложений на странице
    site_tab = {}   # объявляем словарь для хранения данных
    for i in range(1, count()):
        q = requests.get(f"{URL} + {i}&room2=1")
        req = q.content
        soup = BeautifulSoup(req, "lxml")
        title_all_list = [i.text for i in soup.find_all(
            class_="_93444fe79c--color_black_100--Ephi7 _93444fe79c--lineHeight_22px--FdvaW _93444fe79c--fontWeight_bold--BbhnX _93444fe79c--fontSize_16px--QNYmt _93444fe79c--display_block--KYb25 _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq")]

        href_all = soup.find_all("a", class_="_93444fe79c--link--VtWj6")
        href_list = [item.get("href") for item in href_all]

        for n in range(len(title_all_list)):
            site_tab[title_all_list[n]] = href_list[n]  # добавляем пару ключ-значение в словарь
            print(site_tab)
        with open(f'site_tab{i}.json', "w", encoding="utf-8") as file:     # записываем данные в файл
            json.dump(site_tab, file, indent=4, ensure_ascii=False)
        print(site_tab)





if __name__ == '__main__':
    st1()
