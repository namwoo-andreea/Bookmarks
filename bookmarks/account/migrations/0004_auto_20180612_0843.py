# Generated by Django 2.0.6 on 2018-06-12 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='asset/default-user.jpg', upload_to='profile/%y/%m/%d/'),
        ),
    ]
