from django.contrib import admin
from estoque.models import Produto, Compra

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
  exclude = ('valor_medio',)

admin.site.register(Compra)