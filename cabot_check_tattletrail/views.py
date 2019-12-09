from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from cabot.cabotapp.models import StatusCheck
from cabot.cabotapp.views import (CheckCreateView, CheckUpdateView,
                                  StatusCheckForm, base_widgets)

from .models import TattletrailStatusCheck


class TattleTrailCheckForm(StatusCheckForm):
    symmetrical_fields = ('service_set', 'instance_set')
    class Meta:
        model = TattletrailStatusCheck
        fields = (
            'name',
            'monitor_name',
            'monitor_lifetime',
            'monitor_checkin',
            'monitor_id',
            'monitor_subscribers',
            'frequency',
            'active',
            'importance',
            'debounce'
        )
        widgets = dict(**base_widgets)
        widgets.update({
            'monitor_checkin': forms.TextInput(attrs={
                'readonly':'readonly'
                }),
            'monitor_id': forms.TextInput(attrs={
                'readonly':'readonly'
                }),
        })

class TattletrailStatusCheckView(CheckCreateView):
    model = TattletrailStatusCheck
    form_class = TattleTrailCheckForm

class TattletrailStatusCheckUpdateView(CheckUpdateView):
    model = TattletrailStatusCheck
    form_class = TattleTrailCheckForm

def duplicate_check(request, pk):
    pc = StatusCheck.objects.get(pk=pk)
    npk = pc.duplicate()
    return HttpResponseRedirect(reverse('update-tattletrail-check', kwargs={'pk': npk}))