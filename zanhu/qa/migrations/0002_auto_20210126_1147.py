# Generated by Django 2.1.7 on 2021-01-26 03:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
