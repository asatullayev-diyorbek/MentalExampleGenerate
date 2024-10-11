from django.contrib.auth.models import User
from django.db import models


class Generate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    file_html = models.FileField(upload_to='generate/renders/html/')
    file_pdf = models.FileField(upload_to='generate/renders/pdf/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + self.created.strftime('%d/%m/%Y, %H:%M:%S')

    class Meta:
        verbose_name = "Generatsiya"
        verbose_name_plural = "Generatsiyalar"