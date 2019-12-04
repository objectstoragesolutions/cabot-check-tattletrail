from django.db import models
from cabot.cabotapp.models import StatusCheck, StatusCheckResult
import redis as baseRedis
import json
import os

class TattletrailStatusCheck(StatusCheck):
    check_name = 'tattletrail'
    create_url_name = 'create-tattletrail-check'
    edit_url_name = 'update-tattletrail-check'
    duplicate_url_name = 'duplicate-tattletrail-check'
    icon_class = 'glyphicon-road'
    monitor_id = models.CharField(
        help_text=b'Monitor ID to check.',
        null=False,
        blank=False,
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

    def _run(self):
        result = StatusCheckResult(status_check=self)
        try:
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






