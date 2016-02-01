rawzica - Chores reminders for workplaces
=========================================

So you have plants at your workplace. Perhaps you hold common meals on
fridays and there's dishes to be cleaned, remains to be stuffed with.
Maybe you lack a cleaning lady, and one of you has to do all the work.
Every time.

Perhaps you decide to take turns in waterning the plants, cleaning the shit up,
and taking care of similar chores. Perhaps you shift duties every other week,
keeping the chiefs in an online collaborative spreadsheet.

Rawzica can parse that (CSV) spreadsheet and send configurable daily
email reminders. 


Installing
----------
To build/install on a Debian-based GNU/Linux distro:

```bash
# Build the deb package
dpkg-buildpackage -us -uc -b
# Install the package
dpkg -i ../rawzica_*.deb
# Install its dependencies
apt-get install -f
```

To install on any POSIX-compatible system:

```bash
sudo pip install git+https://github.com/biolab/rawzica.git
```

If your _/etc/crontab_ doesn't already periodically (i.e. daily) invoke the
scripts in _/etc/cron.daily/_ (as is probably the case in Mac OS X), you may
need to set it so that it does.

Usage
-----
Configure rawzica in _/etc/rawzica.conf_. That's it.


Example
-------
Say you have a direct URL to a CSV spreadsheet (Google Sheets work well if
you use the export/download URL) in the following format:

```text
start date,name,email,chore
2015-12-10  ,Ann,a@acme.com,wash the dishes
2015-12-24 ,Bill,b@acme.com,sit on the couch all day long
2015-01-08,Cindy,c@acme.com,bring male coworkers beer
2015-01-22 ,Dave,d@acme.com,make up more shit for Ann to do
...
```

Basically, the spreadsheet is populated with chores you and your coworkers
agree upon. The `start date` field and the `email` field are mandatory,
although they may be called otherwise, others are optional, dependent on the
email template you use.

Say also you have the following _email.template_, which adheres to Python's
`str.format()` specification:

```text
Hey, {name}!

How's it going, {name}?

It's your turn this week to {chore}.

Enjoy it, {name}.

Your beloved coworkers,
```

Now, you can configure rawzica with the following _/etc/rawzica.conf_ file:

```ini
[default]
url = https://docs.google.com/spreadsheets/d/Your_GDocs_Sheet_Key/export?format=csv&gid=0
date_format = %Y-%m-%d

[csv_fields]
start_date = start date
rcpt_to = email

[smtp]
host = insecure-smtp.acme.com
mail_from = rawzica@acme.com

[template]
monday = /path/to/rawzica/template/email.template
monday_subject = rawzica chore notification
```

In the above case, email notifications will be sent out only on mondays.
You can have different notifications for different days of the week. See the
configuration file for more information.

If it's Monday, you can test the setup by running on the command line:
```bash
rawzica
```
