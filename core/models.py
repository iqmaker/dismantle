# -*- coding: utf-8 -*-
from django.db import models
import os
import settings
import Image
from django.template import Library
from django import template
from enums import *
from django.contrib.auth.models import User
import inspect
import re

def DBOUT( obj ):
    """Returns the current line number in our program."""
    print ">>>>>>>>>>>>>>>>>>: ", obj, ' LINE:', inspect.currentframe().f_back.f_lineno
    
register = Library()

baloon_data = open( settings.TEMPLATE_DIRS[0] + 'core/baloon.html', 'r' ).read()

def get_baloon_template():
    return baloon_data
    
def thumbnail(file, size='200x200'):
    x, y = [int(x) for x in size.split('x')]
    
    #defining the filename and the miniature filename
    basename, format = file.rsplit('.', 1)
    miniature = basename + '_' + size + '.' +  format
    miniature_filename = os.path.join(settings.MEDIA_ROOT, miniature)
    miniature_url = os.path.join(settings.MEDIA_URL, miniature)
    
    # if the picture wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        print '>>> debug: resizing the picture to the format %s!' % size
        filename = os.path.join(settings.MEDIA_ROOT, file)
        picture = Image.open(filename)
        picture.thumbnail([x, y]) # generate a 200x200 thumbnail
        picture.save(miniature_filename, picture.format)
    return miniature_url

register.filter(thumbnail)

class Person( models.Model ):
    user = models.OneToOneField( User )
    second_name = models.CharField( max_length=30, verbose_name=u'Отчество', blank=True, null=True )
    raw_password = models.CharField( max_length=128, verbose_name=u''  )
    birth_date = models.DateField( verbose_name=u'Дата рождения', blank=True, null=True )
    
    user_balance = models.FloatField( verbose_name=u'Сумма счета (руб)' )   
    reg_date = models.DateField( verbose_name=u'Дата регистрации', auto_now_add=True )
    status = models.IntegerField( choices=CONTACT_STATUS, verbose_name=u'Статус' )
    
    phone = models.CharField( max_length = 128, verbose_name=u'Телефон', blank=True, null=True )
    remark = models.TextField( verbose_name=u'Описание', blank=True, null=True )
    
    
    
class Manufacture( models.Model ):
    title = models.CharField( max_length=64, verbose_name=u'Название' )
    ru_title = models.CharField( max_length=64, verbose_name=u'Русскоязычное название', blank=True, null=True )
    
    def __unicode__(self):
        return self.title
      
    class Meta:
        verbose_name = u"Марка"
    
    def file_name( self ):
        fname = re.sub( '\.|\-|\(|\)', ' ', self.title ).strip().lower().split()
        fname = '_'.join( fname )
        return fname
        
    def url_name( self ):
        return self.file_name().replace( '_', '-' )
        
    def logo_location( self, size ):
        location = os.path.join( settings.MEDIA_ROOT, 'images/manufactures' )
        location = os.path.join( location, size )
        location = os.path.join( location, self.file_name() + '.png' )
        return location
        
    def logo_url( self, size ):
        location = os.path.join( settings.MEDIA_URL, 'images/manufactures' )
        location = os.path.join( location, size )
        location = os.path.join( location, self.file_name() + '.png' ) 
        return location
      
    def logo_url_mini( self ):
        return self.logo_url( 'mini' )
        
    def logo_url_small( self ):
        return self.logo_url( 'small' )
        
    def logo_root_mini( self ):
        return self.logo_location( 'mini')
        
    def render_picture( self, filename ):
        picture_path = os.path.join(settings.MEDIA_URL, filename )
        picture_path = picture_path.replace('\\','/') # Windows-Fix
        result = '<img src="%s"/></a>' % picture_path
        return result
      
    def get_thumbnail(self):
        return self.render_picture( self.logo_url_mini() )
    
    get_thumbnail.short_description = 'Логотип'
    get_thumbnail.allow_tags = True
        

