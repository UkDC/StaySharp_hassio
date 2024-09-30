import math

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from StaySharp.settings import EMAIL_HOST_USER
from info_ss.tasks import check_registration
from info_ss.utilities import info_collect
from .forms import All_knifesForm_step1, All_knifesForm_step2, Grinding_dataForm, Honing_dataForm, RegisterUserForm, \
    MyUserChangeForm
from .models import All_knifes, Account_table
from .tasks import send_email_for_varify, send_mail_fb
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages


# расчет параметров настройки станка для заточки и хонингования
class CalculationView(View):
    def get(self, request):
        return render(request, 'Calculation.html')

    def post(self, request):
        form_grinding = Grinding_dataForm(request.POST)
        form_honing = Honing_dataForm(request.POST)

        # сбор стат.информации
        info_collect(request, calculation_visits=True)

        if form_honing.is_valid():
            KJ = form_honing.cleaned_data['KJ']
            GA = form_honing.cleaned_data['GA']
            RWH = form_honing.cleaned_data['RW']
            honing_add = form_honing.cleaned_data['honing_add']
            FVB_S = form_honing.cleaned_data['FVB_S']
            C3_C4 = form_honing.cleaned_data['C3_C4']
            C5_C6 = form_honing.cleaned_data['C5_C6']

            AC = math.sqrt((KJ - 6) ** 2 + 11.9 ** 2)
            BAC = math.atan(11.9 / (KJ - 6))
            DC = math.sqrt(RWH ** 2 + AC ** 2 - 2 * RWH * AC * math.cos(math.radians(90 + GA + honing_add) - BAC))
            FC = math.sqrt(DC ** 2 - (C3_C4 + FVB_S) ** 2)
            FVB_H = FC - C5_C6 + 6

            return render(request, 'Calculation.html',
                          context={'KJ': KJ, 'GA': GA, 'RWH': RWH, 'honing_add': honing_add, 'FVB_S': FVB_S,
                                   'C3_C4': C3_C4, 'C5_C6': C5_C6, 'FVB_H': FVB_H})

        elif form_grinding.is_valid():
            KJ = form_grinding.cleaned_data['KJ']
            GA = form_grinding.cleaned_data['GA']
            RWG = form_grinding.cleaned_data['RW']
            C1 = form_grinding.cleaned_data['C1']
            C2 = form_grinding.cleaned_data['C2']

            AC = math.sqrt((KJ - 6) ** 2 + 11.9 ** 2)
            BAC = math.atan(11.9 / (KJ - 6))
            DC = math.sqrt(RWG ** 2 + AC ** 2 - 2 * RWG * AC * math.cos(math.radians(90 + GA) - BAC))
            EC = math.sqrt(DC ** 2 - C1 ** 2)
            USH = EC - C2 + 6

            return render(request, 'Calculation.html',
                          context={'KJ': KJ, 'GA': GA, 'RWG': RWG, 'C1': C1, 'C2': C2, 'USH': USH})

        return render(request, 'Calculation.html')


def main(request):
    return render(request, 'Main.html')


# feedback
def feedback(request):
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email = request.POST['email']
        message = request.POST['message']
        # send an email
        send_mail_fb.delay(
            message_name,  # subject
            message,  # message
            message_email,  # from_email
            [EMAIL_HOST_USER],  # to email
        )
        return render(request, 'Feedback.html', context={'message_name': message_name})
    return render(request, 'Feedback.html')


