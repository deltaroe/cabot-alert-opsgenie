Cabot OpsGenie Plugin
=====

This plugin allows you to send alerts to [OpsGenie](http://opsgenie.com) from [Cabot](http://cabotapp.com/). It needs an app API key, and user/group IDs for each user.
Based on [cabot-alert-pushover](https://github.com/packetcollision/cabot-alert-pushover) plugin.

Installation
----
1. Activate the Cabot venv
2. Run `pip install git+git://github.com/dibits/cabot-alert-opsgenie.git`
3. Add cabot_alert_opsgenie==0.0.1 to the CABOT_PLUGINS_ENABLED list in *\<environment\>*.env
4. Add `OPSGENIE_KEY=<YOUR_OPSGENIE_KEY>`
5. Stop Cabot
6. Run `foreman run python manage.py syncdb`
7. Start Cabot.
