# -*- coding: utf-8 -*-
from django.contrib import admin
from dismantle.core.models import Contragent, Car, Model, Manufacture, CarPicture, ContragentPicture, Picture, Dismantle, DismantleModel
import os


class InlineDismantleModel(admin.TabularInline):
    model = DismantleModel
    extra = 4
    
class InlineCarPicture(admin.TabularInline):
    model = CarPicture
    extra = 2

class InlineContragentPicture(admin.TabularInline):
    model = ContragentPicture
    extra = 2
    


      
class PictureAdmin( admin.ModelAdmin ):
    list_display = (
      'title',
      'picture',
      'get_thumbnail',
      'description',
      'pub_date',
    )
    
class CarAdmin( admin.ModelAdmin ):
    list_display = ('manufacture', 'model', 'date_from', 'color', 'body_type', 'mileage', 'engine_size', 'engine_hp', 'condition', 'price', 'currency' )
    list_filter = ('manufacture', 'date_from', 'color', 'body_type', 'condition' )
    date_hierarchy = 'reg_date'
    ordering = ('-reg_date',)
    fieldsets = [   (None,               {'fields': ['manufacture', 'model', 'date_from', 'color', 
                             'color_metallic', 'body_type', 
                             'doors_count', 'mileage', 'mileage_unit', 'transmission', 
                             'car_power', 'wheel_drive' ,'hand_location',  
                             'engine_size', 'engine_hp', 'gears_count', 
                             'warranty', 'condition', 'vin', 
                             'price', 'currency', 'auction', 
                             'custome', 'remark']}),
                    ( u'Комплектация', {'fields': ['salon', 'interior', 'climate_control', 
                           'air_conditioning', 'heated_seats', 'heated_mirrors', 
                           'cruise_control', 'adjustable_steering', 'power_steering', 
                           'central_locking', 'navigation_system', 'onboard_computer', 
                           'bluetooth_handsfree', 'parktronic', 'rain_sensor', 
                           'light_sensor', 'headlamp_washer', 'xenon_headlights', 
                           'fog_lights', 'wooden', 'wheels', 'wheel_size', 
                           'tires', 'spoiler', 'hitch', 'has_ballon', 
                           'hatch', 'obscured_glass']}),
            ( u'Безопасность', { 'fields': ['antilock_brakes_abs', 'break_assist', 'traction_control_tcs', 'stability_program_esp', 'airbag'] } ),
            ( u'Противоугонное оборудование', { 'fields': ['alarm', 'satellite_alarm_system', 'immobilizer', 'castle_cat', 'locking_bonnet'] } ),
            ( u'Электропривод', { 'fields': ['mirror', 'glass', 'driver_seat', 'passenger_seat'] } ),
            ( u'Мультимедиа', { 'fields': ['cd', 'mp3', 'dvd', 'tv', 'cassette'] } ),]
    pictures = [InlineCarPicture]

from dismantle.core.models import Dismantle

class ContragentAdmin( admin.ModelAdmin ):
    list_display = ('title', 'status', 'region', 'city', 'address', )
    list_filter = ( 'title', 'reg_date', 'status', 'state' )
    date_hierarchy = 'reg_date'
    ordering = ('-reg_date',)
    fieldsets = [ (None, { 'fields':['title', 'logo', 'foundation_year', 
                                    'status', 'state', 'region', 'city', 
                                    'address', 'phone', 'fax', 'email', 
                                    'url', 'skype', 'jabber', 'icq', 
                                    'latitude', 'longitude', 'short_remark', 'remark', 'main'] }), ]                           
    inlines = [InlineContragentPicture]
    
class DismantleAdmin( ContragentAdmin ):
    list_display = ('title', 'status', 'region', 'city', 'address' )
    list_filter = ( 'title', 'reg_date', 'status', )
    date_hierarchy = 'reg_date'
    ordering = ('-reg_date',)
    fieldsets = [ (None, { 'fields':['title', 'foundation_year', 
                                    'status', 'state', 'region', 'city', 
                                    'address', 'phone', 'fax', 'email', 
                                    'url', 'skype', 'jabber', 'icq', 
                                    'latitude', 'longitude', 'schedule', 'short_remark', 'remark', 'html', 'master'] }), ]
            
    inlines= [InlineDismantleModel, InlineContragentPicture, ]

admin.site.register(Contragent, ContragentAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Picture, PictureAdmin )
admin.site.register(Dismantle, DismantleAdmin)
