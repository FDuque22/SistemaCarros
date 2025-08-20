from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_assinatura = models.DateField(blank=True, null=True)
    data_expiracao = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Se data_assinatura foi informada e não tem expiração, gera +30 dias
        if self.data_assinatura and not self.data_expiracao:
            self.data_expiracao = self.data_assinatura + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.user.username}"
