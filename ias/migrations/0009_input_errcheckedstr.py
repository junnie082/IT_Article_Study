# Generated by Django 5.0 on 2024-04-04 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ias', '0008_article_voter_input_voter_alter_article_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='errCheckedStr',
            field=models.TextField(null=True),
        ),
    ]