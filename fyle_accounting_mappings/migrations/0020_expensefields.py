# Generated by Django 3.1.14 on 2023-02-21 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0023_auto_20221213_0857'),
        ('fyle_accounting_mappings', '0019_auto_20230105_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseFields',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attribute_type', models.CharField(help_text='Attribute Type', max_length=255, null=True)),
                ('source_field_id', models.IntegerField(help_text='Field ID', max_length=255, null=True)),
                ('is_enabled', models.BooleanField(default=False, help_text='Is the field Enabled')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at datetime')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at datetime')),
                ('workspace', models.ForeignKey(help_text='Reference to Workspace model', on_delete=django.db.models.deletion.PROTECT, to='workspaces.workspace')),
            ],
            options={
                'db_table': 'expense_fields',
            },
        ),
    ]
