#!/usr/bin/env python

import scraperwiki
import requests
import re
import dateutil.parser
from BeautifulSoup import BeautifulSoup
from datetime import datetime, date, timedelta

# Let's focus on zoning and planning committee at first
html = requests.get('http://www.ci.minneapolis.mn.us/meetings/zp/WCMS1P-120286')
html = BeautifulSoup(html.text)
main = html.find('div', id = 'maincontent')

# Get data about the meeting
meeting_data = {}
meeting_data['committee'] = main.find('h1').getText()
meeting_data['committee_id'] = re.sub('[^0-9a-zA-Z]+', '', meeting_data['committee'].lower())
meeting_data['meeting_type'] = main.find('p', 'MeetingName').getText()
# Details
meeting_details = main.findAll('p', '2MeetingDetails')
meeting_data['date'] = dateutil.parser.parse(meeting_details[0].getText()).date()
meeting_data['time'] = meeting_details[1].getText().split('-', 1)[0].strip()
meeting_data['place'] = meeting_details[1].getText().split('-', 1)[1].strip()
# Who was there
meeting_members = main.findAll('p', '2CommitteeMembers')
present_search = re.search('Commissioners present: ([.*]).*?([0-9]*)', meeting_members[0].getText())
meeting_data['present'] = present_search.group(0) if present_search is not None else None



print meeting_data


# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
