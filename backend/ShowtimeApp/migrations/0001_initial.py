# Generated by Django 5.1.2 on 2024-11-21 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MovieApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('showtime_id', models.AutoField(primary_key=True, serialize=False)),
                ('theater_location', models.CharField(max_length=255)),
                ('show_date', models.DateField()),
                ('show_time', models.TimeField()),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('available_seats', models.PositiveIntegerField(default=100)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtimes', to='MovieApp.movie')),
            ],
        ),
    ]
