# Generated by Django 4.1.7 on 2023-09-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_blogs'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='image',
            field=models.ImageField(default='', upload_to='blogs/'),
            preserve_default=False,
        ),
    ]
