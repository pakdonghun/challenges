
from bs4 import BeautifulSoup
import requests
import os
import csv

os.system("clear")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def stack(word):
    url_for_page = f"https://stackoverflow.com/jobs?r=true&q={word}"
    result = requests.get(url_for_page)
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        pagination = soup.find("div", {"class": "s-pagination"})
        pages = pagination.find_all("a")
        last_page = pages[-2].text.strip()
        datas_stack = []
        for each_page in range(int(last_page)):
            print(f"Stackover Scrapping page {each_page+1}")
            url = f"https://stackoverflow.com/jobs?r=true&q={word}&pg={each_page+1}"
            result = requests.get(url)
            soup = BeautifulSoup(result.text, "html.parser")
            lists = soup.find_all("div", {"class": "grid--cell fl1"})
            data_stack = []
            for list in lists:
                title = list.find("a").text
                company = list.find("h3").find("span").text.strip()
                if "via" in company:
                    company = company.replace(
                        company[company.find('via'):], "").rstrip()
                link = list.find("a")["href"]
                link = f"https://stackoverflow.com{link}"
                data = {"title": title, "company": company, "link": link}
                data_stack.append(data)
            datas_stack += data_stack
    except:
        print("No job or jobs less than a page found for stackoverflow")
        datas_stack = []
    return datas_stack


def wwr(word):
    url_for_page = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    result = requests.get(url_for_page, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        lists = soup.find("article").find_all("li", {"class": "feature"})
        datas_wwr = []
        print(f"Weworkremotely Scrapping")
        for list in lists:
            title = list.find("span", {"class": "title"}).text
            company = list.find("span", {"class": "company"}).text
            link = list.find("a")["href"]
            link = "https://weworkremotely.com/remote-jobs" + link
            data = {"title": title,
                    "company": company, "link": link}
            datas_wwr.append(data)
    except:
        print("No job found for weworkremote")
        datas_wwr = []
    return datas_wwr


def remoteok(word):
    url_for_page = f"https://remoteok.io/remote-dev+{word}-jobs"
    result = requests.get(url_for_page, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        lists = soup.find_all("tr", {"class": "job"})
        datas_remoteok = []
        print(f"Remoteok Scrapping")
        for list in lists:
            if list != None:
                info = list.find("td", {"class": "company_and_position"})
                title = info.find("h2").text
                company = info.find("h3").text
                link = info.find("a")["href"]
                link = "https://remoteok.io/" + link
                data = {"title": title, "company": company, "link": link}
            datas_remoteok.append(data)
    except:
        print("No job found for remoteok")
        datas_remoteok = []
    return datas_remoteok


def total_datas(word):
    data1 = stack(word)
    data2 = wwr(word)
    data3 = remoteok(word)
    total = data1 + data2 + data3
    return total


def save_to_csv_file(datas, word, rownames):
    file = open(f"{word}_jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(rownames)
    for data in datas:
        writer.writerow(list(data.values()))
    return
