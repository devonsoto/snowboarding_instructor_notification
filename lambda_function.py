from bs4 import BeautifulSoup
import requests
import collections
import os
import resend


# Tool to help me print out the first n lines of soup string
def printMe(str, num_lines):
    s = str.prettify()
    lines = s.split('\n')
    print('\n'.join(lines[:num_lines]))
    return

def sendEmail(working_days, off_days):
    resend.api_key = os.environ["RESEND_API_KEY"]

    if resend.api_key is None:
        raise ValueError("RESEND_API_KEY environment variable is not set.")



    # Create and the html string, seperates working days and off days
    # into two tables 
    html_str = "<html><body>"

    html_str += "<h2>Working Days</h2>"
    html_str += "<table border='1'><tr><th>Date</th><th>Activity</th></tr>"
    for day, activity in working_days.items():
        html_str += f"<tr><td>{day}</td><td>{activity}</td></tr>"
    html_str += "</table>"

    html_str += "<h2>Off Days</h2>"
    html_str += "<table border='1'><tr><th>Date</th><th>Activity</th></tr>"
    for day, activity in off_days.items():
        html_str += f"<tr><td>{day}</td><td>{activity}</td></tr>"
    html_str += "</table>"

    html_str += "</body></html>"


    # TODO: Add a check to see if there are no changes to the schedule, if there isn't do not send an email
    # probably will need a db with the previous schedule to compare to the current schedule, 
    # if working_days == None:
    #     params = {
    #         "from": "Acme <onboarding@resend.dev>",
    #         "to": ["devon@empoweringsoftware.co"],
    #         "subject": "Snowboard Instructor Schedule",
    #         "html": "<strong>No Scheldule changes!</strong>",
    #     }


    params = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["devon@empoweringsoftware.co"],
        "subject": "Snowboard Instructor Schedule",
        "html": html_str,
    }
    

    email = resend.Emails.send(params)

    if not email:
        raise ValueError(f"Failed to send email: {email.text}")
    
    return email
    
    

def login_and_scrape():
    login_url = 'https://instructor.snow.com/snow/instructorTools.asp?'
    TIMEOFF = 'V/BC Time Off (Allow Override)'
    REQUESTED_TIMEOFF = 'V/BC Time Off (No Override)'
    
    INSTRUCTOR_SNOW_PASSWORD = os.environ['INSTRUCTOR_SNOW_PASSWORD']
    INSTRUCTOR_SNOW_PASS_NUMBER = os.environ['INSTRUCTOR_SNOW_PASS_NUMBER']

    # Login credentials
    payload = {
        'passNumber': INSTRUCTOR_SNOW_PASS_NUMBER,
        'password': INSTRUCTOR_SNOW_PASSWORD,
        'rnd': 'rnd=3782839974',
        'userAction.x': '18',
        'userAction.y': '13',
        'action': 'LogIn'
    }


    s = requests.session() 
    response = s.post(login_url, data=payload)

    html_content = response._content

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the schedule table
    tables = soup.find_all('table') 
    schedule_table = tables[1]

    # get the inner tbody
    body = schedule_table.find_all('tbody')
    row = body[1].find_all('table')
    schedule_html = row[3]

    schedule_rows = schedule_html.find_all('tr')

    true_rows = []
    obj = collections.defaultdict(str)
    for row in schedule_rows:
        if 'February' in row.text:
            true_rows.append(row)
    
    for j in  range(len(true_rows)):
        dates = true_rows[j].find_all('td')[0].text
        working = true_rows[j].find_all('td')[2].text
        obj[dates] = working


    working_days = collections.defaultdict(str)
    off_days = collections.defaultdict(str)
    for key,value in obj.items():
        if value != TIMEOFF and value != REQUESTED_TIMEOFF:
            working_days[key] = value
        
        else:
            off_days[key] = value

        
    
    print('working_days', working_days)
    print('off_days', off_days)

    response = sendEmail(working_days, off_days)

    if response:
        print(response)
        return 'Email Sent'

    else: 
        print('Email Failed to Send', response)
        return 'Email Failed to Send'


def lambda_handler(event, context):

    response = login_and_scrape()
    
    return response

lambda_handler(None, None)