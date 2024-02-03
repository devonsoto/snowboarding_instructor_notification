# Snowboard instructor Notification

Being a snowboard instructor at Beaver Creek, when our schedules are updated we were not given a notification via email. This script logs into the schedule site, checks working day and off days and then emails me my schedule. The script runs daily using an AWS Lambda function that runs on a Amazon EventBridge Scheduler.

# Future Work

1. This only helps me! So I would like to create a interface where other instructors can sign up.
2. Save the schedule to a database and only send an email when there are working days added

## Getting Started

You can't really test this on your own because I would have to give you my pass number. So check the screenshot below and I'll add an ec2 instance once there's a UI for other instructors.

## Built With

- [Python](https://www.python.org/) - The scripting language
- [AWS Lambda Function](https://aws.amazon.com/pm/lambda/?gclid=Cj0KCQiAwvKtBhDrARIsAJj-kTisqgUDz5yXraRw4Z-EqFIMq8xtW5KQ1Twi_PsqlU990fXOT2t8JuQaAr9JEALw_wcB&trk=73f686c8-9606-40ad-852f-7b2bcafa68fe&sc_channel=ps&ef_id=Cj0KCQiAwvKtBhDrARIsAJj-kTisqgUDz5yXraRw4Z-EqFIMq8xtW5KQ1Twi_PsqlU990fXOT2t8JuQaAr9JEALw_wcB:G:s&s_kwcid=AL!4422!3!651212652666!e!!g!!lambda%20function!909122559!45462427876) - How I run the script
- [A dream](https://en.wikipedia.org/wiki/Dream) - One can dream

- [Resend](https://resend.com/home) - Email sending platform