class Model( models.Model ):
    manufacture = models.ForeignKey( Manufacture, verbose_name=u'Марка' )
    title = models.CharField( max_length=64, verbose_name=u'Название' )
    ru_title = models.CharField( max_length=64, verbose_name=u'Русскоязычное название', blank=True, null=True  )
    
    def file_name( self ):
        fname = re.sub( '\.|\-|\(|\)', ' ', self.title ).strip().lower().split()
        fname = '_'.join( fname )
        return fname
        
    def url_name( self ):
        return self.file_name().replace( '_', '-' )
        
    def __unicode__(self):
      return self.title
      
    class Meta:
      verbose_name = u"Модель"

class State( models.Model ):
    title = models.CharField( max_length=32, verbose_name=u'Название' )
    
    def __unicode__(self):
      return self.title
      
    class Meta:
      verbose_name = u"Страна"

class Region( models.Model ):
    title = models.CharField( max_length=32, verbose_name=u'Название' )
    state = models.ForeignKey( State, verbose_name=u'Страна' )
    ru_title = models.CharField( max_length=64, verbose_name=u'Русскоязычное название' )
    
    def file_name( self ):
        fname = re.sub( '\.|\-|\(|\)', ' ', self.title ).strip().lower().split()
        fname = '_'.join( fname )
        return fname

    def url_name( self ):
        return self.file_name().replace( '_', '-' )
        
    def __unicode__(self):
      return self.title
      
    class Meta:
      verbose_name = u"Регион"

class City( models.Model ):
    title = models.CharField( max_length=32, verbose_name=u'Название' )
    ru_title = models.CharField( max_length=64, verbose_name=u'Русскоязычное название' )
    region = models.ForeignKey( Region, verbose_name=u'Регион' )
    state = models.ForeignKey( State, verbose_name=u'Страна' )
    regional_center = models.BooleanField(  verbose_name=u'Региональный центр' )
    latitude = models.FloatField( verbose_name=u'Широта', blank=True, null=True )
    longitude = models.FloatField( verbose_name=u'Долгота', blank=True, null=True ) 
    
    def dot_latitude( self ):
        return str(self.latitude)
        
    def dot_longitude( self ):
        return str(self.longitude)
        
    def __unicode__(self):
      return self.title

    def file_name( self ):
        fname = re.sub( '\.|\-|\(|\)', ' ', self.title ).strip().lower().split()
        fname = '_'.join( fname )
        return fname

    def url_name( self ):
        return self.file_name().replace( '_', '-' )
        
    class Meta:
      verbose_name = u"Город"

class Picture( models.Model ):
    title = models.CharField( max_length=250, verbose_name=u'Название' )
    description = models.TextField('Описание', blank=True)
    pub_date = models.DateTimeField(verbose_name=u'Дата публикации', auto_now_add=True)
    picture = models.ImageField(verbose_name=u'Изображение', upload_to='pictures', max_length=250 )

    def get_picture_filename(self):
      return os.path.join(settings.MEDIA_ROOT, self.str(picture) )

    def get_picture_url(self):
      return os.path.join(settings.MEDIA_URL, self.str(picture) )
    
    def render_picture( self, filename ):
      picture_path = os.path.join(settings.MEDIA_URL, filename )
      picture_path = picture_path.replace('\\','/') # Windows-Fix
      result = '<a href="'+ str(self.id) +'/"><img src="'+ str(picture_path) +'"/></a>'  
      return result
      
    def get_thumbnail(self):
      try:
        thump_path = thumbnail( str(self.picture), '160x160')
      except Exception, e:
        print e
      return self.render_picture( thump_path )
    
    get_thumbnail.short_description = 'Миниатюра'
    get_thumbnail.allow_tags = True
    
    def preview_picture_url(self):
      return self.render_picture( str(self.picture.url) )
    
    preview_picture_url.short_description = 'Миниатюра'
    preview_picture_url.allow_tags = True
    
    def __unicode__(self):
      return self.title
    
    class Meta:
      verbose_name = u"Изображение"

        
    