# выбор оптимального угла
class Choose_the_angleView(View):

    def get(self, request):
        model = All_knifes.objects.all()
        form1 = All_knifesForm_step1()
        form2 = All_knifesForm_step2()
        angle = 0
        honing_add = 0
        return render(request, 'Choose-the-angle.html',
                      context={'model': model, 'form1': form1, 'form2': form2, 'angle': angle,
                               'honing_add': honing_add})

    def post(self, request):

        angle = 0
        honing_add = 0

        # сбор стат.информации
        info_collect(request, choose_visits = True)

        # проверка на step1

        if request.POST['step'] == 'step1':
            model = All_knifes.objects.all()
            form = All_knifesForm_step1(request.POST)

            if form.is_valid():
                brand = form.cleaned_data['brand']
                series = form.cleaned_data['series']
                steel = form.cleaned_data['steel']

                if All_knifes.objects.filter(brand=brand, series=series, steel=steel):
                    knife = All_knifes.objects.filter(brand=brand, series=series, steel=steel)[
                        0]  # отображаем первый элемент из выбранных

                    return render(request, 'Choose-the-angle.html',
                                  context={'model': model, 'knife': knife, 'angle': angle, 'honing_add': honing_add,
                                           'message_step1': 'look our suggestion or'})

                elif All_knifes.objects.filter(brand=brand, brand__isnull=False):
                    angle = All_knifes.objects.filter(brand=brand).aggregate(Avg('angle'))[
                        'angle__avg']  # среднее значение из выбранных
                    honing_add = All_knifes.objects.filter(brand=brand).aggregate(Avg('honing_add'))[
                        'honing_add__avg']  # среднее значение из выбранных
                    knife = All_knifes.objects.filter(brand=brand)[0]  # отображаем первый элемент из выбранных
                    return render(request, 'Choose-the-angle.html',
                                  context={'model': model, 'knife': knife, 'angle': angle, 'honing_add': honing_add,
                                           'message_step1': 'look our suggestion or'})

                elif All_knifes.objects.filter(steel=steel, steel__isnull=False):
                    angle = All_knifes.objects.filter(steel=steel).aggregate(Avg('angle'))[
                        'angle__avg']  # среднее значение из выбранных
                    honing_add = All_knifes.objects.filter(steel=steel).aggregate(Avg('honing_add'))[
                        'honing_add__avg']  # среднее значение из выбранных
                    knife = All_knifes.objects.filter(steel=steel)[0]  # отображаем первый элемент из выбранных
                    return render(request, 'Choose-the-angle.html',
                                  context={'model': model, 'knife': knife, 'angle': angle, 'honing_add': honing_add,
                                           'message_step1': 'look our suggestion or'})

            return render(request, 'Choose-the-angle.html',
                          context={'model': model, 'angle': angle, 'honing_add': honing_add,
                                   'message_step1': 'Not found, try next step'})

        # проверка step2

        elif request.POST['step'] == 'step2':
            model = All_knifes.objects.all()
            form = All_knifesForm_step2(request.POST)
            angle = 0
            honing_add = 0
            if form.is_valid():
                carbon = form.cleaned_data['carbon']
                add = form.cleaned_data['CrMoV']
                for knife in All_knifes.objects.all():  # если есть 'carbon' и 'CrMoV' - проверка на точное совпадение
                    if knife.carbon == carbon and knife.CrMoV == add:
                        return render(request, 'Choose-the-angle.html',
                                      context={'model': model, 'knife': knife, 'add': add, 'carbon': carbon,
                                               'angle': angle, 'honing_add': honing_add,
                                               'message_step2': 'look our suggestion or'})

                if All_knifes.objects.filter(carbon__exact=carbon):  # проверка на точное совпадение по 'carbon'
                    angle = All_knifes.objects.filter(carbon__exact=carbon).aggregate(Avg('angle'))[
                        'angle__avg']  # среднее значение из выбранных
                    honing_add = All_knifes.objects.filter(carbon__exact=carbon).aggregate(Avg('honing_add'))[
                        'honing_add__avg']  # среднее значение из выбранных
                    return render(request, 'Choose-the-angle.html',
                                  context={'model': model, 'angle': angle, 'honing_add': honing_add,
                                           'carbon': carbon, 'message_step2': 'look our suggestion or'})

                elif All_knifes.objects.filter(carbon__lt=carbon + 0.08,
                                               carbon__gt=carbon - 0.08):  # если не точное совпадение выбирается из интервала
                    angle = All_knifes.objects.filter(carbon__lt=carbon + 0.08, carbon__gt=carbon - 0.08).aggregate(
                        Avg('angle'))['angle__avg']  # среднее значение из выбранных
                    honing_add = \
                        All_knifes.objects.filter(carbon__lt=carbon + 0.08, carbon__gt=carbon - 0.08).aggregate(
                            Avg('honing_add'))['honing_add__avg']  # среднее значение из выбранных
                    return render(request, 'Choose-the-angle.html',
                                  context={'model': model, 'angle': angle, 'honing_add': honing_add, 'carbon': carbon,
                                           'message_step2': 'look our suggestion or'})

                return render(request, 'Choose-the-angle.html',
                              context={'model': model, 'angle': angle, 'honing_add': honing_add, 'add': add,
                                       'carbon': carbon,
                                       'message_step2': 'Not found, try next step'})
        # проверка step3

        elif request.POST['step'] == 'step3':
            model = All_knifes.objects.all()
            if request.POST['category'] == 'low_quality':
                angle = All_knifes.objects.filter(category='low_quality').aggregate(Avg('angle'))[
                    'angle__avg']  # среднее значение из имеющихсях
                honing_add = All_knifes.objects.filter(category='low_quality').aggregate(Avg('honing_add'))[
                    'honing_add__avg']
                return render(request, 'Choose-the-angle.html',
                              context={'model': model, 'low_quality': True, 'angle': angle, 'honing_add': honing_add,
                                       'message_step3': 'look our suggestion'})

            elif request.POST['category'] == 'medium_quality':
                angle = All_knifes.objects.filter(category='medium_quality').aggregate(Avg('angle'))[
                    'angle__avg']  # среднее значение из имеющихсях
                honing_add = All_knifes.objects.filter(category='medium_quality').aggregate(Avg('honing_add'))[
                    'honing_add__avg']
                return render(request, 'Choose-the-angle.html',
                              context={'model': model, 'medium_quality': True, 'angle': angle, 'honing_add': honing_add,
                                       'message_step3': 'look our suggestion'})

            elif request.POST['category'] == 'high_quality':
                angle = All_knifes.objects.filter(category='high_quality').aggregate(Avg('angle'))[
                    'angle__avg']  # среднее значение из имеющихсях
                honing_add = All_knifes.objects.filter(category='high_quality').aggregate(Avg('honing_add'))[
                    'honing_add__avg']
                return render(request, 'Choose-the-angle.html',
                              context={'model': model, 'high_quality': True, 'angle': angle, 'honing_add': honing_add,
                                       'message_step3': 'look our suggestion'})

            elif request.POST['category'] == 'premium_quality':
                angle = All_knifes.objects.filter(category='premium_quality').aggregate(Avg('angle'))[
                    'angle__avg']  # среднее значение из имеющихсях
                honing_add = All_knifes.objects.filter(category='premium_quality').aggregate(Avg('honing_add'))[
                    'honing_add__avg']
                return render(request, 'Choose-the-angle.html',
                              context={'model': model, 'premium_quality': True, 'angle': angle,
                                       'honing_add': honing_add,
                                       'message_step3': 'look our suggestion'})

        return render(request, 'Choose-the-angle.html', context={'model': model})


