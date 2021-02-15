# Generated by Django 2.2.18 on 2021-02-15 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('order', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('date', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=20)),
                ('checked', models.BooleanField()),
                ('notified', models.BooleanField()),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.List')),
            ],
        ),
    ]
