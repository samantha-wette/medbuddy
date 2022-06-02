# SAMANTHA WETTE - Project Pitch

A platform that incentivizes users to take their medications consistently. 

## Background

Many people need to take daily medications to take care of their health, but taking them consistently can be a struggle.

When life is busy, a phone or calendar reminder is not enough to follow through on every dose. I decided to create a platform where users of all ages are rewarded for taking their medications regularly.

## MVP

- As a user, I want to manage a personalized medication list so that I can take care of my health.
- As a user, I want to log my medication use on a regular schedule. I also want to earn points every time I log my medication use so that I am more likely to actually take my medications on time.
- As a user, I want to customize my profile with a virtual pet (sprite). I also want to be able to redeem my earned points for prizes so I can level up or customize my pet.
- As a user, I want to view my medication use data so that I can have a complete picture of my medication compliance. I also want to be able to share my data with others I choose such as caretakers and medical providers.

## Tech stack

- **Database:** PostgreSQL
- **Backend:** Python 3
- **Frontend:** Web browser

### Dependencies

- Python packages:
  - SQLAlchemy ORM
  - Flask
  - Jinja
- APIs/external data sources:
  - Google Calendar API: used to schedule medication doses
  - Drugs.com: medication and supplement data scraped with BeautifulSoup
- Browser/client-side dependencies:
  - Bootstrap
  - React

## Roadmap

### Sprint 1

- User registration and authentication
- Display username and sprite on profile
- Add and remove items to/from private medication profile
- Log medication use and update point total in profile
- Exchange points for prizes

### Sprint 2

- Drugs.com integration: return search results to enhance medication profile creation
- Google Calendar integration: set medication reminders
- Bootstrap frontend