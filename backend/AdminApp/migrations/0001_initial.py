# Generated by Django 5.1.2 on 2024-11-21 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_id', models.IntegerField()),
                ('action', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'indexes': [models.Index(fields=['admin_id'], name='AdminApp_ad_admin_i_0c36c8_idx'), models.Index(fields=['-timestamp'], name='AdminApp_ad_timesta_b7cf56_idx')],
            },
        ),
    ]
