# Generated by Django 5.1.3 on 2024-11-22 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='article_image',
            new_name='post_image',
        ),
    ]