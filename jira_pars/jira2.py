import requests
from bs4 import BeautifulSoup

# Введите свой логин и пароль
login = "ваш логин"
password = "ваш пароль"

# Создайте сессию
session = requests.Session()

# Получите токен для входа
params = {
    "os_username": login,
    "os_password": password,
    "os_destination": "/"
}
response = session.post("https://your-jira-domain.com/auth/jira/login.jsp", data=params)

# Получите список всех задач для вашего аккаунта
url = "https://your-jira-domain.com/issues/search.jsp?issue="
params = {
    "os_username": login,
    "os_password": password,
    "os_destination": "/"
}
response = session.post(url, data=params)

# Разверните HTML и найдите значения, которые мы хотим получить
soup = BeautifulSoup(response.content, "html.parser")
issue_list = soup.find_all("ul", {"class": "issues-list"})[0].findAll("li")

# Откройте файл для записи и запишите заголовки
with open("task_list.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Description", "Due Date", "Comments", "Attachments"])

# Цикл по всем задачам
for issue in issue_list:
    issue_title = issue.find("div", {"class": "title"}).text.strip()
    issue_description = issue.find("div", {"class": "description"}).text.strip()
    issue_due_date = issue.find("div", {"class": "due-date"}).text.strip()

    # Получите комментарии для данной задачи
    comments_url = "https://your-jira-domain.com/issues/" + issue_title + ".jsp?following=true"
    comments_response = session.get(comments_url)
    soup_comments = BeautifulSoup(comments_response.content, "html.parser")
    comments = soup_comments.find_all("div", {"class": "activity"})

    # Откройте файл для записи и запишите комментарии
    with open(f"{issue_title}.txt", "w") as comments_file:
        for comment in comments:
            comments_file.write(comment.text.strip() + "\n")

    # Получите прилагаемые файлы для данной задачи
    attachments_url = "https://your-jira-domain.com/issues/" + issue_title + ".jsp?attachments=true"
    attachments_response = session.get(attachments_url)
    soup_attachments = BeautifulSoup(attachments_response.content, "html.parser")
    attachments = soup_attachments.find_all("a", {"class": "issue-attachment"})

    # Откройте папку для сохранения прилагаемых файлов
    attachments_dir = f"{issue_title}_attachments"
    os.makedirs(attachments_dir)

    # Сохраните прилагаемые файлы
    for attachment in attachments:
        file_name = attachment.text.strip()
        file_url = "https://your-jira-domain.com/" + attachment["href"].split("?")[0]
        with open(os.path.join(attachments_dir, file_name), "wb") as file:
            response = session.get(file_url)
            file.write(response.content)

    # Запишите заголовки и комментарии в файл
    with open("task_list.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([issue_title, issue_description, issue_due_date, comments[0].text.strip(), attachments_dir])