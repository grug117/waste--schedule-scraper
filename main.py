from bs4 import BeautifulSoup
from http import cookies
from datetime import datetime

import os
import requests
import boto3
import json


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
    table = None

    soup = BeautifulSoup(html, 'html.parser')
    fieldsets = soup.find_all('fieldset')

    for fs in fieldsets:
      label = fs.find('label')

      if label and label.text == "Your next collection days are":
        tbl = fs.find('table')

        if tbl:
          table = tbl
          break

    if table is None:
      raise Exception("Could not find table of collection dates in scraped content")

    schedule_data = []

    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            # Get the text in the first column (Collection date) and remove leading and trailing whitespace
            collection_date = cols[0].text.strip()
            # Parse the collection date using the datetime module
            collection_date = datetime.strptime(collection_date, '%A, %B %d, %Y')
            # Convert the collection date to the YYYY-MM-DD format
            collection_date = collection_date.strftime('%Y-%m-%d')

            # Get the text in the second column (Bin type)
            bin_type = cols[1].text.strip()
            schedule_data.append({'collection_date': collection_date, 'bin_type': bin_type})

    if len(schedule_data) == 0:
        raise Exception('Unable to parse schedule data from table')

    return schedule_data

def upload_schedule_data_to_s3(bucket_name, data):
    s3 = boto3.resource('s3')

    # TODO: rename to be date specific
    key = datetime.now().strftime('%Y%m%d') + '.json'

    json_string = json.dumps(data)

    print(f'upload to {bucket_name}/{key}')
    s3.Object(bucket_name, key).put(Body=json_string)

def main():
    url = os.environ['URL']
    bucket_name = os.environ['BUCKET_NAME']

    session = requests.Session()
    set_session_id(session, url)

    waste_schedule_html = get_waste_schedule_raw_html(session, url)
    schedule_data = extract_schedule_data_from_html(waste_schedule_html)

    upload_schedule_data_to_s3(bucket_name, schedule_data)
