from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView
from pytils.translit import slugify
from django.core.mail import send_mail

from blog.models import Blog
from config import settings


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content')
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save()
        # проверка на условие отправки письма
        self.send_notification_email()
        return self.object

    def send_notification_email(self):
        from_email = settings.EMAIL_HOST_USER
        subject = 'Поздравляем'
        message = f'Ваша публикация {self.object.title} набрала {self.object.count_view} просмотров'
        recipient_email = settings.EMAIL_HOST_USER
        if self.object.count_view > 100 and not self.object.notification_sent:
            send_mail(subject, message, from_email, [recipient_email])
            print("Письмо успешно отправлено")

            self.object.notification_sent = True
            self.object.save()

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_view', args=[self.kwargs.get('pk')])

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog')
