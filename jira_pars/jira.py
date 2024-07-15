import requests
from getpass import getpass
from bs4 import BeautifulSoup
import csv
import os
from datetime import time
import urllib.request
import re



login = ""
password = ""
url = "https://project.samokat.ru/issues"


# session = requests.Session()
with (requests.Session() as session):
    session.auth = (login, password)

    count = 1
    for n in range(0, 250, 50):
        # response = session.get(f"https://project.samokat.ru/issues/?jql=project%20%3D%20MA%20AND%20assignee%20in%20(currentUser())&startIndex={n}")
        # src = response.text
        # with open(f'index{n}.html', "w", encoding="utf-8") as file:
        #     file.write(src)
        with open(f"index{n}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_issue_link = soup.find_all("td", class_="summary")
        # print(all_issue_link)
        for issue in all_issue_link:
            print(issue)
            task_name = issue.find("p").find("a").text
            # task_name = task_name.replace(" ", "_").replace(".", "_").replace(":", "_").replace("/", "_").replace("+", "_").replace("'", "_").replace('"', '_')
            rep = re.compile("[^a-zA-Za-яА-я,\d]")
            task_name = rep.sub(" ", f"{task_name}")
            task_name = task_name.strip()
            task_number = issue.find(class_="issue-link").get("data-issue-key")
            task_href = f"https://project.samokat.ru" + issue.find(class_="issue-link").get("href")
            # print(task_name)
            # print(task_number)
            # print(task_href)

            session_href = session.get(task_href)
            res_href = BeautifulSoup(session_href.content, "lxml")

            task_date = res_href.find("time", class_="livestamp").text
            # print(task_date)

            task_description = res_href.find("div", class_="user-content-block").find_all("p")
            description_list = []
            for p in task_description:
                description_list.append(p.text.strip())
            task_description_2 = res_href.find("div", class_="user-content-block").find_all("li")
            for li in task_description_2:
                description_list.append(li.text.strip())
            # print(description_list)

            # task_comment_all = res_href.find_next("div", class_="action-body flooded")
            # print(task_comment_all)
            # task_comment = []
            # for comment in task_comment_all:
            #     comment_text = ''
            #     for p in comment.find_all('p'):
            #         comment_text += p.text.strip() + '\n'
            #     task_comment.append(comment_text.strip())
            # print(task_comment)

            os.makedirs(f"{task_name}_{count}")

            with open(f"{task_name}_{count}/{count}_{task_number}_description.csv", "w", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        task_date,
                        description_list
                )
                )
            # with open(f"{task_name}/{task_number}_comment.csv", "w", encoding="utf-8") as file:
            #     writer = csv.writer(file)
            #     writer.writerow(
            #         (
            #             task_comment
            #     )
            #     )

            download_href_list = []
            download_href_all = res_href.find_all("a", class_="attachment-title")
            # print(download_href_all)
            for d in download_href_all:
                if d:
                    download_href = (f"https://project.samokat.ru{d.get("href")}")
                    file_path = f"{task_name}_{count}"
                    filename = f"{task_name}_{count}_file"
                    # local_path = os.path.join(file_path, filename)
                    # session.get(download_href, stream=True).content.save(local_path)
                    r = session.get(download_href)
                    with open(f"{task_name}_{count}/{filename}.xlsx", "wb") as code:
                        code.write(r.content)
                else:
                    continue
            # print(download_href_list)
            count += 1