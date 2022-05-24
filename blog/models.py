from django.db import models

# Create your models here.
class Post(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150)
    imagem = models.ImageField(upload_to='imagens/')
    conteudo = models.CharField(max_length=2000)
    data_criacao = models.DateTimeField(auto_now=True)
    link = models.URLField(blank=True)

    class Meta():
        db_table = 'blog'

    def __str__(self):
        return self.titulo