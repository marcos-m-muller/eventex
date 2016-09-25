# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ('-created_at',), 'verbose_name': 'inscrição', 'verbose_name_plural': 'inscrições'},
        ),
        migrations.AddField(
            model_name='subscription',
            name='hashed_pk',
            field=models.CharField(max_length=256, null=True, verbose_name='hash'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='cpf',
            field=models.CharField(max_length=11, verbose_name='cpf'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='criado em'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='e-mail'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='telefone'),
        ),
    ]