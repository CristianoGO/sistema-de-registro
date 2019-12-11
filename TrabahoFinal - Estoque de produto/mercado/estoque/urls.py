from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('registrar/', views.registrar, name="registrar"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('produtos/', views.produtos, name="produtos"),
    path('compra/', views.compra, name="compra"),
    path('compra/<int:id>', views.compra_edit, name="compra_edit"),
    path('listagem_compras/', views.listagem_compras, name="listagem_compras"),
    path('deletar_compra/<int:id>', views.deletar_compra, name="deletar_compra"),
    path('enviar', views.enviar, name='enviar'),

]
