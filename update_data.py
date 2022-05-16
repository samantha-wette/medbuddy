from bs4 import BeautifulSoup
from pyparsing import dict_of
import requests
import json


def create_meds_dict():
    """Used to scrape up-to-date A-Z medication list from drugs.com"""
    meds_dict = {}
    med_list = []
    url_suffixes = ['0-9']
    url_list = []
    url_list_2 = []
    for letter in "abcdefghijklmnopqrstuvwxyz":
        for last_letter in "abcdefghijklmnopqrstuvwxyz":
            suffix = f"{letter}{last_letter}"
            url_suffixes.append(suffix)

    for suffix in url_suffixes:
        url = f"https://www.drugs.com/alpha/{suffix}.html"
        url_list.append(url)
    print(url_list)
    for url in url_list:
        try:
            result=requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            meds = doc.find(class_="ddc-list-column-2")

            for med in meds.find_all('li'):
                print(f"THE MED IS {med}")
                med_name = med.a.get_text()
                med_name = str(med_name)
                med_info = med.a.get('href')
                med_info = str(med_info)
                url = f"https://www.drugs.com{med_info}"
                url = str(url)
                med_list.append((med_name, url))
        except:
            print(f"{url} appended to url_list_2, will try again")
            url_list_2.append(url)

    for url in url_list_2:
        try:
            result=requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            meds = doc.find("div", {"id": "content"})
            meds = meds.find("ul", {"class":"ddc-list-unstyled"})
            for med in meds.find_all('li'):
                med_name = med.get_text()
                med_name = str(med_name)
                med_info = med.a.get('href')
                med_info = str(med_info)
                url = f"https://www.drugs.com{med_info}"
                url = str(url)
                med_list.append((med_name, url))
        except:
            print(f"There are no meds at {url}")
    
    print(f"The med_list is {med_list}")

    index = 0
    for med, url in med_list:
        index = index + 1
        meds_dict[index] = {'name': med, 'info': url}
    
    meds_dict=json.dumps(meds_dict)
    with open('static/data/meds.json', 'w') as json_file:
        json.dump(meds_dict, json_file)
    print('Data has been dumped into meds.json')

def delete_duplicates():
    no_duplicates = {}
    file = open('static/data/meds.json', 'r')
    json_data = json.load(file)
    dict_of_dicts = json.loads(json_data)
    print(len(dict_of_dicts))
    print("**********")
    for key, value in dict_of_dicts.items():
        if value not in no_duplicates.values():
            no_duplicates[key] = value
    meds_dict=json.dumps(no_duplicates)
    with open('static/data/meds.json', 'w') as json_file:
        json.dump(meds_dict, json_file)
    print('DUMPED')