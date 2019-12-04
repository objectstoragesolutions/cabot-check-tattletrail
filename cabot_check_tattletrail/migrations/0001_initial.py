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
                ('monitor_id', models.CharField(max_length=2000, null=False, blank=False))
            ],
            options={
                'abstract': False,
            },
            bases=('cabotapp.statuscheck',),
        ),
    ]