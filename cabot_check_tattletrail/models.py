from django.db import models
from cabot.cabotapp.models import StatusCheck, StatusCheckResult
import json
import os
import requests

class TattletrailStatusCheck(StatusCheck):
    
    check_name = 'tattletrail'
    create_url_name = 'create-tattletrail-check'
    edit_url_name = 'update-tattletrail-check'
    duplicate_url_name = 'duplicate-tattletrail-check'
    icon_class = 'glyphicon-road'
    api_url = os.environ['Tattletrail_URL']
    monitor_name = models.CharField(
        help_text=b'Monitor Name',
        null=False,
        blank=False,
        max_length=250
        )
    monitor_lifetime = models.IntegerField(
        help_text=b'Monitor interval time in seconds',
        null=False,
        blank=False
        )
    monitor_checkin = models.CharField(
        help_text=b'Checkin URL.',
        max_length=250,
        blank=True,
        null=True
        )
    monitor_id = models.CharField(
        help_text=b'Monitor Id.',
        max_length=250,
        blank=True,
        null=True
        )
    monitor_subscribers = models.CharField(
        help_text=b'Subscribers emails, please separate them using comma.',
        max_length=250,
        blank=True,
        null=True
        )

    def convert(self, data):
        if isinstance(data, bytes): return data.decode()
        if isinstance(data, dict): return dict(map(self.convert, data.items()))
        if isinstance(data, tuple): return tuple(map(self.convert, data))
        if isinstance(data, list): return list(map(self.convert, data))
        return data

    def monitorIsDown(self, monitorDetails):
        if monitorDetails.get('IsDown') == 'True': return True
        return False

    def createNewMonitor(self):
        subscribers = []
        try:
            subscribers=self.monitor_subscribers.split(',')
        except Exception as e:
            subscribers = []

        params = {"processname": self.monitor_name,"intervaltime": int(self.monitor_lifetime),"subscribers": subscribers}
        header = self.prepareHeader()
        res = requests.post(url = self.api_url, json = params, headers = header)
        return res

    def updateMonitor(self):
        subscribers = []
        try:
            subscribers=self.monitor_subscribers.split(',')
        except Exception as e:
            subscribers = []

        params = {"processname": self.monitor_name,"intervaltime": int(self.monitor_lifetime),"subscribers": subscribers}
        header = self.prepareHeader()
        api_url_for_update = self.api_url + '/' + self.monitor_id
        requests.put(url = api_url_for_update, json = params, headers = header)

    def deleteMonitor(self):
	header = self.prepareHeader()
        api_url_for_delete = self.api_url + '/' + self.monitor_id
        requests.delete(url = api_url_for_delete, headers = header)

    def checkIfMonitorIdExists(self):
        try:
            monitor_id_exists = len(self.monitor_id)
        except Exception as e:
            responsedata = self.createNewMonitor()
            self.monitor_checkin=responsedata.json().get('checkinurl')
            self.monitor_id=responsedata.json().get('monitorid')

    def prepareHeader(self):
        auth_token = os.environ['AUTH_TOKEN']
        header = {'Authorization': 'Bearer ' + auth_token}
        return header

    def buildRawData(self, monitorData):
        resultString = u"""
                          Monitor with name {}
                          was created {}
                          but checked last time at {}""".format(monitorData.get('processName'),monitorData.get('dateOfCreation'),monitorData.get('lastCheckIn'))
        return resultString

    def findMonitor(self):
        get_url = self.api_url + '/' + self.monitor_id
        header = self.prepareHeader()
        response = requests.get(url = get_url, headers = header)
        return response

    def _run(self):
        result = StatusCheckResult(status_check=self)
        try:
            self.checkIfMonitorIdExists()
            monitorResponse = self.findMonitor()
            if (monitorResponse.status_code == 401):
                result.error = u"Cant find monitor process {} with id: {}. Probably it was deleted.".format(self.monitor_name,self.monitor_id)
                result.succeeded = False
                result.raw_data = '401 UNAUTHORIZED'
                return result
            if (monitorResponse.status_code == 404):
                result.error = u"Cant find monitor process {} with id: {}. Probably it was deleted.".format(self.monitor_name,self.monitor_id)
                result.succeeded = False
                result.raw_data = '404 NOT FOUND'
                return result
            if (monitorResponse.status_code == 200):
                monitorData = monitorResponse.json().get('monitorDetails')
                if (monitorData.get('isDown')):
                    result.error = u"Monitor process {} is down! Please checkin using URL: {}".format(self.monitor_name,self.monitor_checkin)
                    result.succeeded = False
                    result.raw_data = self.buildRawData(monitorData)
                    return result
                else:
                    result.succeeded = True
                    result.error = 'None'
                    result.raw_data = 'Monitor is alive!'
                    return result
            result.succeeded = True
            result.error = 'Unexpected response!'
            result.raw_data = u'Response code is: {}'.format(monitorResponse.status_code)
            return result
        except Exception as e:
            result.error = e.args
            result.succeeded = False
            result.raw_data = e.args
            return result

    def save(self, *args, **kwargs):
        self.updateMonitor()
        return super(StatusCheck, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.deleteMonitor()
        return super(StatusCheck, self).delete(*args, **kwargs)