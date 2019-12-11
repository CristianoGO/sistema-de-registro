from django import forms
from .models import Produto, Compra
from django.contrib.auth.models import User

class AddProdutoForm(forms.ModelForm):
    nome = forms.CharField(label='', max_length=300, widget=forms.TextInput(attrs={'placeholder':'Digire o nome do produto'}))
    
    class Meta:
        model = Produto
        fields = ('nome',)

class CompraLevaProdutosForm(forms.ModelForm):
    produto = forms.ModelChoiceField(queryset=Produto.objects.all(), empty_label="Selecione um dos produtos", label='PRODUTO')
    quantidade = forms.IntegerField(min_value=1, label="QUANTIDADE", widget=forms.NumberInput(attrs={'placeholder': 'Quantidade'}))
    valor = forms.DecimalField(decimal_places=2, min_value=0.01, label='VALOR EM R$', widget=forms.NumberInput(attrs={'placeholder': 'Valor em R$'}))

    class Meta:
        model = Compra
        fields = ('produto','quantidade', 'valor',)
    
class UsuarioForm(forms.ModelForm):
    username = forms.CharField(label="",max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'name':'nome'}))
    email = forms.EmailField(label="",max_length=200, widget=forms.TextInput(attrs={'placeholder': 'E-mail: tianoc123@gmail.com', 'name':'email'}))    
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Senha de usuário', 'name':'senha'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=200,widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Senha de usuário'}))