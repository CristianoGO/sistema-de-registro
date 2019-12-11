from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=300)
    valor_medio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    def __str__(self):
        return self.nome

class Compra(models.Model):
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.1)])
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.quantidade, self.produto.nome)

    # Sobrescreve o método do modelo save() para calcular o valor_medio automaticamente.
    def save(self, *args, **kwargs):
        quantidade_total = 0
        valor_total = 0

        super(Compra, self).save(*args, **kwargs)
        
        # Compras relacionadas
        compras = Compra.objects.filter(produto=self.produto).aggregate(Sum('quantidade'), Sum('valor'))

        if compras['quantidade__sum'] is not None:
            quantidade_total += compras['quantidade__sum']
            valor_total += compras['valor__sum']
        
        novo_valor_medio = valor_total / quantidade_total
        produto = self.produto
        produto.valor_medio = novo_valor_medio
        produto.save()