# вывод таблицы с записями пользователя
class Account_tableView(TemplateView):
    template_name = 'Account-table.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        # сбор стат.информации
        info_collect(request, account_table_visits=True)

        if user and user.is_active:
            context = self.get_context_data(**kwargs)
            context['my_knifes'] = Account_table.objects.filter(user=user)
            return self.render_to_response(context)


# редактирование таблиц с записями пользователя
def account_table_edit(request):
    Account_tableFormSet = modelformset_factory(Account_table, exclude=('date',), can_delete=True)
    user = request.user
    if user and user.is_active:
        if request.method == 'POST':
            # выборка formset по user
            formset = Account_tableFormSet(request.POST, queryset=Account_table.objects.filter(user=user))
            if formset.is_valid():
                # удаление дополнительных форм-строк, в таблице,  если они не заполнены
                if not any([formset.cleaned_data[-1][value] for value in formset.cleaned_data[-1] if value != 'user']):
                    formset.cleaned_data[-1]['DELETE'] = True
                # сохранение форм
                formset.save()
                user.is_active = True
                user.save()
                return redirect('account_table')

            formset = Account_tableFormSet(queryset=Account_table.objects.filter(user=user))
            return render(request, 'Account-table_edit.html', context={'formset': formset})
        else:
            formset = Account_tableFormSet(queryset=Account_table.objects.filter(user=user))
            return render(request, 'Account-table_edit.html',
                          context={'formset': formset, 'error_messages': 'Not correct input'})
    return render(request, 'registration/login.html', context={'error': "You need to login"})


