# Generated by Django 3.2.18 on 2024-04-29 03:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0003_rename_menu_active_knowledgebaseviewermodel_status_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryEndpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint_title', models.CharField(max_length=350, unique=True)),
                ('query_url', models.URLField(unique=True)),
                ('query_endpoint_type', models.CharField(choices=[('get', 'GET'), ('post', 'POST'), ('put', 'PUT'), ('delete', 'DELETE')], default='get', max_length=20)),
                ('endpoint_service_type', models.CharField(choices=[('search', 'SEARCH'), ('query', 'QUERY')], default='query', max_length=20)),
                ('status_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='knowledgebaseviewermodel',
            name='display_column_first',
            field=models.CharField(default=django.utils.timezone.now, help_text='The column that will be displayed when the page loads', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='knowledgebaseviewermodel',
            name='display_column_fourth',
            field=models.CharField(blank=True, help_text='The column that will be displayed when the page loads', max_length=150, unique=True),
        ),
        migrations.AddField(
            model_name='knowledgebaseviewermodel',
            name='display_column_second',
            field=models.CharField(default=django.utils.timezone.now, help_text='The column that will be displayed when the page loads', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='knowledgebaseviewermodel',
            name='display_column_third',
            field=models.CharField(default=django.utils.timezone.now, help_text='The column that will be displayed when the page loads', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='knowledgebaseviewermodel',
            name='left_side_menu_title',
            field=models.CharField(help_text='Left side menu title', max_length=350, unique=True),
        ),
    ]
