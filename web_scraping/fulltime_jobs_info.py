from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import nums_from_string
import concurrent.futures
import time


def extract(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
    scraping = requests.get(url, headers)
    soup = BeautifulSoup(scraping.content, "html.parser")
    return soup


def transform(soup):
    # This is for full descrption
    full_descrption = soup.find_all("div", class_="yvsb870 _1v38w810")
    # This is for salary and location etc
    info_grid = soup.find_all("div", class_="yvsb870 v8nw070 v8nw076")
    info_grid_child = info_grid[0].find_all("div", class_="yvsb870 _14uh9944y o76g430")

    return [full_descrption, info_grid_child]


def clear_raw_data(current_page):
    # transform(current_page)[0] => full description
    result = []
    for i in transform(current_page)[0]:
        for sen in i.find_all():
            cindexr_to_replace = {".": " ", ",": " ", "!": " ", "\xa0": " ", ":": " "}
            clear_sen = sen.text.translate(str.maketrans(cindexr_to_replace)).strip()
            # This remove duplicate sentence cannot remove the whole paragraphy with following child node sentence.
            # To understand this, you can try to uncomment line47: print(sen.text)
            if clear_sen not in result:
                result.append(clear_sen)
    return result


def separate_sentence(current_page):
    # separate each word from a sentence
    sigle_word = []
    for sigle_sen in clear_raw_data(current_page):
        first = 0
        for index, word in enumerate(sigle_sen):
            if word == " ":
                # the code below is to ignor the empty string. for example: ['https', '//switchre', 'com', '', '', '', 'au']
                if (" " or "") not in sigle_sen[first:index].strip():
                    sigle_word.append(sigle_sen[first:index].strip())
                    first = index
        sigle_word.append(sigle_sen[first:].strip())
    return sigle_word


def organise_salary(salary_sentence):
    result_salary = []
    if "k" in salary_sentence or "K" in salary_sentence:
        each_salary = []
        for num in nums_from_string.get_nums(salary_sentence):
            if len(str(num)) <= 3:
                if len(str(int(num * 1000))) <= 6 and (num * 1000) < 300000:
                    each_salary.append(num * 1000)
        result_salary.append(each_salary)
    else:
        # this is to filter out the daily salary for a full time job
        for num in nums_from_string.get_nums(salary_sentence):
            if len(str(num)) >= 5:
                result_salary.append(nums_from_string.get_nums(salary_sentence))
    return result_salary


# open the full jobs list from seek website
job_title = []
company_name = []
states = []
url_without_duplicate = []

with open("./final_result/fulltime_jobs_url.csv", "r") as open_file:
    csvreader = csv.reader(open_file)
    for i in list(csvreader)[1:]:
        if i[3] not in url_without_duplicate:
            job_title.append(i[1])
            company_name.append(i[2])
            states.append(i[3])
            url_without_duplicate.append(i[4])


# ===============capture the key words of programming and database =================
# one_url = "https://www.seek.com.au/job/56806929?type=standard"
# current_page = extract(one_url)
# transform(current_page)
# open the programming languages dictionary
with open("./dictionaries/languages_dict.csv", "r") as pg_open_file:
    reader = csv.reader(pg_open_file)
    langu_dictionary = [i[1] for i in reader][1:]


# open the database dictionary
with open("./dictionaries/database_dict.csv", "r") as db_open_file:
    reader = csv.reader(db_open_file)
    db_dictionary = [i[1] for i in reader][1:]


def full_content(one_url):
    current_page = extract(one_url)
    transform(current_page)
    prgm_lang = []
    db_sys = []
    for word in separate_sentence(current_page):
        for lang in langu_dictionary:
            if lang == word:
                if word not in prgm_lang:
                    prgm_lang.append(word)
        for db in db_dictionary:
            if db == word:
                if word not in db_sys:
                    db_sys.append(word)

    # ====================================================================
    url_index = url_without_duplicate.index(one_url)
    # This IF is to avoid the post page has expired.
    if transform(current_page)[1]:
        for i in transform(current_page)[1]:
            if "$" in i.text:
                # This is to avoid having $ sign but without salary number
                try:
                    salary = round((max(organise_salary(i.text)[0])) * 0.9)

                    break
                except:
                    salary = ""
            salary = ""

        each_job = {
            "Job Title": job_title[url_index],
            "Company Name": company_name[url_index],
            "Office Loaction": states[url_index],
            "Salary": salary,
            "PG": ",".join(prgm_lang),
            "DB": ",".join(db_sys),
            "URL": url_without_duplicate[url_index],
        }
        job_list.append(each_job)
        time.sleep(1)
    return


if __name__ == "__main__":

    url = url_without_duplicate
    job_list = []
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(full_content, url)

    df = pd.DataFrame(job_list)
    df.to_csv("./final_result/fulltime_jobs_info.csv", index=True)

    end = time.time()
    print("2/4")
    print((end - start) / 60)
    # print(f'Each job post web scraping finished and spent: {(end - start) / 60} min(s). => 2 out 3.')
