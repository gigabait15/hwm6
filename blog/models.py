from django.db import models

from catalog.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Cодержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    count_view = models.IntegerField(default=0, verbose_name='Количество просмотров')
    notification_sent = models.BooleanField(default=False, verbose_name='Отправлено ли сообщение')

    def __str__(self):
        return f'{self.title}  {self.created_at}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
