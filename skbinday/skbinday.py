import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup
from collections import namedtuple
from skbinday.emailtemplate import get_email_html

BASE_URL = 'https://myaccount.stockport.gov.uk/bin-collections/show'

BinDay = namedtuple('BinDay', ('name', 'date'))


def parse_date(raw_date):
    return datetime.strptime(raw_date, '%A, %d %B %Y')


def output_week(week, html=False):
    week_output = []
    for date, bin_days in week.items():
        if html:
            week_output.append('<h3>{}</h3>'.format(date.strftime("%a %d %B %Y")))
        for bin_day in bin_days:
            if html:
                content = "{}<br>".format(bin_day.name)
            else:
                content = "{} due {}".format(bin_day.name, bin_day.date.strftime("%a %d %B %Y"))
            week_output.append(content)

    return "\n".join(week_output)


def send_notification(week, future):
    text = """
Your next bin collections

{}

{} 
    """.format(output_week(week), output_week(future))

    if len(week) == 0:
        this_week_output = '<h3 style="color: #bd2319">There are no bins due this week.</h3>' \
                         + '<p>Future bin days follow.</p>'
    else:
        this_week_output = output_week(week, True)

    html = """
<h2>Your next bin collections</h2> 

<p>{}</p>

<p>{}</p>

    """.format(this_week_output, output_week(future, True))

    html = get_email_html(html)

    send_via_mailgun(text, html)


def send_via_mailgun(text, html):
    res = requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(os.environ['MAILGUN_DOMAIN']),
        auth=("api", os.environ['MAILGUN_API_KEY']),
        data={"from": "SK Bin Day Notification Service <{}>".format(os.environ['FROM_ADDRESS']),
              "to": os.environ['SKBINDAY_RECIPIENTS'].split(','),
              "subject": "Your next bin day",
              "text": text,
              "html": html
              })

    print(res.status_code)
    print(res.text)


def add_to_week(week, index, bin_day):
    if index not in week:
        week[index] = []

    week[index].append(bin_day)


def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s


def run(urn):
    url = "{}/{}".format(BASE_URL, urn)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    bins = soup.find(class_='bin-collection')

    this_week = {}
    future = {}

    colours = ['black', 'brown', 'blue', 'green']
    for colour in colours:
        c_bin = bins.find(class_='service-item-{}'.format(colour))
        title = rchop(c_bin.find('h3').text.strip(), ' bin')
        date = c_bin.find_all('p')[1].text.strip()
        py_date = parse_date(date)

        bin_day = BinDay(title, py_date)
        index = py_date

        difference = py_date - datetime.utcnow()

        add_to = this_week if difference.days < 6 else future

        add_to_week(add_to, index, bin_day)

    future = dict(sorted(future.items()))
    send_notification(this_week, future)
