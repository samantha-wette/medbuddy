# MedBuddy
## _Hackbright Capstone Project_

MedBuddy is a web application that gamifies the med tracking experience to increase medication compliance.

## Features
- Add medications, herbs, and supplements to med profile from an extensive database, or add custom items
- Adopt a "Buddy" which can be viewed on every page 
- Schedule single or recurring medication doses with option for Google Calendar reminders
- Quick-Log upcoming doses on landing page; log scheduled doses or as-needed medications on Log page to include notes or specific dose amount
- Upon logging doses, earn points to purchase buddy accessories or adopt additional buddies
- Edit med list to indicate whether medications are current, daily, and/or as-needed
- Learn about products on med-list using data from [Drugs.com]
- View updated med list, doses taken, and doses missed

## Accessibility
MedBuddy is [WCAG] compliant with descriptive alt tags, extensive ARIA labeling, and full keyboard accessibility. MedBuddy was written with the VSCode Web Accessibility [extension]. MedBuddy was tested both manually and with [Access] Assistant to ensure accessibility for all users.

## Demo
Click [here] to view the MedBuddy demo video!
<br>

[![A gif of a user dynamically adding medications to MedBuddy. As the user types in the name of the medication, a drop-down bar populates with matching meds. The user can also input their own med that is not on the list. The user can indicate whether their med is taken daily, as needed, and/or currently.](https://github.com/samantha-wette/medbuddy/blob/main/static/img/gif1.gif?raw=true)]


## Tech Stack
Category | Tech
--- | --- 
**Backend** | [Python], [Flask], [Postgresql], [SQLAlchemy]
**Frontend** | [JavaScript], [HTML], [CSS], [Bootstrap], [jQuery]
**API** | Google [Calendar], [OAuth]
**Other** | [BeautifulSoup], [Jinja], [Drugs.com], [Canva]

## Installation

To begin, clone this repository to your local machine.
```sh
git clone https://github.com/samantha-wette/medbuddy.git
```

After cloning, use your CLI to navigate to the project root directory and initialize a virtual environment.
```sh
virtualenv env
source env/bin/activate
```

Once in the virtual environment, install all required depenencies.
```sh
pip3 install -r requirements.txt
```

Next, create and seed a database for the project.
```sh
python3 seed_database.py
```
Finally, start the server to launch MedBuddy.
```sh
python3 server.py
```

## Author
Samantha Wette | *[Github], [Linkedin]*


[Drugs.com]: <https://www.drugs.com/>
[Python]: <https://www.python.org/>
[Flask]: <https://flask.palletsprojects.com/en/2.1.x/>
[Postgresql]: <https://www.postgresql.org/>
[SQLAlchemy]: <https://www.sqlalchemy.org/>
[JavaScript]: <https://developer.mozilla.org/en-US/docs/Web/JavaScript>
[HTML]: <https://developer.mozilla.org/en-US/docs/Web/HTML>
[CSS]: <https://developer.mozilla.org/en-US/docs/Web/CSS>
[Bootstrap]: <https://getbootstrap.com/>
[jQuery]: <http://jquery.com>
[Calendar]: <https://developers.google.com/calendar/api>
[OAuth]: <https://developers.google.com/identity/protocols/oauth2>
[BeautifulSoup]: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
[Jinja]: <https://jinja.palletsprojects.com/en/3.1.x/>
[Github]: <https://github.com/samantha-wette>
[Linkedin]: <https://www.linkedin.com/in/samanthawette/>
[WCAG]: <https://www.w3.org/WAI/standards-guidelines/wcag/>
[extension]: <https://marketplace.visualstudio.com/items?itemName=MaxvanderSchee.web-accessibility>
[Access]: <https://chrome.google.com/webstore/detail/access-assistant/ojiighldhdmahfdnhfdebnpmlbiemdfm?hl=en-US>
[Canva]: <https://www.canva.com/>
[here]: <https://youtu.be/_NKujEak9Mg>