# регистрации нового пользователя с активацией через email
class RegisterFormView(CreateView):
    model = User
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')
    template_name = 'registration/Sighup.html'

    def form_valid(self, form):
        for user in User.objects.all():
            if form.cleaned_data['email'] == user.email:
                form.add_error(None, {'email': 'This email has already been registered'})
                return render(self.request, 'registration/Sighup.html', context={'form': form})
        form.save()
        # метод save() переопределен в RegisterUserForm, и устанавливает is_active = False
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)
        email = form.cleaned_data['email']
        # отправление письма для подтверждения аутентификации, функция определена в utilities.py
        send_email_for_varify(self.request, user, email)
        return render(self.request, 'registration/Sighup.html', context={'form': form, 'send_email': True})

    def form_invalid(self, form):
        return render(self.request, 'registration/Sighup.html', context={'form': form, "done": False})


# вывод - регистрация выполнена
class RegisterDoneView(TemplateView):
    template_name = 'registration/Sighup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['done'] = True
        return context


# переход по ссылке в email и активация нового пользователя
class EmailVerify(View):
    def get(self, request, uidb64, token, email):  # email передается через ссылку для активации
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.email = email  # если верификация прошла успешно, то сохраняем новый email
            user.save()
            # при удачной активации выполняется login пользователя
            login(request, user)
            return render(request, 'registration/activation_done.html')

        return render(request, 'registration/activation_done.html', context={'not_match': True})

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


# редактирование аккаунта
def edit_account(request):
    user = request.user
    init = User.objects.get(username=user.username)

    if user and user.is_active:
        if request.method == 'POST':
            form = MyUserChangeForm(request.POST, instance=init)
            if form.is_valid():
                if 'email' in form.changed_data:
                    new_email = form.cleaned_data['email']  # получение нового пароля
                    form.save()
                    username = form.cleaned_data['username']
                    user = User.objects.get(username=username)
                    user.email = form.initial['email']  # возвращаем первоначальный email, пока не будет подтверждена
                    # достоверность нового пароля
                    user.save()
                    # отправление письма для подтверждения аутентификации, функция определена в utilities.py
                    send_email_for_varify(request, user, new_email)
                    return render(request, 'registration/Edit_account.html', context={'form': form, 'send_email': True})
                elif form.changed_data:
                    form.save()
                    return render(request, 'registration/Edit_account.html', context={'form': form, 'done': True})
                return render(request, 'registration/Edit_account.html', context={'form': form, 'done': False})
            return render(request, 'registration/Edit_account.html', context={'form': form, 'done': False})
        else:
            form = MyUserChangeForm()
            return render(request, 'registration/Edit_account.html', context={'form': form, 'done': False})
    return render(request, 'registration/Edit_account.html', context={'error': "You need to login"})


# удаление аккаунта
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'registration/Edit_account.html'
    success_url = reverse_lazy('main')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        info = request.user.username + ' Deleted'
        logout(request)
        messages.add_message(request, messages.SUCCESS, info)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
