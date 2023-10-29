# Generated by Django 3.2.22 on 2023-10-29 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('esg_projects', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertask',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tasks', to='esg_projects.esgproject'),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='responsible_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]