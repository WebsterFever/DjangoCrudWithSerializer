# Generated by Django 5.0.3 on 2024-03-26 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='recipe',
            new_name='recipes',
        ),
    ]