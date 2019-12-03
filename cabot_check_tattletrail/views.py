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
            'monitor_id',
            'frequency',
            'active',
            'importance',
            'debounce'
        )
        widgets = dict(**base_widgets)
        widgets.update({
            'host': forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': 'service.arachnys.com',
            })
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