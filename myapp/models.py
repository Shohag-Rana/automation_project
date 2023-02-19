from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

# Create your models here.
STATUS_CHOICES = [
    ('started', 'started'),
    ('completed', 'completed'),
]

EXCLUDED_APPS = ["django", "db", "test_case_executor", "common"]
APP_NAME_CHOICES = [
    (app, app) for app in settings.INSTALLED_APPS if not any(app.startswith(excluded) for excluded in EXCLUDED_APPS)
]
APP_NAME_CHOICES.append(("test_case_run", "test_case_run"))


class Executor(models.Model):
    status = models.CharField(max_length=500, choices=STATUS_CHOICES, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    app_name = models.CharField(max_length=1000, choices=APP_NAME_CHOICES, blank=False, null=False)
    test_case = models.TextField(unique=True, null=False, blank=False)

    def __str__(self):
        return f"{self.app_name} {self.test_case}"
