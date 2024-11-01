# Generated by Django 5.1.2 on 2024-11-01 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('user_lastname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('photo', models.CharField(blank=True, max_length=1000, null=True)),
                ('birthdate', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='ValidationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.user')),
            ],
            options={
                'db_table': 'validation_code',
            },
        ),
    ]