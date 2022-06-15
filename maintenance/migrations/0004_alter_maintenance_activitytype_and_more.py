# Generated by Django 4.0.4 on 2022-06-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0003_alter_maintenance_activitytype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='activitytype',
            field=models.ManyToManyField(blank=True, related_name='typeact', to='maintenance.typeactivities'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='tasktype',
            field=models.ManyToManyField(blank=True, related_name='typetask', to='maintenance.typetasks'),
        ),
    ]