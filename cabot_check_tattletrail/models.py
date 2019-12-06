from django.db import models
from cabot.cabotapp.models import StatusCheck, StatusCheckResult
import redis as baseRedis
import json
import os
import requests

class TattletrailStatusCheck(StatusCheck):
    
    check_name = 'tattletrail'
    create_url_name = 'create-tattletrail-check'
    edit_url_name = 'update-tattletrail-check'
    duplicate_url_name = 'duplicate-tattletrail-check'
    icon_class = 'glyphicon-road'
    monitor_name = models.CharField(
        help_text=b'Monitor Name',
        null=False,
        blank=False,
        max_length=100
        )
    monitor_lifetime = models.IntegerField(
        help_text=b'Monitor interval time in seconds',
        null=False,
        blank=False
        )
    monitor_checkin = models.CharField(
        help_text=b'Checkin URL.',
        max_length=100
        )
    monitor_id = models.CharField( 
        max_length=100
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

    def findDeadProcesses(self, redisConnection, monitorId):
        deadMonitor = {}
        allKeys = self.convert(redisConnection.keys('*'))
        if monitorId in allKeys:
            monitorDetails = redisConnection.hgetall(monitorId)
            if self.monitorIsDown(self.convert(monitorDetails)):
                deadMonitor['id'] = monitorId
                deadMonitor['monitordetails'] = monitorDetails
        return deadMonitor

    def createNewMonitor(self):
        api_url = os.environ['Tattletrail_URL']
        params = {"processname": self.monitor_name,"intervaltime": self.monitor_lifetime,"subscribers": []}
        res = requests.post(url=api_url,data=params)

    def _run(self):
        result = StatusCheckResult(status_check=self)
        try:
            if '/checkin' not in self.monitor_checkin:
                responsedata = self.createNewMonitor()
                loadedResponse = json.loads(responsedata)
                self.monitor_checkin = loadedResponse['checkinurl']
                self.monitor_id = loadedResponse['monitorid']

            redisConn = baseRedis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0, password=os.environ['REDIS_PASS'])
            deadMonitors = self.findDeadProcesses(redisConn, self.monitor_id)
        except Exception as e:
            result.error = e.args
            result.succeeded = False
        else:
            if ('id' in deadMonitors):
                result.error = u"Monitor process {} is down!".format(self.monitor_id)
                result.succeeded = False
            else:
                result.succeeded = True
        return result






