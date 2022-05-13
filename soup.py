from bs4 import BeautifulSoup
import requests
import json

"""Used to scrape up-to-date A-Z medication list from drugs.com"""

def create_meds_list():
    url_suffixes = ['0-9']
    url_list = []
    med_dict = {}
    for letter in "abc":
        for last_letter in "abcdefghijklmnopqrstuvwxyz":
            suffix = f"{letter}{last_letter}"
            url_suffixes.append(suffix)

    for suffix in url_suffixes:
        url = f"https://www.drugs.com/alpha/{suffix}.html"
        url_list.append(url)
    print(url_list)
    for url in url_list:
        try:
            print(url)
            print("IN THE FOR URL IN URL LIST LOOP")
            result = requests.get(url)
            print(result)
            doc = BeautifulSoup(result.content, "html.parser")
            meds = doc.find_all(class_="ddc-list-column-2").get_text()
            print("************")
            print(meds)
            for med in meds:
                print("in for loop")
                index = index(med)
                print(index)
                print(med)
                med_dict[f"dict[{index}]"] = {}
                med_dict[f"dict[{index}]"]['med'] = med
        except:
            print(f"There are no meds at {url}")    
    print(med_dict)
    meds_dict=json.dumps(med_dict)
    with open('static/data/meds.json', 'w') as json_file:
        json.dump(med_dict, json_file)
    print('DUMPED')
    # print(type(meds_list))``
    # print(meds_list)
        # print(meds_list)
        # with open('meds.json', 'w') as json_file:
        #     #meds_list = json.dumps
        #     meds_list = json.dumps(meds_list)
        #     json_file.write(meds_list)

create_meds_list()