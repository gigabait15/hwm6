# Generated by Django 5.0.3 on 2024-03-04 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Cодержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Изображение')),
                ('slug', models.CharField(blank=True, max_length=100, null=True, verbose_name='slug')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_published', models.BooleanField(default=True, verbose_name='Признак публикации')),
                ('count_view', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('notification_sent', models.BooleanField(default=False, verbose_name='Отправлено ли сообщение')),
            ],
            options={
                'verbose_name': 'блог',
                'verbose_name_plural': 'блоги',
            },
        ),
    ]
