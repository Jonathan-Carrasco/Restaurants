# Generated by Django 2.2 on 2019-07-19 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('timestamp', models.IntegerField()),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
    ]
