# Generated by Django 4.0 on 2023-12-02 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_email_verified_emailverification'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailVerification',
        ),
    ]
