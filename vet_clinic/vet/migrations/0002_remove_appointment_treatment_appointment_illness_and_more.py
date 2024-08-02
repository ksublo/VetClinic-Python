# Generated by Django 5.0.4 on 2024-05-06 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='treatment',
        ),
        migrations.AddField(
            model_name='appointment',
            name='illness',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vet.illness'),
        ),
        migrations.AddField(
            model_name='shift',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Monday', max_length=10),
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='medicines',
        ),
        migrations.AlterField(
            model_name='host',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start_time',
            field=models.TimeField(),
        ),
        migrations.DeleteModel(
            name='Treatment',
        ),
        migrations.AddField(
            model_name='appointment',
            name='medicines',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vet.medicine'),
        ),
    ]
