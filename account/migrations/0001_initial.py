# Generated by Django 3.2.9 on 2023-12-26 17:59

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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('user_icon', models.ImageField(blank=True, null=True, upload_to='user_icons/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(verbose_name=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
