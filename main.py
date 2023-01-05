from bs4 import BeautifulSoup
from http import cookies
import os
import requests


def set_session_id(session, url):
    response = session.get(url)

    if response.status_code != 200:
        raise Exception('could not get session id')

    c = cookies.SimpleCookie()
    c.load(response.request.headers['cookie'])

    session_id = c.get('ASP.NET_SessionId').value
    print(f'session_id:{session_id}')
    # ASP.NET_SessionId cookie is set on the session (requests.Session) to be used in subsequent requests


def get_waste_schedule_raw_html(session, url):
    house_num = os.environ['HOUSE_NUM']
    postcode = os.environ['POSTCODE']

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {
        'personInfo.person1.RequiredFields':'%7Cadd%7C',
        'personInfo.person1.Title': '',
        'personInfo.person1.FirstName': '',
        'personInfo.person1.LastName': '',
        'personInfo.person1.HouseNumberOrName': house_num,
        'personInfo.person1.Postcode': postcode,
        'person1_FindAddress': 'Find+address'
    }

    response = session.post(url, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception('waste schedule not found')

    return response.content

def extract_schedule_data_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

def main():
    url = os.environ['URL']
    session = requests.Session()
    set_session_id(session, url)

    waste_schedule_html = get_waste_schedule_raw_html(session, url)
    extract_schedule_data_from_html(waste_schedule_html)
