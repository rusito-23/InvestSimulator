# Generated by Django 2.1.2 on 2018-10-13 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=75, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='liquid',
            field=models.FloatField(default=10000),
        ),
        migrations.AddField(
            model_name='ownership',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Asset'),
        ),
        migrations.AddField(
            model_name='ownership',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Wallet'),
        ),
        migrations.AddField(
            model_name='wallet',
            name='assets',
            field=models.ManyToManyField(through='Game.Ownership', to='Game.Asset'),
        ),
    ]
