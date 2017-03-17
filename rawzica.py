#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import csv
from datetime import datetime
from tempfile import NamedTemporaryFile
from smtplib import SMTP
from email.mime.text import MIMEText

try:
    from urllib.request import urlopen
except ImportError:  # Py2
    from urllib2 import urlopen

try:
    from configparser import ConfigParser
except ImportError:  # Py2
    from ConfigParser import ConfigParser


__version__ = '0.2'

NOW = datetime.now()
CONFIG_FILE = '/etc/rawzica.conf'


def parse_config():
    config = ConfigParser(interpolation=None)  # Don't interpolate for date_format
    if not config.read(CONFIG_FILE):
        sys.exit('Error: Cannot read configuration file ' + CONFIG_FILE)
    return config


def download(url):
    if not url:
        sys.exit('Error: No URL specified in config file ' + CONFIG_FILE)
    try:
        with urlopen(url) as response, NamedTemporaryFile() as tmp:
            tmp.write(response.read())
            tmp.flush()
            with open(tmp.name, encoding='utf-8') as f:
                return list(csv.DictReader(f))
    except Exception as e:
        sys.exit('Error: ' + e.args[0])


def find_closest_line(data, config):
    date_format = config.get('default', 'date_format', fallback='')
    if not date_format:
        try:
            from dateutil.parser import parse as parse_date
        except ImportError:
            sys.exit('Need python-dateutil unless you configure date_format')
    else:
        def parse_date(date_string):
            return datetime.strptime(date_string, date_format)

    def start_date(line,
                   field=config.get('csv_fields', 'start_date', fallback='start_date')):
        return parse_date(line[field])

    def end_date(line,
                 field=config.get('csv_fields', 'end_date', fallback='')):
        return parse_date(line[field]) if field else datetime.max

    for line in reversed(list(data)):
        if start_date(line) <= NOW <= end_date(line):
            return line
    sys.exit('Error: No line in csv matches NOW')


def main():
    config = parse_config()
    data = download(config.get('default', 'url'))
    line = find_closest_line(data, config)

    for weekday, day in enumerate(('monday', 'tuesday', 'wednesday',
                                   'thursday', 'friday', 'saturday', 'sunday')):
        template = config.get('template', day)
        if NOW.weekday() != weekday or not template:
            continue
        with open(template) as template:
            email = MIMEText(template.read().format(**line))
        email['Subject'] = config.get('template', day + '_subject', fallback='Rawzica notification')
        email['From'] = config.get('smtp', 'mail_from', fallback='rawzica')
        email['To'] = line[config.get('csv_fields', 'rcpt_to', fallback='root@localhost')]
        print('Sending email:\n', email)
        smtp = SMTP(host=config.get('smtp', 'host', fallback=''),
                    port=config.get('smtp', 'port', fallback=0))
        smtp.send_message(email)
        smtp.quit()


if __name__ == '__main__':
    sys.exit(main())
