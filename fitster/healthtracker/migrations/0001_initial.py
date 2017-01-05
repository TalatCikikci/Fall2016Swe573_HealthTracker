# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 00:21
from __future__ import unicode_literals

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
            name='Itemcalories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_calories', models.DecimalField(decimal_places=1, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Itemnutrients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_nutrientdict', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipeitems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_ndbno', models.IntegerField()),
                ('item_quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Userhistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_no', models.IntegerField()),
                ('item_name', models.CharField(max_length=200)),
                ('item_quantity', models.IntegerField()),
                ('item_unit', models.CharField(max_length=50)),
                ('item_unit_modifier', models.DecimalField(decimal_places=1, max_digits=6)),
                ('item_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateofbirth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('height', models.PositiveIntegerField(help_text='Measured in (cm)')),
                ('weight', models.PositiveIntegerField(help_text='Measured in (kg)')),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Userrecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recipeitems',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthtracker.Userrecipe'),
        ),
        migrations.AddField(
            model_name='itemnutrients',
            name='history_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthtracker.Userhistory'),
        ),
        migrations.AddField(
            model_name='itemcalories',
            name='history_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healthtracker.Userhistory'),
        ),
    ]
