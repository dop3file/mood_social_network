# Generated by Django 4.0.6 on 2022-08-25 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_profile_first_name_alter_profile_surname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='interests',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.interest'),
        ),
    ]