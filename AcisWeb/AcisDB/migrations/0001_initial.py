# Generated by Django 2.1 on 2018-12-20 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Erds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('erd_id', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('product_priority', models.CharField(max_length=10)),
                ('author', models.CharField(max_length=20)),
                ('HLD', models.TextField()),
                ('version', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('l1_jira', models.CharField(max_length=20)),
                ('l2_jira', models.CharField(max_length=20)),
                ('bug_jiras', models.TextField()),
                ('platform', models.CharField(max_length=20)),
                ('workload', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TestCases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_name', models.CharField(max_length=50)),
                ('age', models.DateTimeField()),
                ('erd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AcisDB.Erds')),
            ],
        ),
        migrations.CreateModel(
            name='TestReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_result', models.CharField(max_length=10)),
                ('test_log', models.TextField()),
                ('report_path', models.TextField()),
                ('fw_version', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AcisDB.TestCases')),
            ],
        ),
    ]
