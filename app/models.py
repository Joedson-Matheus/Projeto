from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

def user_directory_path(instance, filename):
    """
    Define o caminho do diretório para salvar a foto do perfil do usuário.
    O arquivo será salvo em MEDIA_ROOT/imagens/user_<id>/<filename>
    """
    return f'imagens/user_{instance.id}/{filename}'

def image_move_directory_path(instance, filename):
    """
    Define o caminho do diretório para salvar a foto do filme.
    O arquivo será salvo em MEDIA_ROOT/imagens/user_<id>/<filename>
    """
    return f'imagens/move_{instance.id}/{filename}'


class Plano(models.Model):
    """
    Modelo que representa um plano de assinatura.
    Contém o nome do plano, descrição, preço e permissões associadas.
    """
    nome = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class ProfileUser(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=20, default='Nome')
    sobrenome = models.CharField(max_length=20, default='Sobrenome')
    email = models.EmailField(unique=True)
    foto_perfil = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    status_assinatura = models.ForeignKey(Plano, null=True, blank=True, on_delete=models.SET_NULL)
    pontos = models.IntegerField(default=0)
    seguindo = models.ManyToManyField('self', through='Seguir', symmetrical=False, related_name='seguidores')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome']

    @property
    def total_seguidores(self):
        return self.seguidores.count()
    
    @property
    def total_seguindo(self):
        return self.seguindo.count()

    def __str__(self):
        return self.nome




class Filme(models.Model):
    """
    Modelo que representa um filme, com informações como título, gênero, descrição, disponibilidade,
    data de lançamento e relacionamento com o usuário que o criou.
    """
    titulo = models.CharField(max_length=255)
    genero = models.CharField(max_length=100)
    capa = models.ImageField(upload_to=image_move_directory_path, null=True, blank=True)
    descricao = models.TextField()
    disponibilidade = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='filmes')

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    """
    Modelo que representa uma avaliação de um filme por um usuário.
    Contém a nota (de 1 a 5), comentário, e informações de data de criação e atualização.
    """
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='avaliacoes')
    titulo = models.CharField(max_length=20, default='Sem titulo')
    comentario = models.TextField(blank=True, null=True)
    nota = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    likes = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)


class RankingAvaliacao(models.Model):
    """
    Modelo que representa o ranking de uma avaliação.
    Contém a relação da avaliação e sua posição no ranking.
    """
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='rankings')
    rank = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['avaliacao', 'rank'], name='unique_avaliacao_rank')
        ]
        ordering = ['rank']  # Ordena por rank por padrão

    def __str__(self):
        return f'Rank {self.rank}: {self.avaliacao.titulo} - {self.avaliacao.usuario.nome}'


class Favorito(models.Model):
    """
    Modelo que representa a relação de favoritos entre um usuário e um filme.
    Contém informações de data de criação.
    """
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='favoritos')
    usuario = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='favoritos')
    criado_em = models.DateTimeField(auto_now_add=True)


class FilmeAssistido(models.Model):
    """
    Modelo que representa a relação de filmes assistidos por um usuário.
    Contém informações de data de quando o filme foi assistido.
    """
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='filmes_assistidos')
    usuario = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='filmes_assistidos')
    data_assistido = models.DateTimeField(auto_now_add=True)


class Recomendacao(models.Model):
    """
    Modelo que representa a recomendação de um filme de um usuário para um amigo.
    Contém o filme, o usuário, o email do amigo, uma mensagem, e a data de criação.
    """
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='recomendacoes')
    usuario = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='recomendacoes')
    email_amigo = models.EmailField()
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)


class Playlist(models.Model):
    """
    Modelo que representa uma playlist de filmes criada por um usuário.
    Contém o nome da playlist, o usuário, os filmes na playlist, e a data de criação.
    """
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='playlists')
    filmes = models.ManyToManyField(Filme, related_name='playlists')
    criado_em = models.DateTimeField(auto_now_add=True)


class Seguir(models.Model):
    """
    Modelo que representa a relação de seguimento entre usuários.
    Contém o seguidor, o seguido, e a data de criação.
    """
    seguidor = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='seguindo_set')
    seguido = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='seguidores_set')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['seguidor', 'seguido'], name='unique_seguidor_seguido')
        ]
        verbose_name = 'Seguir'
        verbose_name_plural = 'Seguidores'

    def __str__(self):
        return f'{self.seguidor} segue {self.seguido}'


class Grupo(models.Model):
    """
    Modelo que representa um grupo de usuários.
    Contém o nome do grupo, o administrador do grupo, os membros, e a data de criação.
    """
    nome = models.CharField(max_length=255)
    admin = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='grupos_admin')
    membros = models.ManyToManyField(ProfileUser, related_name='grupos')
    criado_em = models.DateTimeField(auto_now_add=True)


class AcaoGamificacao(models.Model):
    """
    Modelo que representa uma ação de gamificação.
    Contém o nome da ação, descrição e pontos associados.
    """
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    pontos = models.IntegerField()

    def __str__(self):
        return self.nome


class Gamificacao(models.Model):
    """
    Modelo que representa a relação de gamificação entre um usuário e uma ação.
    Contém o usuário, a ação de gamificação, e a data de criação.
    """
    usuario = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='gamificacoes')
    acao = models.ForeignKey(AcaoGamificacao, on_delete=models.CASCADE, related_name='gamificacoes')
    criado_em = models.DateTimeField(auto_now_add=True)
