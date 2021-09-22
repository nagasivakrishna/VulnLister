# https://github.com/nagasivakrishna/VulnLister/
# Use it with precaution and do not use it extensively
# To reduce the data set building time and results reduce the page numbers on line 93
# Made with love by SivaKrishna

import requests
import time
import re
from bs4 import BeautifulSoup

metadata = []
vulns = []
redirects = []


def choose(opt):
    if opt != 1 and opt != 2:
        try:
            opt = int(input("Enter valid number: "))
            choose(opt)
        except ValueError:
            choose(opt)
    return opt


def search(names, data, red):
    search_str = input(f'''
Enter the tool/ software/ vulnerability you want to scan for. (".." to go back)
>> ''').lower()
    if search_str == '..':
        main(0)
    results = []
    for i in names:
        if re.findall(search_str, i.lower()):
            print(f"index : {names.index(i)}")
            print(f"Vuln  : {i}")
            print(f"info  : {data[names.index(i)]}")
            print(f"Link  : {red[names.index(i)]}\n\n")
    search(vulns, metadata, redirects)


def run(l, ch):
    html = requests.get(l).text
    soup = BeautifulSoup(html, 'lxml')
    redirects_obj = soup.find_all('a', class_='vulndb__result resultblock')
    rows_obj = soup.find_all('div', class_='resultblock__info-title')
    meta_data_obj = soup.find_all('div', class_='resultblock__info-meta')
    for i in range(len(rows_obj)):
        vulns.append(rows_obj[i].text.strip())
        redirects.append(f"https://www.rapid7.com{redirects_obj[i]['href']}")
        try:
            metadata.append(f"{meta_data_obj[i].text.replace(' ', '').split('|')[0].strip()}, {meta_data_obj[i].text.replace(' ', '').split('|')[1].strip()}")
        except IndexError:
            metadata.append(f"{meta_data_obj[i].text.replace(' ', '').strip()}")

    if ch == 1:
        for i in range(len(rows_obj)):
            print(f''' 
{vulns[i]}
{metadata[i]}
{redirects[i]}''')
    


def main(choice):
    link = f'https://www.rapid7.com/db/?q=&type=&page=1'
    print(f"""
----Options----
> 1 : List CVEs
> 2 : Search
""")
    ch = choose(choice)
    if ch == 1:
        n = int(input("Enter the maximum page numbers to display: "))
        page = 1
        while str(requests.get(link)) == '<Response [200]>' and page <= n:
            print()
            print("-------------------------------------------------------------------------------------------------------------")
            print(f'{str(requests.get(link))} for page {page} for {link}')
            print("-------------------------------------------------------------------------------------------------------------")
            run(link, ch)
            page += 1
            link = f"https://www.rapid7.com/db/?q=&type=&page={page}"
            time.sleep(1)
    else:
        if len(vulns) < 200:
            page = 1
            print("Working on it :)")
            time.sleep(1)
            print("Building Data SET! ....")
            time.sleep(2)
            print("takes like 10 seconds that's it >UwU<")
            while page <= 10:    # default number of pages. Edit for more or less values.
                run(link, ch)
                page += 1
                link = f"https://www.rapid7.com/db/?q=&type=&page={page}"
        search(vulns, metadata, redirects)


if __name__ == '__main__':
    choice = 0
    main(choice)
