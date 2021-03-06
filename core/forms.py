# -*- coding: utf-8 -*-
from django import forms
from django.forms import Form
from django.forms import ModelForm
from core.models import Dismantle
from core.models import Manufacture, Model, Person, State, Region, City
from django.contrib.localflavor.fr.forms import FRPhoneNumberField
from django.core.validators import ValidationError
import datetime 
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets 
import enums
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User

EMPTY_VALUES=[None,'',]
class CustomModelChoiceField(forms.ModelChoiceField):
    def __init__(self, check_queryset=None, *args, **kwargs):
        super(CustomModelChoiceField, self).__init__(*args, **kwargs)
        self.check_queryset = check_queryset

    def to_python(self, value):
        print( value )
        if value in EMPTY_VALUES:
            print value
            return None
            
        if self.check_queryset:
            
            self.queryset = self.check_queryset
        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{key: value})
        except (ValueError, self.queryset.model.DoesNotExist):
            raise ValidationError(self.error_messages['invalid_choice'])
        
        print( value.id, value.title )
        return value
        
class DismantleSearchForm( Form ):
    manufacture = CustomModelChoiceField( queryset=Manufacture.objects.all(), label=u'Марка автомобиля',  required=False, empty_label=u"не выбрано",  )
    model = CustomModelChoiceField( queryset=Model.objects.filter( id=0 ), check_queryset=Model.objects.all(), label=u'Модель', required=False, empty_label=u"любая модель")
    
    year = forms.ChoiceField( choices=enums.FOUNDATION_YEAR, label=u'Год автомобиля', required=False )
    car_service= forms.BooleanField( label=u'Свой автосервис', required=False )
    purchase_vehicles= forms.BooleanField( label=u'Скупка автомобилей на разборку', required=False )
    new_parts= forms.BooleanField( label=u'Наличие новых запчастей', required=False )
    contract_motor= forms.BooleanField( label=u'Специализация на контрактных двигателях', required=False )
    send_regions= forms.BooleanField( label=u'Отправка в регионы', required=False )
    local_delivery= forms.BooleanField( label=u'Местная доставка покупателю', required=False )
    
    
    #manufacture.widget.attrs["onchange"] = "setMake();"

class DismantleAddForm( ModelForm ):
    class Meta:
        model = Dismantle
    
class DismantleModelForm( Form ):
    modelid = forms.IntegerField(widget=forms.HiddenInput, required=False) 
    manufacture = CustomModelChoiceField( queryset=Manufacture.objects.all(), label=u'Марка автомобиля',  required=True, empty_label=u"не выбрано",  )
    model = CustomModelChoiceField( queryset=Model.objects.all(), check_queryset=Model.objects.all(), label=u'Модель', required=True, empty_label=u"любая модель") 
    from_year = forms.ChoiceField( choices=enums.FOUNDATION_YEAR, label=u'Год (с какого)', required=True )
    to_year = forms.ChoiceField( choices=enums.FOUNDATION_YEAR, label=u'Год (по какой)', required=True )
    representation = forms.ChoiceField( choices=enums.PERSENT_VALUE, label=u'Представленность запчастей в %', required=False )
    
    def __init__(self, *args, **kwargs):
        super(DismantleModelForm, self).__init__(*args, **kwargs)
        self.fields['manufacture'].widget.attrs['onchange'] = "DynamicModels(this);"
        
class ImageForm( Form ):
    imageid = forms.IntegerField(widget=forms.HiddenInput, required=False) 
    title = forms.CharField( max_length=250, label=u'Название', required=True )
    description = forms.CharField( widget=forms.Textarea, label=u'Описание', required=False)
    picture = forms.ImageField(label=u'Изображение', required=False )
    
