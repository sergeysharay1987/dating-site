from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from dating_site.settings import BASE_DIR
from django.db.models import QuerySet
from .apps import MyTinderConfig
from PIL import Image
from my_tinder.models import CustomUser
from .forms import CreateClientForm
from .my_tinder_services.put_watermark import put_watermark

app_name = MyTinderConfig.name  # название приложения
watermark = 'watermark.png'  # название изображение, содержащее водяной знак
path_to_watermark = f'{BASE_DIR}/{app_name}/{watermark}'  # путь до изображения, содержащее водяной знак

menu = [{'title': 'Зарегистрироваться', 'url_name': 'registration'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    context = {'menu': menu}
    return render(request, 'my_tinder/index.html', context=context)


def registration(request):
    if request.method == 'GET':

        form = CreateClientForm()
        return render(request, 'my_tinder/registration.html', {'form': form})

    elif request.method == 'POST':

        bound_form = CreateClientForm(request.POST, request.FILES)
        if bound_form.is_valid():

            image_field: InMemoryUploadedFile = bound_form.cleaned_data['avatar']
            image = Image.open(image_field, mode='r')
            watermarked_image = put_watermark(image, path_to_watermark)
            watermarked_image.seek(0)
            file_data = {'avatar': SimpleUploadedFile(f'image.png', watermarked_image.read(),
                                                      content_type=f'image/png')}
            data = bound_form.cleaned_data
            bound_form = CreateClientForm(data, file_data)
            bound_form.save()
            return render(request, 'my_tinder/registration.html', {'form': bound_form})
        else:

            return render(request, 'my_tinder/registration.html', {'form': bound_form})


@method_decorator(decorator=login_required, name='get')
class ClientPageView(DetailView):
    model = CustomUser
    pk_url_kwarg = 'id'
    template_name = 'my_tinder/client_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f'context: {type(context["object"])}')
        client_info = {'avatar': context['object'].avatar,
                       'gender': context['object'].gender,
                       'first_name': context['object'].first_name,
                       'last_name': context['object'].last_name}
        client_email = context['object'].email
        auth_user_id = context['object'].id
        context['client_info'] = client_info
        context['client_email'] = client_email
        context['auth_user_id'] = auth_user_id
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.user.id != context['auth_user_id']:
            return redirect('client_page', id=request.user.id)
        return self.render_to_response(context)


class LoginClient(LoginView):
    template_name = 'my_tinder/login_page.html'

    def get_success_url(self):
        auth_user = self.request.user.id
        return reverse('client_page', args=[auth_user])


def logout_client(request):
    logout(request)
    return redirect('login')


# @login_required()
# def clients_page(request, id):
#     if request.method == 'GET':
#         if id == request.user.id:
#
#             auth_user = CustomUser.objects.get(id=id)
#             other_clients: QuerySet = CustomUser.objects.all()
#             other_clients = other_clients.exclude(id=auth_user.id)
#             context = {'id': id,
#                        'other_clients': other_clients}
#             return render(request, 'my_tinder/clients_page.html', context=context)
#         else:
#             return redirect('watch_clients', id=request.user.id)


@method_decorator(decorator=login_required, name='get')
class ListClientsView(ListView):
    model = CustomUser
    template_name = 'my_tinder/clients_page.html'
    pk_url_kwarg = 'id'
    context_object_name = 'other_clients'

    def get_queryset(self):
        auth_user_id = self.request.user.id
        queryset = super().get_queryset()
        queryset.exclude(pk=auth_user_id)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        print(f'request: {request.session["_auth_user_id"]}')
        context = self.get_context_data()
        print(f'context: {context[""]}')
        if request.user.id != request.session["_auth_user_id"]:
            return redirect('watch_clients', id=request.user.id)

        return self.render_to_response(context)


# Вьюха для просмотра подробной информации о другом участнике
@login_required()
def other_client_page(request, id, other_client_id):
    auth_user: CustomUser = CustomUser.objects.get(id=id)
    other_client: CustomUser = CustomUser.objects.get(id=other_client_id)
    other_client_info = {'avatar': other_client.avatar,
                         'gender': other_client.gender,
                         'first_name': other_client.first_name,
                         'last_name': other_client.last_name}

    context = {'id': id,
               'other_client_id': other_client.pk,
               'other_client_info': other_client_info,
               'other_client_email': other_client.email,
               'other_client': other_client,
               'auth_user': auth_user}

    if request.method == 'GET':

        if id == request.user.id:

            return render(request, 'my_tinder/other_client_page.html', context)
        else:
            return redirect('other_client_detail', id=request.user.id, other_client_id=other_client_id)
    if request.method == 'POST':
        # Получаем email, переданный при помощи ajax запроса
        other_client_email = request.POST.get('other_client_email')
        try:

            auth_user.customuser_set.get(email=other_client_email)

        except ObjectDoesNotExist:

            auth_user.customuser_set.add(other_client)

        else:

            pass

        return render(request, 'my_tinder/other_client_page.html', context)
