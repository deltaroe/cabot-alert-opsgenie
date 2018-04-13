__author__ = '\n     ~\n    . .\n    /V\\\n   // \\\\\n  /(___)\\\n   ^ ~ ^\nd i b i t s'
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.template import Context, Template

from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from os import environ as env
import requests
import json

opsgenie_template = "Service {{ service.name }} {% if service.overall_status == service.PASSING_STATUS %}is back to normal{% else %}reporting {{ service.overall_status }} status{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}."


class OpsGenieAlert(AlertPlugin):
    name = 'OpsGenie'
    author = 'dibits'

    def send_alert(self, service, users, duty_officers):
        alert = True
        priority = 'P3'

        c = Context({
            'service': service,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
            })

        message = Template(opsgenie_template).render(c)

        if service.overall_status == service.PASSING_STATUS:
            self._close_opsgenie_alert(message=message, service=service)
        else:
            if service.overall_status == service.WARNING_STATUS:
                priority = 'P3'
            elif service.overall_status == service.ERROR_STATUS:
                priority = 'P2'
            elif service.overall_status == service.CRITICAL_STATUS:
                priority = 'P1'
            else:
                alert = False

            if not alert:
                return

            self._create_opsgenie_alert(message=message, priority=priority, service=service)

    def _create_opsgenie_alert(self, message, service, priority=0):
        opsgenie_url = 'https://api.opsgenie.com/v2/alerts'

        payload = {
            'message': message,
            'alias': service.name,
            'priority': priority,
        }
        self._send_opsgenie_alert(opsgenie_url=opsgenie_url, payload=payload)

    def _close_opsgenie_alert(self, message, service):
        opsgenie_url = 'https://api.opsgenie.com/v2/alerts/%s/close?identifierType=alias' % service.name
        self._send_opsgenie_alert(opsgenie_url=opsgenie_url)

    def _send_opsgenie_alert(self, opsgenie_url, payload={}):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'GenieKey %s' % env['OPSGENIE_KEY']
        }

        requests.post(opsgenie_url, data=json.dumps(payload), headers=headers)

class OpsGenieAlertUserData(AlertPluginUserData):
    name = "OpsGenie Plugin"
