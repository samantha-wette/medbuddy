from bs4 import BeautifulSoup
import requests
import json

"""Used to scrape up-to-date A-Z medication list from drugs.com"""

def create_meds_dict():
    meds_dict = {}
    med_list = []
    url_suffixes = ['0-9']
    url_list = []
    url_list_2 = []
    for letter in "ab":
        for last_letter in "ab":
            suffix = f"{letter}{last_letter}"
            url_suffixes.append(suffix)

    for suffix in url_suffixes:
        url = f"https://www.drugs.com/alpha/{suffix}.html"
        url_list.append(url)
    print(url_list)
    for url in url_list:
        try:
            result=requests.get(url)
            print("********** got the result********")
            doc = BeautifulSoup(result.text, "html.parser")
            print("********got the doc******")
            print(doc)
            meds = doc.find(class_="ddc-list-column-2")
            # meds = doc.find("ul", {"class":"ddc-list-column-2"})

            print("got the meds")
            # print(meds)
            for med in meds.find_all('li'):
                print(f"THE MED IS {med}")
                med_name = med.a.get_text()
                med_name = str(med_name)
                print(med_name)
                med_info = med.a.get('href')
                med_info = str(med_info)
                print(med_info)
                url = f"https://www.drugs.com{med_info}"
                url = str(url)
                print(url)
                med_list.append((med_name, url))
        except:
            url_list_2.append(url)
            print(f"{url} not in that format")
    print(url_list_2)   
    print("**************") 
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
    
    print(med_list)
    index = 0
    for med, url in med_list:
        index = index + 1
        meds_dict[index] = {'name': med, 'info': url}
    
    meds_dict=json.dumps(meds_dict)
    with open('static/data/meds.json', 'w') as json_file:
        json.dump(meds_dict, json_file)
    print('DUMPED')

create_meds_dict()
    # print(type(meds_list))
    # print(meds_list)
        # print(meds_list)
        # with open('meds.json', 'w') as json_file:
        #     #meds_list = json.dumps
        #     meds_list = json.dumps(meds_list)
        #     json_file.write(meds_list)