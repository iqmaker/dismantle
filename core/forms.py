# -*- coding: utf-8 -*-
from django import forms
from django.forms import Form
from django.forms import ModelForm
from core.models import Dismantle
from core.models import Manufacture, Model, Person
from django.contrib.localflavor.fr.forms import FRPhoneNumberField
from django.core.validators import ValidationError

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
    
    #manufacture.widget.attrs["onchange"] = "setMake();"


class DismantleForm( ModelForm ):
    class Meta:
        model = Dismantle

class user_registration_form( Form ):
    login = forms.CharField( label=u'Логин', max_length=30, min_length=3, help_text=u'Выберите логин от 3 до 30 символов' )
    email = forms.EmailField( label=u'E-Mail', help_text=u'Введите реальный Email адрес' )
    password = forms.CharField( label=u'Пароль', max_length=30, min_length=3, help_text=u'Введите пароль')
    username = forms.CharField( label=u'Фамилия, Имя, Отчество', max_length=128, min_length=3, help_text=u'Ваше реальное имя в формате Фамилия, Имя, Отчество')
    
    
    
    
    
    
    
    
    
    
    