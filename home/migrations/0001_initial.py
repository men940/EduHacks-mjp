# Generated by Django 4.1.8 on 2023-04-08 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('photo', models.ImageField(null=True, upload_to='')),
                ('description', models.TextField(blank=True, null=True)),
                ('school', models.TextField(default='school1')),
                ('update', models.DateTimeField(auto_now=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]