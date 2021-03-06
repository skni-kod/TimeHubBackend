# Generated by Django 4.0.4 on 2022-05-31 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RESTApi', '0002_zdjecieuzytkownika_remove_tablicaetykieta_etykieta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tablica',
            name='uzytkownicy',
        ),
        migrations.CreateModel(
            name='TablicaUzytkownik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rola_w_tablicy', models.CharField(max_length=255)),
                ('tablica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RESTApi.tablica')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
