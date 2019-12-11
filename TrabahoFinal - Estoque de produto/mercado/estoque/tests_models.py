from django.test import TestCase
from .models import Compra, Produto
from django.contrib.auth.models import User

class CompraTests(TestCase):

    def setUp(self):
        Produto.objects.create(nome="Produto1", valor_medio=0)
        

    def test_cria_compra(self):
        produto = Produto.objects.first()
        previous_compra_count = Compra.objects.count()
        Compra.objects.create(produto=produto, valor=100, quantidade=100)
        self.assertEqual(Compra.objects.count(), previous_compra_count + 1)


    def test_valor_medio_trigger(self):
        valor1 = 500
        valor2 = 200
        quantidade = 100
        produto = Produto.objects.first()
        Compra.objects.create(produto=produto, valor=valor1, quantidade=quantidade)
        Compra.objects.create(produto=produto, valor=valor2, quantidade=quantidade)
        valor_medio_esperado = (valor1 + valor2)/(quantidade * 2)

        self.assertEqual(Produto.objects.first().valor_medio,  valor_medio_esperado)
        compra = Compra.objects.last()
        compra.valor = valor1
        compra.save()
        
        valor_medio_esperado = (valor1 * 2)/(quantidade * 2)
        self.assertEqual(Produto.objects.first().valor_medio,  valor_medio_esperado)


class ProdutoTests(TestCase):
        
    def test_cria_produto(self):
        previous_produto_count = Produto.objects.count()
        Produto.objects.create(nome="Produto1")
        self.assertEqual(Produto.objects.count(), previous_produto_count + 1)


class UserTests(TestCase):
    
    def test_cria_usuario(self):
        previous_usuario_count = User.objects.count()
        User.objects.create(username="Usuario", password="123")
        self.assertEqual(User.objects.count(), previous_usuario_count + 1)