class Car( models.Model ):
    manufacture = models.ForeignKey( Manufacture, verbose_name=u'Марка' )
    model = models.ForeignKey( Model, verbose_name=u'Модель' )
    date_from = models.DateField( verbose_name=u'Дата выпуска' )
    reg_date = models.DateField( verbose_name=u'Дата регистрации',auto_now_add=True )
    color = models.IntegerField( choices=COLOR,  verbose_name=u'Цвет' )
    color_metallic = models.BooleanField(  verbose_name=u'Металлик' )
    body_type = models.IntegerField( choices=BODY_TYPE,  verbose_name=u'Тип кузова' )
    doors_count = models.IntegerField( choices=DOORS_COUNT,  verbose_name=u'Количество дверей', blank=True, null=True )

    
    transmission = models.IntegerField( verbose_name=u'Коробка передач', blank=True, null=True, choices=KPP_TYPE )
    car_power = models.IntegerField( verbose_name=u'Двигатель', blank=True, null=True, choices=CAR_POWER )
    wheel_drive = models.IntegerField( verbose_name=u'Привод', blank=True, null=True, choices=WHEEL_DRIVE )
    hand_location = models.IntegerField( verbose_name=u'Расположение руля', blank=True, null=True, choices=HAND_LOCATION )
    
    mileage = models.IntegerField(  verbose_name=u'Пробег', blank=True, null=True )    
    mileage_unit = models.IntegerField( choices=MILEAGE_UNIT,  verbose_name=u'', blank=True, null=True )
    engine_size = models.IntegerField(  verbose_name=u'Объем двигателя (см^3)', blank=True, null=True )
    engine_hp = models.IntegerField(  verbose_name=u'Мощность двигателя (hp)', blank=True, null=True )
    gears_count = models.IntegerField(  verbose_name=u'Количество передач', blank=True, null=True )
    warranty = models.IntegerField( choices=WARRANTY,  verbose_name=u'Гарантия', blank=True, null=True )
    condition = models.IntegerField( choices=CONDITION,  verbose_name=u'Состояние', blank=True, null=True )
    vin = models.CharField( max_length=32,  verbose_name=u'Vin', blank=True, null=True )
    price = models.FloatField(  verbose_name=u'Цена', blank=True, null=True )
    currency = models.IntegerField( choices=CURRENCY,  verbose_name=u'Валюта', blank=True, null=True )
    auction = models.NullBooleanField(  verbose_name=u'Торг', blank=True, null=True )
    custome = models.NullBooleanField(  verbose_name=u'Растаможен', blank=True, null=True )
    remark = models.TextField( verbose_name=u'Описание', blank=True, null=True )

    #Комплектация
    salon = models.CharField( max_length=16, choices=SALON, verbose_name=u'Салон', blank=True, null=True )
    interior = models.CharField( max_length=16, choices=INTERIOR, verbose_name=u'Цвет Салона', blank=True, null=True )
    climate_control = models.CharField( max_length=16, choices=CLIMATE_CONTROL, verbose_name=u'Климат-контроль', blank=True, null=True )
    air_conditioning = models.NullBooleanField( verbose_name=u'Кондиционер', blank=True, null=True )
    heated_seats = models.CharField( max_length=16, choices=HEATED_SEATS, verbose_name=u'Обогрев сидений', blank=True, null=True )
    heated_mirrors = models.NullBooleanField( verbose_name=u'Обогрев зеркал', blank=True, null=True )
    cruise_control = models.NullBooleanField( verbose_name=u'Круиз-контроль', blank=True, null=True )
    adjustable_steering = models.CharField( max_length=16, choices=ADJUSTABLE_STEERING, verbose_name=u'Регулируемая рулевая колонка', blank=True, null=True )
    power_steering = models.NullBooleanField( verbose_name=u'Усилитель рулевого управления', blank=True, null=True )
    central_locking = models.NullBooleanField( verbose_name=u'Центральный замок', blank=True, null=True )
    navigation_system = models.NullBooleanField( verbose_name=u'Навигационная система', blank=True, null=True )
    onboard_computer = models.NullBooleanField( verbose_name=u'Бортовой компьютер', blank=True, null=True )
    bluetooth_handsfree = models.NullBooleanField( verbose_name=u'Bluetooth и handsfree', blank=True, null=True )
    parktronic = models.NullBooleanField( verbose_name=u'Парктроник', blank=True, null=True )
    rain_sensor = models.NullBooleanField( verbose_name=u'Датчик дождя', blank=True, null=True )
    light_sensor = models.NullBooleanField( verbose_name=u'Датчик света', blank=True, null=True )
    headlamp_washer = models.NullBooleanField( verbose_name=u'Омыватель фар', blank=True, null=True )
    xenon_headlights = models.NullBooleanField( verbose_name=u'Ксеноновые фары', blank=True, null=True )
    fog_lights = models.NullBooleanField( verbose_name=u'Противотуманные фары', blank=True, null=True )
    wooden = models.NullBooleanField( verbose_name=u'Отделка под дерево', blank=True, null=True )
    wheels = models.CharField( max_length=16, choices=WHEELS, verbose_name=u'Диски', blank=True, null=True )
    wheel_size = models.CharField( max_length=16, choices=WHEEL_SIZE, verbose_name=u'Размер дисков', blank=True, null=True )
    tires = models.CharField( max_length=16, choices=TIRES, verbose_name=u'Покрышки', blank=True, null=True )
    spoiler = models.NullBooleanField( verbose_name=u'Спойлер', blank=True, null=True )
    hitch = models.NullBooleanField( verbose_name=u'Фаркоп', blank=True, null=True )
    has_ballon = models.NullBooleanField( verbose_name=u'Газовый балон', blank=True, null=True )
    hatch = models.NullBooleanField( verbose_name=u'Люк', blank=True, null=True )
    obscured_glass = models.NullBooleanField( verbose_name=u'Тонированные стекла', blank=True, null=True )

    # Безопасность:
    antilock_brakes_abs = models.NullBooleanField( verbose_name=u'Антиблокировочная система (ABS)', blank=True, null=True )
    break_assist = models.NullBooleanField( verbose_name=u'Break assist', blank=True, null=True )
    traction_control_tcs = models.NullBooleanField( verbose_name=u'Антипробуксовочная система (TCS)', blank=True, null=True )
    stability_program_esp = models.NullBooleanField( verbose_name=u'Система курсовой устойчивости (ESP)', blank=True, null=True )
    airbag = models.CharField( max_length=16, choices=AIRBAG, verbose_name=u'Подушки безопасности', blank=True, null=True )

    # Противоугонное оборудование:
    alarm = models.NullBooleanField( verbose_name=u'Сигнализация', blank=True, null=True )
    satellite_alarm_system = models.NullBooleanField( verbose_name=u'Спутниковая охранная система', blank=True, null=True )
    immobilizer = models.NullBooleanField( verbose_name=u'Иммобилайзер', blank=True, null=True )
    castle_cat = models.NullBooleanField( verbose_name=u'Замок КПП', blank=True, null=True )
    locking_bonnet = models.NullBooleanField( verbose_name=u'Замок капота', blank=True, null=True )

    # Электропривод:
    mirror = models.NullBooleanField( verbose_name=u'Электропривод зеркал', blank=True, null=True )
    glass = models.CharField( max_length=16, choices=GLASS, verbose_name=u'Стеклоподъемники', blank=True, null=True )
    driver_seat = models.NullBooleanField( verbose_name=u'Электропривод сиденья', blank=True, null=True )
    passenger_seat = models.NullBooleanField( verbose_name=u'Электропривод пассажирского сиденья', blank=True, null=True )

    # Мультимедиа:
    cd = models.NullBooleanField( verbose_name=u'CD-магнитола', blank=True, null=True )
    mp3 = models.NullBooleanField( verbose_name=u'MP3', blank=True, null=True )
    dvd = models.NullBooleanField( verbose_name=u'DVD', blank=True, null=True )
    tv = models.NullBooleanField( verbose_name=u'TV', blank=True, null=True )
    cassette = models.NullBooleanField( verbose_name=u'Кассетная магнитола', blank=True, null=True )
    def __unicode__(self):
      return str(self.manufacture) + ' ' + str(self.model)
      
    class Meta:
      verbose_name = u"Автомобиль"

