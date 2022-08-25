# Generated by Django 4.0.6 on 2022-08-24 15:52

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github_social_link',
            field=models.CharField(blank=True, max_length=150, null=True, validators=[core.utils.validate_github_link]),
        ),
    ]