# employee/models.py

from django.db import models

FIELD_TYPES = [
    ('text', 'Text'),
    ('number', 'Number'),
    ('date', 'Date'),
    ('password', 'Password'),
]

class CustomForm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FormField(models.Model):
    form = models.ForeignKey(CustomForm, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class EmployeeData(models.Model):
    form = models.ForeignKey(CustomForm, on_delete=models.CASCADE)
    data = models.JSONField()  # Stores form input values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Employee #{self.id}"