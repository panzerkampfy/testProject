# Generated by Django 3.1.5 on 2021-02-18 09:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
