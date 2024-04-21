from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Миксин, требующий аутентификации пользователя.
    """

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            # Если raise_exception установлен в True или пользователь уже аутентифицирован,
            # просто вернуть результат базовой реализации
            return super().handle_no_permission()

        # Если пользователь не аутентифицирован, выполнить кастомные действия
        # Например, перенаправить на страницу входа
        # Получить URL для страницы входа
        login_url = reverse('users:login')

        # Получить URL, на который пользователь пытался перейти
        next_url = self.request.get_full_path()

        # Перенаправить на страницу входа с сохранением параметра next для возвращения
        return HttpResponseRedirect(f"{login_url}?next={next_url}")

class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'


class ProductCreateView(CustomLoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'category']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:home')


class ProductUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'category']

    def get_queryset(self):
        # Ограничиваем запрос только теми объектами, которые принадлежат текущему пользователю
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        new_mat = form.save(commit=False)
        new_mat.slug = slugify(new_mat.name)
        new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


class ProductDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')

    def get_queryset(self):
        # Ограничиваем запрос только теми объектами, которые принадлежат текущему пользователю
        return super().get_queryset().filter(user=self.request.user)


class ContactView(View):
    template_name = 'catalog/contact.html'

    def get(self, request):
        context = {'title': 'Контакты'}
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('emails')
        message = request.POST.get('message')
        print(f'name:{name}\nemails:{email}\nmessage:{message}')

        context = {'title': 'Контакты'}
        return render(request, self.template_name, context)