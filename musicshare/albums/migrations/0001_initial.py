# Generated by Django 3.2.12 on 2022-04-22 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('genre', models.CharField(choices=[('rock', 'Rock'), ('jazz', 'Jazz'), ('blues', 'Blues')], max_length=155)),
                ('popularity', models.CharField(choices=[('top', 'Top'), ('oldy', 'Oldy')], max_length=155)),
                ('artists', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='artists.artist')),
            ],
            options={
                'db_table': 'albums',
            },
        ),
    ]
