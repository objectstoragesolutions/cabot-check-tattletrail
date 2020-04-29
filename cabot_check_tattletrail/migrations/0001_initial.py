from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cabotapp', '0007_statuscheckresult_consecutive_failures'),
    ]

    operations = [
        migrations.CreateModel(
            name='TattletrailStatusCheck',
            fields=[
                ('statuscheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cabotapp.StatusCheck')),
                ('monitor_name', models.CharField(max_length=250, null=False, blank=False)),
                ('monitor_lifetime', models.IntegerField(null=False, blank=False)),
                ('monitor_checkin', models.CharField(max_length=250, null=True, blank=True)),
                ('monitor_id', models.CharField(max_length=250, null=True, blank=True)),
                ('monitor_subscribers', models.CharField(max_length=250, blank=True, null=True))
            ],
            options={
                'abstract': False,
            },
            bases=('cabotapp.statuscheck',),
        ),
    ]