class CarPicture( Picture ):
    car = models.ForeignKey( Car, verbose_name=u"Автомобиль" )
    class Meta:
      verbose_name = u"Фото автомобиля"

class Contragent( models.Model ):
    title = models.CharField( max_length=512, verbose_name=u'Название' )
    logo = models.ForeignKey( Picture, verbose_name=u'Логотип', blank=True, null=True )
    foundation_year = models.IntegerField( choices=FOUNDATION_YEAR, verbose_name=u'Год основания', null=True, blank=True )
    reg_date = models.DateField( verbose_name=u'Дата регистрации', auto_now_add=True )
    status = models.IntegerField( choices=CONTRAGENT_STATUS, verbose_name=u'Статус' )
    state = models.ForeignKey( State, verbose_name=u'Страна', blank=True, null=True )
    region = models.ForeignKey( Region, verbose_name=u'Регион', blank=True, null=True )
    city = models.ForeignKey( City, verbose_name=u'Город', blank=True, null=True )
    address = models.CharField( max_length=512, verbose_name=u'Адрес', blank=True, null=True )
    phone = models.CharField( max_length = 128, verbose_name=u'Телефон', blank=True, null=True )
    fax = models.CharField( max_length = 64, verbose_name=u'Факс', blank=True, null=True )
    email = models.EmailField( verbose_name=u'EMail', blank=True, null=True )
    url = models.URLField( verbose_name=u'Сайт', blank=True, null=True )
    skype = models.CharField( max_length=128, verbose_name='Скайп', blank=True, null=True )
    jabber = models.CharField( max_length=128, verbose_name='Jabber', blank=True, null=True )
    icq = models.CharField( max_length=128, verbose_name='ICQ', blank=True, null=True )
    latitude = models.FloatField( verbose_name=u'Широта', blank=True, null=True )
    longitude = models.FloatField( verbose_name=u'Долгота', blank=True, null=True ) 
    short_remark = models.CharField( max_length=512, verbose_name=u'Краткое описание', blank=True, null=True )
    remark = models.TextField( verbose_name=u'Подробное описание', blank=True, null=True )
    main = models.ForeignKey( 'self', verbose_name=u'Вышестоящая организация', blank=True, null=True )
    last_editing = models.DateField( verbose_name=u'Дата последней коррекции', blank=True, null=True, auto_now_add=True )
    
    def dot_latitude( self ):
        return str(self.latitude)
        
    def dot_longitude( self ):
        return str(self.longitude)
        
    def __unicode__(self):
      return self.title
      
    class Meta:
      verbose_name = u"Организация"