class DismantleAddForm( Form ):
    dismantle_id = forms.IntegerField(widget=forms.HiddenInput) 
    title = forms.CharField( label=u'Название разборки', min_length=3, max_length=64 )
    logo  = forms.FileField( label=u'Логотип компании', required=False )
    foundation_year = forms.ChoiceField( choices=enums.FOUNDATION_YEAR, label=u'Год основания', required=False )
    state = CustomModelChoiceField( queryset=State.objects.all(), label=u'Страна' )
    region = CustomModelChoiceField( queryset=Region.objects.all(), check_queryset=Region.objects.all(), label=u'Регион', required=True )
    city = CustomModelChoiceField( queryset=City.objects.all(), check_queryset=City.objects.all(), label=u'Город', required=False )
    address = forms.CharField( label=u'Адрес', min_length=3, max_length=128 )
    
    car_service= forms.BooleanField( label=u'Свой автосервис', required=False )
    purchase_vehicles= forms.BooleanField( label=u'Скупка автомобилей на разборку', required=False )
    new_parts= forms.BooleanField( label=u'Наличие новых запчастей', required=False )
    contract_motor= forms.BooleanField( label=u'Специализация на контрактных двигателях', required=False )
    send_regions= forms.BooleanField( label=u'Отправка в регионы', required=False )
    local_delivery= forms.BooleanField( label=u'Местная доставка покупателю', required=False )
    
    schedule= forms.CharField( label=u'Режим работы', min_length=3, max_length=128, required=False )
    phone=forms.CharField( label=u'Телефон', max_length=256, min_length=6, help_text=u'Телефон')
    fax=forms.CharField( label=u'Факс', max_length=128, min_length=6, help_text=u'Факс', required=False) 
    email = forms.EmailField( label=u'E-Mail', help_text=u'Введите реальный Email адрес' )
    url = forms.URLField(label='Сайт', required=False)
    skype = forms.CharField( label=u'Скайп', min_length=3, max_length=64, required=False )
    jabber= forms.CharField( label=u'Jabber', min_length=3, max_length=64, required=False )
    icq= forms.CharField( label=u'ICQ', min_length=3, max_length=64, required=False )
    short_remark= forms.CharField( widget=forms.Textarea, label=u'Краткое описание', min_length=3, max_length=512 )
    remark= forms.CharField(widget=forms.Textarea, label=u'Подробно о разборке', required=False)
    html = forms.CharField(widget=forms.Textarea, label=u'В формате html', required=False)
    
    
class UserForm( Form ):
    login = forms.CharField( label=u'Логин', max_length=30, min_length=3, help_text=u'Выберите логин от 3 до 30 символов' )
    email = forms.EmailField( label=u'E-Mail', help_text=u'Введите реальный Email адрес' )
    username = forms.CharField( label=u'Фамилия, Имя, Отчество', max_length=128, min_length=3, help_text=u'Ваше реальное имя в формате Фамилия, Имя, Отчество')
    phone = forms.CharField( label=u'Телефон:+7(код)номер', max_length=128, min_length=6, help_text=u'Ваш мобильный телефон для связи')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserForm, self).__init__(*args, **kwargs)
    
    def clean_email(self):
        if not self.request:
            return ''
        if self.request.method == 'POST':
            user_email = self.request.POST['email'].strip()
            emails = User.objects.filter( email=user_email ).exclude( id=self.request.user.id )
            if len( emails ) !=0:
                raise forms.ValidationError("Данный email уже используется")
        else:
            user_email = ''
        return user_email
        
    def clean_login(self):
        if not self.request:
            return '' 
            
        if self.request.method == 'POST':
            user_login =  self.request.POST['login'].strip()
            logins = User.objects.filter( username=user_login ).exclude( id=self.request.user.id )
            if len( logins ) != 0:
                raise forms.ValidationError("Логин занят")
        else:
            user_login=''
            
        return user_login
        
    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data.split( ',' )) < 3:
            if len( data.split( ' ' ) ) < 3:
                raise forms.ValidationError("Введите Имя, Фамилию, Отчество через запятую")
        return data
        
    def clean_phone( self ):
        data = self.cleaned_data['phone']
        import re
        r = re.findall( '\+?\d+\s*\(\s*\d{3,}\s*\)\s*[\d\-]{5,}', data )
        if len( r ) < 1 or data == '+7(985)3027777':
            raise forms.ValidationError("Укажите телефон в правильном формате, например +7(985)3027777")
        return data

class UserProfileForm( UserForm ):
    user_balance = forms.FloatField( label=u'Баланс (RUR)', required=False )
    
class UserRegistrationForm ( UserForm ):
    password = forms.CharField( widget=forms.PasswordInput, label=u'Пароль', max_length=30, min_length=3, help_text=u'Введите пароль')
    
    
class RestorePasswordForm( Form ):
    username = forms.CharField( label=u'Логин', max_length=30, min_length=3, help_text=u'Выберите логин от 3 до 30 символов' )

class ChangePasswordForm( Form ):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        
    old_password = forms.CharField( label=u'Старый пароль', max_length=30, min_length=3, help_text=u'Старый пароль')
    new_password = forms.CharField( label=u'Новый пароль', max_length=30, min_length=3, help_text=u'Новый пароль')
    
    def clean_old_password( self ):
        if not self.request:
            return '' 
        
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect( "/login" )
        
        if self.request.method == 'POST':
            old =  self.request.POST['old_password']
            u = User.objects.get( id = self.request.user.pk )
            p = Person.objects.get( user = u )
            if p.raw_password != old:
                raise forms.ValidationError("Указан неправильный старый пароль")
            else:
                print 'Пароль верен'
        else:
            old=''
        
        print 'old = %s' % old
        return old
    
#-----------------------------
from core.models import TodoList, TodoItem  # Change as necessary
from django.forms import ModelForm
 
class TodoListForm(ModelForm):
  class Meta:
    model = TodoList
 
class TodoItemForm(ModelForm):
  class Meta:
    model = TodoItem
    exclude = ('list',)
    
    
    
    
    
    
    
    