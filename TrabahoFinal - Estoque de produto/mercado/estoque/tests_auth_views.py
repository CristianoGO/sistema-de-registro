from django.test import TestCase
from .views import * 

class AuthViewsAuth(TestCase):

    # Seta um usuário para conseguir logar.
    def setUp(self):
        user = User(username='nome')
        user.set_password('pass')
        user.save()


    def test_login_e_logout_efetuados_corretamente(self):
        resposta = self.client.post('/login/', {'username': 'nome', 'password': 'pass'}, follow=True)
        self.assertTrue(resposta.context['user'].is_authenticated)

        resposta = self.client.get('/logout/', follow=True)
        self.assertFalse(resposta.context['user'].is_authenticated)


    def test_redireciona_logado_para_home_registrar(self):
        self.client.login(username='nome', password='pass')
        resposta = self.client.get('/registrar/', follow=True)
        self.assertRedirects(resposta, '/')
        resposta = self.client.post('/registrar/', follow=True)
        self.assertRedirects(resposta, '/')


    def test_redireciona_logado_para_home_login(self):
        self.client.login(username='nome', password='pass')
        resposta = self.client.get('/login/', follow=True)
        self.assertRedirects(resposta, '/')
        resposta = self.client.post('/login/', follow=True)
        self.assertRedirects(resposta, '/')


    def test_mostra_template_login_view(self):
        # Testa a view LOGIN
        resposta = self.client.get('/login/')
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'estoque/login.html')


    def test_mostra_template_registrar_view(self):
        # Testa a view REGISTRAR
        resposta = self.client.get('/registrar/')
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'estoque/registrar.html')


    def test_recusa_form_branco_login_view(self):
        # pedido em branco
        resposta = self.client.post('/login/', {}) 
        self.assertFalse(resposta.context['user'].is_authenticated)


    def test_recusa_form_invalido_login_view(self):
        resposta = self.client.post('/login/', {'username': '', 'password': '123'}) 
        self.assertFalse(resposta.context['user'].is_authenticated)
        
    def test_aceita_form_valido_login_view(self):
        resposta = self.client.post('/login/', {'username': 'nome', 'password': 'pass'})
        self.assertRedirects(resposta, '/')
        

    def test_recusa_form_branco_registrar_view(self):
        resposta = self.client.post('/registrar/', {}) 
        self.assertEqual(resposta.status_code, 200)

    def test_recusa_form_invalido_registrar_view(self):
        resposta = self.client.post('/registrar/', {'username': '', 'password': '123', 'email': 'email@email.com'}) 
        self.assertEqual(resposta.status_code, 200)
        
    def test_aceita_form_valido_registrar_view(self):
        resposta = self.client.post('/registrar/', {'username': 'nome2', 'password': 'pass', 'email': 'email2@email.com'})
        self.assertRedirects(resposta, '/login/')