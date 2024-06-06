import requests
import csv
import json
from bs4 import BeautifulSoup
import re


url = "https://parsemachine.com/sandbox/catalog/"



headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
}
# req = requests.get(url, headers = headers)
# src = req.text


# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

# with open("index.html", encoding="utf-8") as file:
#     src=file.read()
#
#
# soup = BeautifulSoup(src, "lxml")
# all_products_href = soup.find_all(class_="card-title")
#
# all_cat_dict = {}
# for item in all_products_href:
#     item_text = item.text.replace("\n", "").replace(" ","",)
#     item_href = "https://parsemachine.com" + item.find("a", class_="no-hover").get("href")
#     print(f"{item_text}: {item_href}")
#
#     all_cat_dict[item_text] = item_href


# with open("all_cat_dict.json", "w") as file:
#     json.dump(all_cat_dict, file, indent=4, ensure_ascii=False)

with open("all_cat_dict.json") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
for cat_name, cat_href in all_categories.items():
    req = requests.get(url=cat_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{cat_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data/{count}_{cat_name}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    price = soup.find(class_="mt-0 mb-0").find("span").text
    price_value = soup.find(class_="mt-0 mb-0").find("big").text.replace("\xa0", "")
    articul = soup.find(class_="mt-4 mb-0").find("span").text
    articul_value = soup.find(class_="mt-4 mb-0").find(id="sku").text
    charact = soup.find(class_="col-xl-6 col-lg-7 col-md-8 col-sm-7 col-12").find_all("td")
    char = []
    for i in charact:
        char.append(i.text)
    charactiristics = soup.find(class_="mt-0 mb-2").find("span").text
    characteristic_value = " ".join(char)
    staf_discription = soup.find(class_="mt-4 mb-2").find("span").text.strip() + ": " + soup.find(class_="mt-4 mb-2").find(id="description").text.strip().replace("\n", " ")
    staf_discription_value = soup.find(class_="mt-4 mb-2").find(id="description").text.strip().replace("\n", " ")
    staf_discription_value = re.sub(r' +', ' ', staf_discription_value)

    with open(f"data/{count}_{cat_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                price +":"+ price_value,
                articul +":"+ articul_value,
                charactiristics +":"+ characteristic_value,
                staf_discription +":"+ staf_discription_value
            )
        )


    product_info = []

    product_info.append(
        {
            "price": price_value,
            "articul": articul_value,
            "charactiristics": characteristic_value,
            "staf_discription": staf_discription_value
        }
    )

    with open (f"data/{count}_{cat_name}.json", "w", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1

    if count == 0:
        print ("the job is done")
        break




# if __name__ == '__main__':


