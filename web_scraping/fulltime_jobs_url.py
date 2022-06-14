from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


def extract(url, page, extra_query=""):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
    prefix = "https://www.seek.com.au/jobs-in-information-communication-technology"
    final_url = prefix + url + str(page) + extra_query
    scraping = requests.get(final_url, headers)
    soup = BeautifulSoup(scraping.content, "html.parser")
    # add one more location
    return soup


def transform(loc, soup):
    title_and_Url = soup.find_all(
        "a",
        class_="_1tmgvw5 _1tmgvw8 _1tmgvwb _1tmgvwc _1tmgvwf yvsb870 yvsb87f _14uh994h",
    )

    company = soup.find_all(
        "span",
        class_="yvsb870 _14uh9944u _1qw3t4i0 _1qw3t4i1x _1qw3t4i2 _1d0g9qk4 _1qw3t4ie",
    )
    if title_and_Url == []:
        return False

    for i in range(len(title_and_Url)):
        company_name = (
            company[i]
            .find(
                "span",
                class_="yvsb870 _14uh9945e _14uh9940 k7nppw0",
            )
            .next_sibling
        )

        each_job = {
            "Job title": title_and_Url[i].text,
            "Company name": company_name.text,
            "States": loc,
            "URL": "https://www.seek.com.au" + title_and_Url[i].get("href"),
        }
        job_list.append(each_job)
    return True


# sub classification codes:
# Architects => 6282
# Developers/Programmers => 2C6287
# Database => 2C6286
# Engineering - software => 2C6290
if __name__ == "__main__":
    # The links below are according to different states to scrap the webpages.
    # SA four characters
    sa_url_part1 = "/in-All-Adelaide-SA/full-time?page="
    sa_url_part2 = "&subclassification=6282%2C6286%2C6287%2C6290"
    sa_list = ["SA", sa_url_part1, sa_url_part2]
    # WA four characters
    wa_url_part1 = "/in-Western-Australia-WA/full-time?page="
    wa_url_part2 = "&subclassification=6282%2C6286%2C6287%2C6290"
    wa_list = ["WA", wa_url_part1, wa_url_part2]
    # ACT four characters
    act_url_part1 = "/in-All-Canberra-ACT/full-time?page="
    act_url_part2 = "&subclassification=6282%2C6286%2C6287%2C6290"
    act_list = ["ACT", act_url_part1, act_url_part2]
    # QLD three characters
    qld_url_part1 = "/in-Queensland-QLD/full-time?page="
    qld_url_part2 = "&subclassification=6282%2C6286%2C6290"
    qld_list_1 = ["QLD", qld_url_part1, qld_url_part2]
    # QLD one character
    qld_url_part3 = "/in-Queensland-QLD/full-time?page="
    qld_url_part4 = "&subclassification=2C6287%2C6287"
    qld_list_2 = ["QLD", qld_url_part3, qld_url_part4]
    # VIC two characters
    vic_url_part1 = "/in-Victoria-VIC/full-time?page="
    vic_url_part2 = "&subclassification=6282%2C6286"
    vic_list_1 = ["VIC", vic_url_part1, vic_url_part2]
    # VIC one character
    vic_url_part3 = "/developers-programmers/in-Victoria-VIC/full-time?page="
    vic_list_2 = ["VIC", vic_url_part3, ""]
    # VIC one character
    vic_url_part4 = "/engineering-software/in-Victoria-VIC/full-time?page="
    vic_list_3 = ["VIC", vic_url_part4, ""]
    # NSW two characters
    nsw_url_part1 = "/in-New-South-Wales-NSW/full-time?page="
    nsw_url_part2 = "&subclassification=6282%2C6286"
    nsw_list_1 = ["NSW", nsw_url_part1, nsw_url_part2]
    # NSW one character
    nsw_url_part3 = "/developers-programmers/in-New-South-Wales-NSW/full-time?page="
    nsw_list_2 = ["NSW", nsw_url_part3, ""]
    # NSW one character
    nsw_url_part4 = "/engineering-software/in-New-South-Wales-NSW/full-time?page="
    nsw_list_3 = ["NSW", nsw_url_part4, ""]

    # sa_list = {"SA": [sa_url_part1, sa_url_part2]}

    total_url_list = [
        sa_list,
        wa_list,
        act_list,
        qld_list_1,
        qld_list_2,
        vic_list_1,
        vic_list_2,
        vic_list_3,
        nsw_list_1,
        nsw_list_2,
        nsw_list_3,
    ]
    start = time.time()
    job_list = []

    for loc, url_1, url_2 in total_url_list:
        for i in range(1, 500):
            first_stage = extract(url_1, i, url_2)
            if transform(loc, first_stage) == False:
                break

    df = pd.DataFrame(job_list)
    df.to_csv("./final_result/fulltime_jobs_url.csv")
    end = time.time()
    print("1/4")
    print((end - start) / 60)
