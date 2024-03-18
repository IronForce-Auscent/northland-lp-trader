# Generated by Django 4.2.10 on 2024-03-05 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lp_trader', '0005_rename_characterdata_character_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='corp',
            name='is_npc_corp',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='pull_data',
            field=models.BooleanField(default=True),
        ),
    ]
