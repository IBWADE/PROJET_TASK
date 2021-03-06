# Generated by Django 4.0.4 on 2022-06-09 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='activitytype',
            field=models.ManyToManyField(blank=True, null=True, related_name='typeact', to='maintenance.typeactivities'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='tasktype',
            field=models.ManyToManyField(blank=True, null=True, related_name='typetask', to='maintenance.typetasks'),
        ),
    ]