class ContragentPicture( Picture ):
    contragent = models.ForeignKey( Contragent, verbose_name=u"Автомобиль" )
    class Meta:
      verbose_name = u"Изображения организации"
    
class Dismantle( Contragent ):
    #Добавить поля, Режим работы, Страница разборки в формате html
    
    car_service= models.NullBooleanField( verbose_name=u'Свой автосервис', blank=True, null=True )
    purchase_vehicles= models.NullBooleanField( verbose_name=u'Скупка автомобилей на разборку', blank=True, null=True )
    new_parts= models.NullBooleanField( verbose_name=u'Наличие новых запчастей', blank=True, null=True )
    contract_motor= models.NullBooleanField( verbose_name=u'Наличие контрактных двигателей', blank=True, null=True )
    send_regions= models.NullBooleanField( verbose_name=u'Отправка в регионы', blank=True, null=True )
    local_delivery= models.NullBooleanField( verbose_name=u'Местная доставка покупателю', blank=True, null=True )
    
    schedule = models.CharField( max_length=256, verbose_name=u'Режим работы', blank=True, null=True )
    html = models.TextField( verbose_name=u'Страница в формате html', blank=True, null=True )
    master = models.ForeignKey( Contragent, verbose_name=u'Организация владелец', related_name='master_dismantle', blank=True, null=True )
    owner =  models.ForeignKey( User, verbose_name=u'Куратор организации' )
    count_views = models.IntegerField( verbose_name=u'Количество показов' )
    
    class Meta:
      verbose_name = u'Авторазборка'
    
    def get_manufactures( self ):
        try:
            return self.manufactures
        except:
            self.manufactures = set()
            dismantle_models = DismantleModel.objects.filter( dismantle=self )
            for i in dismantle_models:
                self.manufactures.add( i.manufacture.logo_url_mini() )
        return self.manufactures
            
    def baloon_small( self ):
        t = template.Template( get_baloon_template().strip() )
        c = template.Context({'d':self, 'manufactures':self.get_manufactures(), 'MEDIA_URL':settings.MEDIA_URL } )
        result = t.render(c)
        return result

      
