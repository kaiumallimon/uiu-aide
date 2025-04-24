# models/tool.py
from django.db import models

class Tool(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    function_name = models.CharField(max_length=100, help_text="Name of the registered Python function used as tool handler.")

    def __str__(self):
        return self.name
