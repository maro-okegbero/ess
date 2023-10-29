from django.db import models

from ess.base_model import BaseModelClass
from users.models import User


class ESGProject(BaseModelClass):
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='project_logos/', blank=True, null=True)
    start_date = models.DateField()
    owner_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='esg_projects', blank=True)

    def __str__(self):
        return self.company_name


class UserTask(BaseModelClass):
    project = models.ForeignKey(ESGProject, on_delete=models.DO_NOTHING, related_name='tasks')
    responsible_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    task_name = models.CharField(max_length=200)
    schedule = models.DateField()

    def __str__(self):
        return self.task_name
