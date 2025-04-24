# # models/agent.py
# from django.db import models
# from django.contrib.auth.models import User
# from apps.admin.tools.pdf_read_embedd.models.tool_model import Tool
#
# class Agent(models.Model):
#     name = models.CharField(max_length=100)
#     prompt_template = models.TextField(help_text="System prompt that defines agent behavior.")
#     tools = models.ManyToManyField(Tool, related_name="agents", blank=True)
#     vector_namespace = models.CharField(max_length=200, help_text="Class name or namespace for Weaviate.")
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agents")
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
