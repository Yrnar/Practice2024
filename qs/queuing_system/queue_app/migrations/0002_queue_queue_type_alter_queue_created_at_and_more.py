# Generated by Django 5.0.6 on 2024-06-06 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queue_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='queue_type',
            field=models.CharField(choices=[('B', 'Bachelor'), ('M', 'Magistracy')], default='B', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='queue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='queue',
            name='ticket_number',
            field=models.CharField(max_length=10),
        ),
    ]