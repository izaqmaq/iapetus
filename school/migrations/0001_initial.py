# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 05:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(choices=[('1st', 'First'), ('2nd', 'Second'), ('3rd', 'Third')], default='1st', max_length=3)),
                ('opening_date', models.DateField(null=True)),
                ('closing_date', models.DateField(null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('status', models.CharField(choices=[('o', 'Current'), ('c', 'Closed')], default='o', max_length=1)),
                ('remarks', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-opening_date'],
            },
        ),
        migrations.CreateModel(
            name='ClassLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('S1', 'Standard 1'), ('S2', 'Standard 2'), ('S3', 'Standard 3'), ('S4', 'Standard 4'), ('S5', 'Standard 5'), ('S6', 'Standard 6'), ('S7', 'Standard 7'), ('S8', 'Standard 8')], max_length=2)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
            ],
            options={
                'ordering': ['level'],
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream', models.CharField(choices=[('S', 'South'), ('E', 'East'), ('N', 'North'), ('W', 'West')], max_length=1)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.ClassLevel')),
            ],
        ),
        migrations.CreateModel(
            name='ClassSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(editable=False, help_text='do not fill!', unique=True)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.AcademicSession')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Classroom')),
            ],
        ),
        migrations.CreateModel(
            name='CommonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idno', models.CharField(max_length=30, unique=True)),
                ('names', models.CharField(help_text='First Middle Surname', max_length=200)),
                ('title', models.CharField(blank=True, choices=[('MR', 'Mr.'), ('MRS', 'Mrs.'), ('MS', 'Miss.')], max_length=3)),
                ('phone', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adm_no', models.IntegerField(unique=True)),
                ('names', models.CharField(help_text='First Middle Surname', max_length=200)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('religion', models.CharField(choices=[('CHR', 'Christian'), ('MUS', 'Muslim'), ('HIN', 'Hindu')], default='CHR', max_length=3)),
                ('join_date', models.DateField()),
                ('year_in_school', models.CharField(choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'), ('5', 'Five'), ('6', 'Six'), ('7', 'Seven'), ('8', 'Eight')], default='1', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('commoninfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='school.CommonInfo')),
            ],
            bases=('school.commoninfo',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('commoninfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='school.CommonInfo')),
            ],
            bases=('school.commoninfo',),
        ),
        migrations.AddField(
            model_name='classsession',
            name='students',
            field=models.ManyToManyField(blank=True, to='school.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='academicsession',
            unique_together=set([('term', 'opening_date')]),
        ),
        migrations.AddField(
            model_name='student',
            name='parent',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='school.Parent'),
        ),
        migrations.AddField(
            model_name='classsession',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Teacher'),
        ),
    ]
