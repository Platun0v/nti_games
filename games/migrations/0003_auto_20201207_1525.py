# Generated by Django 3.1.4 on 2020-12-07 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20201205_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='talantuser',
            name='steam_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='talantuser',
            name='steam_openid',
            field=models.CharField(default='', max_length=200),
        ),
    ]
