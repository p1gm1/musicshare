# Generated by Django 3.2.12 on 2022-04-22 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('songs', '0001_initial'),
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='songs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='songs.song'),
        ),
    ]
