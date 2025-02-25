from django.db import models

class CepModel(models.Model):
    cep = models.CharField(max_length=9, unique=True)  # CEP (formato: 00000-000)
    cidade = models.CharField(max_length=100)          # Cidade

    def __str__(self):
        return self.cep