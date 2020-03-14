# Generated by Django 2.2.10 on 2020-03-14 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userinfo_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='project_id',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]