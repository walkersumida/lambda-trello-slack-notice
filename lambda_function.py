from datetime import datetime, timedelta, timezone
import sys
import os
import requests
import slackweb
import settings

def format_url(url):
    return url.rsplit('/', 1)[0]

def format_card(card):
    return "*{0}*\n {1}\n\n".format(card['name'], format_url(card['url']))

def slack_new(url):
    return slackweb.Slack(url=url)

def slack_notice(msg):
    slack = slack_new(os.environ['SLACK_WEBNOOK_URL'])
    slack.notify(text=msg, mrkdwn=True)

def is_weekday():
    day = datetime.now(timezone(timedelta(hours=+int(os.environ['TIMEZONE_HOURS'])))).strftime('%a')
    return day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

# if __name__ == '__main__': # for local debug
def lambda_handler(event, context):
    # NOTICE: a problem with CloudWatch's cron, so confirm whether it is weekday or not.
    if not is_weekday():
        sys.exit()

    url = os.environ['TRELLO_API_URL']
    slack_mention_and_title = os.environ['SLACK_MENTION_AND_TITLE'] + '\n\n'
    slack_msg_body = ''

    cards = requests.get(url).json()

    for i, card in enumerate(cards):
        slack_msg_body += format_card(card)

    if len(slack_msg_body) > 0:
        slack_notice(slack_mention_and_title + slack_msg_body)
