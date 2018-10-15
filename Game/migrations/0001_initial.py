# Generated by Django 2.1.2 on 2018-10-13 15:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('name', models.CharField(max_length=75, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('asset_price', models.FloatField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('quantity', models.IntegerField()),
                ('is_purchase', models.BooleanField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Game.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('liquid', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Wallet'),
        ),
    ]