class DismantleModel( models.Model ):
    dismantle = models.ForeignKey( Dismantle, verbose_name=u'Разборка' )
    manufacture = models.ForeignKey( Manufacture, verbose_name=u'Марка' )
    model = models.ForeignKey( Model, verbose_name=u'Модель' )
    from_year = models.IntegerField( choices=FOUNDATION_YEAR, verbose_name=u'Год (с какого)', null=True, blank=True )
    to_year = models.IntegerField( choices=FOUNDATION_YEAR, verbose_name=u'Год (по какой)', null=True, blank=True )
    representation = models.IntegerField( choices=PERSENT_VALUE, verbose_name=u'Представленность запчастей в %' )
    

class Settings( models.Model ):
    yandex_map_key = models.CharField( max_length=256, verbose_name=u'API-ключ Яндекс', blank=True, null=True )


class ArticleCategory( models.Model ):
    title = models.CharField( max_length=150, verbose_name=u'Название категории')
    
class ArticleGroup( models.Model ):
    title = models.CharField( max_length=150, verbose_name="Название группы")
    category = models.ForeignKey( ArticleCategory, verbose_name=u'Категория группы' )
    
class Article( models.Model ):
    title = models.CharField( max_length=150, verbose_name=u'Название статьи')
    category = models.ForeignKey( ArticleCategory, verbose_name=u'Категория' )
    grup = models.ForeignKey( ArticleGroup, verbose_name=u'Группа' )
    status = models.IntegerField( choices=ARTICLE_STATUS, verbose_name=u'Статус' )
    reg_date = models.DateField( verbose_name=u'Дата создания', blank=True, null=True, auto_now_add=True )
    last_editing = models.DateField( verbose_name=u'Дата последней коррекции', blank=True, null=True, auto_now_add=True )
    body = models.TextField( verbose_name=u'Страница в формате html', blank=True, null=True )
    owner =  models.ForeignKey( User, verbose_name=u'Автор' )
    dismantle = models.ForeignKey( Dismantle, verbose_name=u'Разборка' )

class Payment( models.Model ):
    title = models.CharField( max_length=150, verbose_name=u'Название')
    currency = models.IntegerField( choices=CURRENCY,  verbose_name=u'Валюта', blank=True, null=True )
    direction = models.IntegerField( choices=PAYMENT_DIRECTION, verbose_name=u'Направление' )
    reg_date = models.DateField( verbose_name=u'Дата создания', auto_now_add=True )
    user = models.ForeignKey( User, verbose_name=u'Пользователь' )
    user_balance = models.FloatField( verbose_name=u'Баланс пользователя' )
    remark = models.CharField( max_length=512, verbose_name=u'Краткое описание', blank=True, null=True )

#-----------------------------------------------------
class TodoList(models.Model):
    name = models.CharField(max_length=100)
 
    def __unicode__(self):
        return self.name
 
class TodoItem(models.Model):
    name = models.CharField(max_length=150, help_text="e.g. Buy milk, wash dog etc")
    list = models.ForeignKey(TodoList)
 
    def __unicode__(self):
        return self.name + " (" + str(self.list) + ")"
        