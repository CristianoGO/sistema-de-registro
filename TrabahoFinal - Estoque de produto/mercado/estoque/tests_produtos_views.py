from django.test import TestCase
from .views import * 
from .models import Produto

class ProdutoViewsAuth(TestCase):

 
    def setUp(self):
        user = User(username='nome')
        user.set_password('pass')
        user.save()

        Produto.objects.create(nome="Produto1", valor_medio=0)


    def test_redireciona_anonimo_para_login_produtos(self):
        resposta = self.client.get('/produtos', follow=True)
        self.assertRedirects(resposta, '/login/?next=/produtos/', status_code=301)
        resposta = self.client.post('/produtos', follow=True)
        self.assertRedirects(resposta, '/login/?next=/produtos/', status_code=301)


    def test_mostra_template_produtos_view(self):
        self.client.login(username='nome', password='pass')
        resposta = self.client.get('/produtos/')
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'estoque/produtos.html')


    def test_recusa_form_branco_produtos_view(self):
        self.client.login(username='nome', password='pass')
        resposta = self.client.post('/compra/', {}) 
        self.assertEqual(resposta.status_code, 302)


    def test_recusa_form_invalido_produtos_view(self):
        resposta = self.client.post('/produtos/', {'nome': ''}) 
        self.assertEqual(resposta.status_code, 302)
        

    def test_aceita_form_valido_produtos_view(self):
        self.client.login(username='nome', password='pass')
        produto = Produto.objects.first()
        resposta = self.client.post('/produtos/', {'nome': 'produtoTeste'})
        self.assertEqual(resposta.status_code, 200)
