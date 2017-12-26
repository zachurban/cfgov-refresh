# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0004_auto_20160615_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=500)),
                ('slug', models.SlugField(max_length=100)),
                ('offered', models.DateField(null=True, blank=True)),
                ('withdrawn', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrepayAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.TextField(max_length=500)),
                ('size', models.IntegerField()),
                ('uri', models.URLField(max_length=500)),
                ('description', models.TextField()),
                ('offered', models.DateField(null=True, blank=True)),
                ('withdrawn', models.DateField(null=True, blank=True)),
                ('posted', models.DateField(help_text='For legacy PDFs, this is the S3 posting date; for SalesForce PDFs, this is the uploaded date', null=True)),
            ],
            options={
                'ordering': ['-posted'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrepayPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=500)),
                ('slug', models.SlugField(max_length=100)),
                ('offered', models.DateField(null=True, blank=True)),
                ('withdrawn', models.DateField(null=True, blank=True)),
                ('plan_type', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='agreement',
            options={'ordering': ['-posted']},
        ),
        migrations.AlterModelOptions(
            name='issuer',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='agreement',
            name='legacy',
            field=models.BooleanField(default=False, help_text='Marker for pre-SalesForce PDFs'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='offered',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='agreement',
            name='posted',
            field=models.DateField(help_text='For legacy PDFs, this is the S3 posting date; for SalesForce PDFs, this is the uploaded date', null=True),
        ),
        migrations.AddField(
            model_name='agreement',
            name='withdrawn',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='issuer',
            name='med_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='issuer',
            field=models.ForeignKey(to='agreements.Issuer', null=True),
        ),
        migrations.AlterField(
            model_name='issuer',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
        migrations.AddField(
            model_name='prepayplan',
            name='issuer',
            field=models.ForeignKey(to='agreements.Issuer'),
        ),
        migrations.AddField(
            model_name='prepayagreement',
            name='issuer',
            field=models.ForeignKey(to='agreements.Issuer', null=True),
        ),
        migrations.AddField(
            model_name='prepayagreement',
            name='plan',
            field=models.ForeignKey(to='agreements.PrepayPlan', null=True),
        ),
        migrations.AddField(
            model_name='creditplan',
            name='issuer',
            field=models.ForeignKey(to='agreements.Issuer'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='plan',
            field=models.ForeignKey(to='agreements.CreditPlan', null=True),
        ),
    ]
