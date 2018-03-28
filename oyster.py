import re
import mechanize
import requests
import json
import ConfigParser
from sys import argv
from bs4 import BeautifulSoup


config = ConfigParser.ConfigParser()
config.read("config.ini")

appid = config.get("Application", 'AppId')
appkey = config.get("Application", 'AppKey')

username = config.get("Authentication", 'UserName')
password = config.get("Authentication", 'Password')


args = str(argv[1])

if (args == "balance"):
    br = mechanize.Browser()

    # Ignore robots.txt
    br.set_handle_robots(False)
    # Google demands a user-agent that isn't a robot
    br.addheaders = [('User-agent', 'Firefox')]

    br.open("https://oyster.tfl.gov.uk/oyster/entry.do")
    br.select_form(name="sign-in")
    br["UserName"] = username
    br["Password"] = password

    br.submit()
    response = br.response().read()

    soup = BeautifulSoup(response, "html.parser")

    code = str(soup.findAll("script")[5])
    matches = re.search(r"\"balance\":\"&#163;\d+\.\d{2}", code)
    print(matches.group(0)[17:])

elif(args == "status"):
    r = requests.get('https://api.tfl.gov.uk/Line/Mode/tube,dlr,overground/Status?app_id=' + appid + '&app_key=' + appkey)
    status = open("status.txt", "w+")
    pjson = json.loads(r.text)

    for obj in pjson:
        print(obj['name'] + ": ").ljust(20) + \
            obj['lineStatuses'][0]['statusSeverityDescription']
        if ('reason' in obj['lineStatuses'][0]):
            print obj['lineStatuses'][0]['reason']

    status.write(json.dumps(pjson, indent=2))
    status.close()
