# Generated by Django 2.0.2 on 2018-02-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='aws_group',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
