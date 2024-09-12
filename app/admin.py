from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import ProfileUser, Plano, Filme, Avaliacao, RankingAvaliacao, Favorito, FilmeAssistido, Recomendacao, Playlist, Seguir, Grupo, AcaoGamificacao, Gamificacao

# Configurando o admin para o modelo ProfileUser
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('nome', 'sobrenome', 'foto_perfil', 'status_assinatura', 'pontos')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'sobrenome', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'nome', 'sobrenome', 'is_staff')
    search_fields = ('email', 'nome', 'sobrenome')
    ordering = ('email',)

# Registrando os modelos no admin
admin.site.register(ProfileUser, UserAdmin)
admin.site.register(Plano)
admin.site.register(Filme)
admin.site.register(Avaliacao)
admin.site.register(RankingAvaliacao)
admin.site.register(Favorito)
admin.site.register(FilmeAssistido)
admin.site.register(Recomendacao)
admin.site.register(Playlist)
admin.site.register(Seguir)
admin.site.register(Grupo)
admin.site.register(AcaoGamificacao)
admin.site.register(Gamificacao)
