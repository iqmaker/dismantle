# -*- coding: utf-8 -*-
from django import forms
from django.forms import Form
from django.forms import ModelForm
from core.models import Dismantle
from core.models import Manufacture, Model
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
    model = CustomModelChoiceField( queryset=Model.objects.filter( id=0 ), check_queryset=Model.objects.all(), label=u'Модель', required=False, empty_label=u"не выбрано")
    
    #manufacture.widget.attrs["onchange"] = "setMake();"
    
class DismantleForm( ModelForm ):
    class Meta:
        model = Dismantle