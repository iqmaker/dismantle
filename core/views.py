# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404  
from django.template import RequestContext
from django.core.urlresolvers import reverse
from core.models import *
from core.forms import *
from django.core.context_processors import csrf
from django.conf import settings

from urllib import FancyURLopener
from random import choice
import urllib
import urllib2
import datetime
import re
from settings import *
from django.utils.encoding import force_unicode
from django.template import Node, Library

import sys
import time
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
import smtplib
from email.mime.text import MIMEText
import enums

from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory, BaseFormSet
import inspect
from django.db.models import Q
from django.core import serializers

class Object:pass

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

headers = {
'Host' : 'www.ripn.net',
'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16',
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language' : 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
'Accept-Encoding' : 'gzip,deflate',
'Accept-Charset' : 'windows-1251,utf-8;q=0.7,*;q=0.7',
'Keep-Alive' : '300',
'Connection' : 'keep-alive',
'Referer' : 'http://www.ripn.net/nic/whois/',
'Content-Type' : 'application/x-www-form-urlencoded',
'Server' : 'nginx/0.7.63',
'Date' : 'Wed, 19 Jan 2011 22:38:32 GMT',
'Content-Type' : 'text/html; charset=windows-1251',
}


def DBOUT( obj ):
    """Returns the current line number in our program."""
    print ( ">>>>>>>>>>>>>>>>>>: ", obj, ' LINE:', str(inspect.currentframe().f_back.f_lineno) )
    
def handle_uploaded_file(f, t):
    destination = open(t, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
def send_text_email( from_email, to_email, subject, body ):
    msg = MIMEText( body.encode( 'utf-8') )
    msg.set_charset('utf-8')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    s = smtplib.SMTP('localhost')
    s.sendmail( from_email, [to_email,], msg.as_string() )
    s.quit()
    
def strip_empty_lines(value):
    """Return the given HTML with empty and all-whitespace lines removed."""
    return re.sub(r'\n[ \t]*(?=\n)', '', force_unicode(value))
    
def set_cookie( response, key, value, days_expire = 60 ):
    if days_expire is None:
        max_age = 365*24*60*60  #one year
    else:
        max_age = days_expire*24*60*60 
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
    return response

def get_region( request ):
    regionid = 4 #Moscow
    if 'regionid' in request.COOKIES:
        regionid = request.COOKIES[ 'regionid' ]
        
    if request.method == 'POST': 
       if 'regionid' in request.POST:
           regiondid = requst.POST[ 'regionid' ]
    else:
        if 'regionid' in request.GET:
            regionid = request.GET[ 'regionid' ]
            
    return regionid
    
class MyOpener(FancyURLopener, object):
    version = choice(user_agents)

class LinkManager:
    links=[ ('/', 'главная') ]
    currentlink = tuple()
    
    def update(self):
        if self.currentlink in self.links:
            self.links = self.links[:self.links.index( self.currentlink ) + 1]
        else:
            self.links.append( self.currentlink )

    def __init__( self, links=[ ('/', 'главная') ], currentlink=( '/', 'главная' ) ):
        self.links = links
        self.currentlink = currentlink
        self.update()

    def add_link( self, link ):
        self.currentlink = link
        self.update()

    def get_currentlink( self ):
        return self.currentlink

    def get_links( self ):
        return self.links

    def get_render_links( self ):
        result = ''
        for link in self.links:
            result += '<a href="' + link[0] + '">/' + link[1] + '</a>'
        return result


def get_coordinates_google( address ):
    myopener = MyOpener()
    result = myopener.open(u'http://maps.google.com/maps/geo?q=%s&output=json&oe=utf8&sensor=true'% urllib.quote( address.encode( 'utf-8') ) )
    data = result.read()
    data = eval( data )
    if data['Status']['code'] != 602:
        try:
            result = data['Placemark'][0]['Point']['coordinates'][0:2][::-1]
        except:
            result = [0.0, 0.0]
    else:
        result = [0.0, 0.0]
    return result


def get_coordinates_yandex( address ):
    myopener = MyOpener()
    #http://geocode-maps.yandex.ru/1.x/?geocode=Москва,+Тверская+улица,+дом+7&key=API-ключ
    result = myopener.open(u'http://geocode-maps.yandex.ru/1.x/?geocode=%s&key=%s&format=json'% ( urllib.quote( address.encode( 'utf-8') ), 'AGM9JU4BAAAApnERaQIA5uUwIjR0IRLVHltbc8K-PSpaLyoAAAAAAAAAAACokFuosvhvF6pJ8ceyJqc8ec75Gw==') )
    data = result.read()
    data = eval( data )
    try:
        point = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[::-1]
    except:
        point = [0.0, 0.0]
    print point
    return point
    
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def update_city_coordinates():
    cities = City.objects.all()
    for city in cities:
        oRegion = Region.objects.get( id=city.region_id )
        oState = State.objects.get( id=city.state_id )
        if (not city.latitude or not city.longitude) or (city.latitude==0.0 or city.longitude==0.0):
            time.sleep( 0.5 )
            address = oState.title.lower() + ', ' + oRegion.ru_title.lower() + u', ' + city.title.lower()
            coord = get_coordinates_yandex( address )
            #print( address.encode( "utf-8" ), coord  )
            city.latitude, city.longitude = coord
            city.save()

def check_contragent_coordinates( c ):
    if (not c.latitude or not c.longitude) or (c.latitude==0.0 or c.longitude==0.0):
        coord = get_coordinates_yandex( c.address )
        c.latitude, c.longitude = coord
        c.save()
    
def update_contragent_coordinates():
    contragents = Contragent.objects.order_by('title')
    for i in contragents:
        check_contragent_coordinates(i)

def blogs(request):
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/blogs.html', 
                                {'region_name':oRegion.ru_title,
                                 'region_label':u'регион:',
                                 'meta':meta,
                                }, context_instance=RequestContext(request)  )

def mansearch(request):
     if request.method == 'GET':  
         GET = request.GET  
         if GET.has_key('q'):
             q = request.GET.get( 'q' )
             search = Manufacture.objects.all()
             results = search.filter(title__contains = q)
             matches = ""
             for result in results:
                 matches = matches + "%s\n" % (result.title)
             return HttpResponse(matches.strip(), mimetype="text/plain")

def modelsearch(request):
     if request.method == 'GET':  
         GET = request.GET  
         if GET.has_key('q'):
             q = request.GET.get( 'q' )
             search = Model.objects.all()
             results = search.filter(title__contains = q)
             matches = ""
             for result in results:
                 matches = matches + "%s\n" % (result.title)
             return HttpResponse(matches.strip(), mimetype="text/plain")

def manufacture_models(request):
    print request.GET
    json_subcat = serializers.serialize("json", Model.objects.filter(manufacture=request.GET['id']).order_by( 'title' ))
    return HttpResponse(json_subcat, mimetype="application/javascript")

def region_by_state(request):
    print request.GET
    json_subcat = serializers.serialize("json", Region.objects.filter(state=request.GET['stateid']) )
    return HttpResponse(json_subcat, mimetype="application/javascript")

def city_by_region(request):
    print request.GET
    json_subcat = serializers.serialize("json", City.objects.filter(region=request.GET['regionid']).order_by( 'title' ))
    return HttpResponse(json_subcat, mimetype="application/javascript")
    
    
def about(request):
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/about.html', 
                            {'region_name':oRegion.ru_title,
                            'region_label':u'регион:',
                            'meta':meta,
                            }, context_instance=RequestContext(request)  )
    
def feedback(request):
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/feedback.html', 
                            {'region_name':oRegion.ru_title,
                            'region_label':u'регион:',
                            'meta':meta,
                            }, context_instance=RequestContext(request)  )

def city_center_by_region( regionid ):
    city = City.objects.get( region = regionid, regional_center=1 )
    city.latitude = str(city.latitude)
    city.longitude = str(city.longitude)
    city.zoom = 9
    return city

def city_center_by_city( cityid ):

    city = City.objects.get( id = cityid )
    city.latitude = str(city.latitude)
    city.longitude = str(city.longitude)
    
    if city.regional_center:
        city.zoom = 10
    else:
        city.zoom = 12
    return city
    
def region(request):
    regionid = get_region( request )
    AREGIONS = ','.join( [ str(x) for x in [ 1, ] ] ) #Only Russia
    states = State.objects.extra(where=['id IN ( %s )' % AREGIONS  ])
    regions = Region.objects.extra( where=['state_id IN ( %s )' % AREGIONS ] )
    
    for i, j in enumerate( regions ):
        if str(j.id) == str(regionid):
            j.selected = 'yes'
        if i>0 and i%10 == 0:
            j.nextline = 'yes'
     
    oRegion = Region.objects.get( id=regionid )
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    resp = render_to_response (  'core/region.html', 
                                { 'states':states, 
                                'regions':regions, 
                                'region_label':u'регион:',
                                'region_name':oRegion.ru_title,
                                'meta':meta,
                                'MEDIA_URL':settings.MEDIA_URL }, 
                                context_instance=RequestContext(request)  )
                                
    set_cookie( resp, 'regionid', regionid ) #Moscow
    resp.content = strip_empty_lines( resp.content )
    return resp


def alias_index( request, manufacture_title=None, model_title=None, region_title=None, city_title=None ):
    manufacture_id = None
    model_id = None
    region_id = None
    city_id = None
    
    if manufacture_title:
        manufactures = Manufacture.objects.all()
        for m in manufactures:
            if m.url_name() == manufacture_title:
                manufacture_id = m.id
                break
        if manufacture_id and model_title:
            models = Model.objects.filter( manufacture=manufacture_id )
            DBOUT( len( models ) )
            for m in models:
                DBOUT( m.url_name() )
                if m.url_name() == model_title:
                    model_id = m.id
                    break
            if model_id and region_title:
                regions = Region.objects.all()
                for r in regions:
                    if r.url_name() == region_title:
                        region_id = r.id
                        break
            if region_id and city_title:
                cities = City.objects.filter( region=region_id )
                for c in cities:
                    if c.url_name() == city_title:
                        city_id = c.id
                        break

            
    print( manufacture_title, model_title, region_title, city_title )
    print (  manufacture_id, model_id, region_id, city_id )
    
    return index( request, manufacture_id, model_id, region_id, city_id )
    
def index( request, manufactureid=None, modelid=None, regionid=None, cityid=None ):
    tree_urls = ( ( '/', 'Главная' ), )

    user_regionid = None
    user_regionid = get_region( request )
    if user_regionid:
        user_region = Region.objects.get( id=user_regionid )

    if manufactureid:
        mf = Manufacture.objects.get( id=manufactureid )
        tree_urls += ( ( '/razborka/%s' % mf.url_name(), mf.ru_title ), )
    if modelid:
        md = Model.objects.get( id=modelid )
        tree_urls += ( ( '/razborka/%s/%s' % (mf.url_name(), md.url_name() ) , md.title ), )
    if regionid:
        rg = Region.objects.get( id=regionid )
        tree_urls  += ( ( '/razborka/%s/%s/region-%s' % ( mf.url_name(), md.url_name(), rg.url_name() ), rg.ru_title ), )
    if cityid:
        ct = City.objects.get( id=cityid )
        tree_urls += ( ( '/razborka/%s/%s/region-%s/gorod-%s' % ( mf.url_name(), md.url_name(), rg.url_name(), ct.url_name() ), ct.ru_title ), )
        
    
    head_links = []

    print( manufactureid, modelid, regionid, cityid )
    if manufactureid and modelid and regionid and cityid:
        #Конечный пункт поэтому ничего не генерим
        pass
    elif manufactureid and modelid and regionid:
        #Генерим города региона в которых есть разборки
        cities = City.objects.filter( region=regionid )
        for c in cities:
            link = '/razborka/%s/%s/region-%s/gorod-%s' % ( mf.url_name(), md.url_name(), rg.url_name(), c.url_name() ) 
            hl = { 'link':link, 'ru_title':c.ru_title }
            head_links.append( hl )
    elif manufactureid and modelid:
        #Генерим регионы в которых есть данные разборки
        regions = Region.objects.filter( state=1 ) #Only Russia
        for r in regions:
            link = '/razborka/%s/%s/region-%s' % ( mf.url_name(), md.url_name(), r.url_name() )
            hl = { 'link':link, 'ru_title':r.ru_title }
            head_links.append( hl )
    elif manufactureid:
        #Генерим модели в данной марки по которым есть разборки
        models = Model.objects.filter( manufacture=manufactureid )
        for m in models:
            link = '/razborka/%s/%s' % ( mf.url_name(), m.url_name() )
            hl = { 'link':link, 'ru_title':m.title }
            head_links.append( hl )
    else:
        #Генерим марки автомобилей по которым есть разборки
        manufactures = Manufacture.objects.order_by( 'title' )
        last_symbol = ''
        for m in manufactures:
            link = '/razborka/%s' % m.url_name()
            image_name = m.file_name() 
            symbol = m.title[:1]
            if last_symbol != symbol:
                hl = { 'link':link, 'ru_title':m.title, 'image_name':image_name, 'symbol':symbol }
                head_links.append( hl )
                last_symbol = symbol
            else:
                hl = { 'link':link, 'ru_title':m.title, 'image_name':image_name }
                head_links.append( hl )
            
            
    if not regionid:
        regionid = user_regionid
        
    update_contragent_coordinates()
    #update_city_coordinates()
        
    manufacture = Manufacture.objects.order_by('ru_title')
    DBOUT( manufacture )
    #for sub in manufacture:
    #    sub.file_name = '_'.join( sub.title.replace('-',' ').lower().split() )

    if request.method == 'POST':    
        head_links = []
        form = DismantleSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            manufactureid = cd['manufacture']
            modelid = cd['model']
    else: 
        data = { 'manufacture':manufactureid, 'model':modelid }
        form = DismantleSearchForm(  data )
     
    if manufactureid is None and modelid is None:
        contragents = ()
    else:
        contragents = Dismantle.objects.order_by('title')

    for sub in contragents:
        sub.latitude = str(sub.latitude)
        sub.longitude = str(sub.longitude)
        print sub.latitude, sub.longitude
        
    if not regionid:
        regionid = 4 #Moscow
    
    if not cityid:
        city_center = city_center_by_region( regionid )
    else:
        city_center = city_center_by_city( cityid )
    
    
    for i, hl in enumerate(head_links):
        if (i)%(int( (len(head_links)+5)/5.0 ) ) == 0:
            hl[ 'block' ] = True
            
    DBOUT( head_links )
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    resp = render_to_response( 'core/index.html', 
                            { 'contragents':contragents,
                            'city_center':city_center,
                            'manufacture':manufacture, 
                            'MEDIA_URL':settings.MEDIA_URL,
                            'total':len(contragents),
                            'region_label':u'регион:',
                            'region_name':user_region.ru_title,
                            'DismantleSearchForm':form,
                            'meta':meta,
                            'tree_urls':tree_urls,
                            'ismain': len(tree_urls)==1,
                            'head_links':head_links,
                            }, 
                            context_instance=RequestContext(request) )
                            
    resp.content = strip_empty_lines( resp.content )
    set_cookie( resp, 'regionid', user_regionid )
    return resp

def mylogout(request):
    logout(request)
    return HttpResponseRedirect( "/" )

def registration( request ):
    if request.method == 'POST':
        form = UserRegistrationForm( request.POST, request=request )
        if form.is_valid():
            fullname = form.cleaned_data['username']
            if len( fullname.split( ',' ) ) >=3:
                last, first, second = [ x.strip() for x in fullname.split(',') ][:3]
            else:
                last, first, second = [ x.strip() for x in fullname.split(' ') ][:3]
                
            u = User( first_name=first, 
                         last_name=last,  
                         username=form.cleaned_data['login'], 
                         email=form.cleaned_data['email'], 
                         is_staff=False,
                         is_active=True, 
                         is_superuser=False, 
                         last_login=datetime.datetime.now(),
                         date_joined=datetime.datetime.now())
                         
            u.set_password( form.cleaned_data["password"].strip() )
            u.save()
            
            p = Person( user = u, 
                        second_name=second, 
                        raw_password=form.cleaned_data["password"].strip(), 
                        birth_date = None,
                        reg_date = datetime.datetime.now(),
                        status = enums.CONTACT_ACTIVE,
                        phone = form.cleaned_data['phone'].strip(),
                        user_balance = 0.0 )
            p.save()
            auser = authenticate(username=u.username, password=p.raw_password)
            login( request, auser)
            return HttpResponseRedirect( "/" )
    else:
        form = UserRegistrationForm()
        
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/registration.html',
                            {'form': form,
                             'next': 'core/profile.html',
                             'meta':meta,
                            }, 
                            context_instance=RequestContext(request))

def changepassword( request ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect( "/login" )
        
    u = User.objects.get( id = request.user.pk )
    
    if request.method == 'POST':
        form = ChangePasswordForm( request.POST, request=request )
        if form.is_valid():
            new = form.cleaned_data['new_password']
            p = Person.objects.get( user = u )
            u.set_password( new )
            p.raw_password = new
            p.save()
            form.message = 'Пароль изменен'
    else:
        form = ChangePasswordForm()
        
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/changepassword.html',
                            {'form': form,
                             'login':u.username,
                             'next': 'core/restorepassword.html',
                             'meta':meta,
                            }, 
                            context_instance=RequestContext(request))  
        
    
                
    
def restorepassword( request ):
    if request.user.is_authenticated():
        return HttpResponseRedirect( "/profile" )
    
    if request.method == 'POST':
        form = RestorePasswordForm( request.POST )
        if form.is_valid():
            login = form.cleaned_data['username'].strip()
            try:
                u = User.objects.get( username=login )
                p = Person.objects.get( user = u )
                print u.email, p.raw_password
                form.message = u'Пароль отправлен на указанный email'
                subject = u'Восстановление пароля vse-razborki.ru ' + login
                body = u'Пароль : ' + p.raw_password
                print body
                
                send_text_email( u'yusupov_dk@mail.ru', u.email, subject, body ) 
            except:
                form.message = u'Пользователь с таким логином не найден'
            
    else:
        form = RestorePasswordForm()
        
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/restorepassword.html',
                            {'form': form,
                             'next': 'core/restorepassword.html',
                             'meta':meta,
                            }, 
                            context_instance=RequestContext(request))  
                            

def extract_phones( source ):
    r = re.findall( '\+7\(\d{3,}\)[\d\-]{5,}', source )
    return r
            
def profile( request ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect( "/login" )
   
    user_regionid = get_region( request )
    if user_regionid:
        user_region = Region.objects.get( id=user_regionid )
        
    u = User.objects.get( id = request.user.pk )
    p = Person.objects.get( user = u )
    dismantles = Dismantle.objects.filter( owner=request.user ).exclude( status=enums.CS_REMOVED )
    if request.method == 'POST':
        form = UserProfileForm( request.POST, request=request )
        if form.is_valid():
            
            fullname = form.cleaned_data['username']
            if len( fullname.split( ',' ) ) >=3:
                last, first, second = [ x.strip() for x in fullname.split(',') ][:3]
            else:
                last, first, second = [ x.strip() for x in fullname.split(' ') ][:3]
            
            u.username = form.cleaned_data['login'].strip()
            u.email = form.cleaned_data['email'].strip()
            u.first_name = first
            u.last_name = last;
            #u.set_password( form.cleaned_data["password"].strip() )
            
            p.second_name = second
            
            p.phone = form.cleaned_data['phone']
            u.save()
            p.save()
            form.message = True
        else:
            print 'not valid form data'
    else:
        data = { 'username' : ', '.join( [u.last_name, u.first_name, p.second_name] ), 
                 'login':u.username, 
                 'email':u.email, 
                 'password':p.raw_password,
                 'user_balance':p.user_balance,
                 'phone':p.phone,
                 }
        form = UserProfileForm( data )
        
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/profile.html',
                            {'form': form,
                             'next': 'core/profile.html',
                             'user':u,
                             'dismantles':dismantles,
                             'meta':meta,
                             'region_label':u'регион:',
                             'region_name':user_region.ru_title,
                            }, 
                            context_instance=RequestContext(request))    

    
def remove_dismantle_model( dismantle_id, notremove=[] ):
    dm = DismantleModel.objects.filter( dismantle=dismantle_id )
    for i in dm:
        if not (i.pk in notremove):
            i.delete()

def remove_contragent_picture( contragent_id, notremove=[] ):
    DBOUT( notremove )
    cp = ContragentPicture.objects.filter( contragent=contragent_id )
    for i in cp:
        if i.title != 'logo' and not( i.pk in notremove):
            DBOUT( "REMOVED:" + str(i.pk) )
            i.delete()
        

def dismantle_remove( request, dismantle_id ):
    if not request.user.is_authenticated():
        raise Http404
    
    u = User.objects.get( id = request.user.pk )
    try:
        d = Dismantle.objects.get( id=dismantle_id )
    except:
        raise Http404
    
    d.last_editing = datetime.datetime.now()
    if d.owner_id != u.id and not u.is_superuser:
        raise Http404
    d.status = enums.CS_REMOVED
    d.save()
    
    return HttpResponseRedirect( "/profile" )
    
        
def dismantle_editor( request, dismantle_id=-1 ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect( "/login" )
        
    u = User.objects.get( id = request.user.pk  )
    
    DismantleModelFormSet = formset_factory(DismantleModelForm, max_num=50)
    ImageFormSet = formset_factory(ImageForm, max_num=20 )
    
    locale_names = { 'action':u'Добавление-коррекция' }
    if request.method == 'POST':
        print request.POST
        print request.FILES
        
        form = DismantleAddForm( request.POST, request.FILES )
        models_formset = DismantleModelFormSet(request.POST, request.FILES, prefix='models' )
        images_formset = ImageFormSet(request.POST, request.FILES, prefix='images' )
        
        if form.is_valid(): 
            dismantle_id = form.cleaned_data['dismantle_id']

            if dismantle_id != -1:
                try:
                    d = Dismantle.objects.get( id=dismantle_id )
                    d.last_editing = datetime.datetime.now()
                except:
                    raise Http404  
                
            else:
                d = Dismantle()
                d.reg_date = datetime.datetime.now()
                d.last_editing = datetime.datetime.now()
            
            d.title=form.cleaned_data['title']
            d.status = enums.CS_BASE
            d.owner = request.user
            d.foundation_year=form.cleaned_data['foundation_year']
            d.state=form.cleaned_data['state']
            d.region=form.cleaned_data['region']
            d.city=form.cleaned_data['city']
            d.address=form.cleaned_data['address']
            d.car_service=form.cleaned_data['car_service']
            d.purchase_vehicles=form.cleaned_data['purchase_vehicles']
            d.new_parts=form.cleaned_data['new_parts']
            d.contract_motor=form.cleaned_data['contract_motor']
            d.send_regions=form.cleaned_data['send_regions']
            d.local_delivery=form.cleaned_data['local_delivery']
            d.schedule=form.cleaned_data['schedule']
            d.phone=form.cleaned_data['phone']
            d.fax=form.cleaned_data['fax']
            d.email=form.cleaned_data['email']
            d.url=form.cleaned_data['url']
            d.skype=form.cleaned_data['skype']
            d.jabber=form.cleaned_data['jabber']
            d.icq=form.cleaned_data['icq']
            d.short_remark=form.cleaned_data['short_remark']
            d.remark=form.cleaned_data['remark']
            d.html=form.cleaned_data['html'] 
            d.latitude = None
            d.longitude = None

#new            
            if u'logo' in request.FILES:
                p = Picture( title = 'logo',
                            description = 'logo',
                            picture = form.cleaned_data[ 'logo' ],
                            pub_date = datetime.datetime.now() )
                p.save()
                d.logo = p
            else:
                DBOUT( "NO LOGO" )
#endnew                
            d.save()
            dismantle_id = d.id 
            
            """
            if u'logo' in request.FILES:
                remove_contragent_logo( dismantle_id )
                logo = ContragentPicture( title = 'logo',
                                                description = 'logo',
                                                picture = form.cleaned_data[ 'logo' ],
                                                pub_date = datetime.datetime.now(),
                                                contragent = d )
                logo.save()
            """
            
            request.POST['dismantle_id'] = dismantle_id
            form = DismantleAddForm( request.POST, request.FILES )
                                            
            #remove_dismantle_model( dismantle_id )
            not_removed_models = []
            for model in models_formset.forms:
                if model.is_valid():
                    if model.cleaned_data['modelid']:
                        try:
                            dm = DismantleModel.objects.get( pk=model.cleaned_data['modelid'] )
                            not_removed_models.append( dm.pk )
                        except:
                            dm = DismantleModel()
                    else:
                        dm = DismantleModel()
                
                    dm.dismantle = d
                    dm.manufacture = model.cleaned_data['manufacture']
                    dm.model = model.cleaned_data['model']
                    dm.from_year = model.cleaned_data['from_year']
                    dm.to_year = model.cleaned_data['to_year']
                    dm.representation = model.cleaned_data['representation'] 
                    dm.save()
                    not_removed_models.append( dm.pk )
                else:
                    print model.errors
                    
            remove_dismantle_model( dismantle_id, notremove=not_removed_models )
            
            not_removed_images = []
            for image in images_formset.forms:
                if image.is_valid():
                    if 'imageid' not in image.cleaned_data:
                        continue
                    
                    DBOUT( image.cleaned_data )
                    if image.cleaned_data['imageid']:
                        try:
                            cp = ContragentPicture.objects.get( pk=image.cleaned_data['imageid'] )
                            not_removed_images.append( cp.pk )
                        except:
                            cp = ContragentPicture()  
                    else:
                        cp = ContragentPicture()  
                    
                    cp.title = image.cleaned_data['title']
                    cp.description = image.cleaned_data['description']
                    cp.pub_date = datetime.datetime.now()
                    cp.contragent = d
                    
                    if 'picture' in image.cleaned_data:
                        if image.cleaned_data['picture'] != None:
                            cp.picture = image.cleaned_data[ 'picture' ]
                        #elif image.cleaned_data['picture
                        
                    cp.save()
                    not_removed_images.append( cp.pk )
                else:
                    print image.errors
                    
            remove_contragent_picture( dismantle_id, notremove=not_removed_images )
        else:
            print "NOT VALID MAIN FORM", form.errors 
        
        return HttpResponseRedirect( "/dismantle-view/%s" % dismantle_id  )
            
    else:
        if dismantle_id == -1: #dismantle-add
            form = DismantleAddForm( initial={'dismantle_id' : dismantle_id } )
            models_formset = DismantleModelFormSet( prefix='models' )
            images_formset = ImageFormSet( prefix='images' )
        else: #dismantle-edit
            locale_names['action']='Коррекция'
            try:
                d = Dismantle.objects.get( id=dismantle_id )
                d.last_editing = datetime.datetime.now()
                if d.owner_id != u.id and not u.is_superuser:
                    raise Http404
            except:
                raise Http404 
            
            
            DBOUT( d.logo )
            main_form_data = { 'title':d.title,
                                'logo':d.logo,
                                'foundation_year':d.foundation_year,
                                'state':d.state,
                                'region':d.region,
                                'city':d.city,
                                'address':d.address,
                                'car_service':d.car_service,
                                'purchase_vehicles':d.purchase_vehicles,
                                'new_parts':d.new_parts,
                                'contract_motor':d.contract_motor,
                                'send_regions':d.send_regions,
                                'local_delivery':d.local_delivery,
                                'schedule':d.schedule,
                                'phone':d.phone,
                                'fax':d.fax,
                                'email':d.email,
                                'url':d.url,
                                'skype':d.skype,
                                'jabber':d.jabber,
                                'icq':d.icq,
                                'short_remark':d.short_remark,
                                'remark':d.remark,
                                'html':d.html, 
                                'dismantle_id': dismantle_id }
                                
            if d.logo:
                locale_names['contragent_logo'] = d.logo.picture.url
                         
            form = DismantleAddForm( main_form_data )
            
            #initing models
            dismantle_models = DismantleModel.objects.filter( dismantle = dismantle_id )
            initial = []
            for dm in dismantle_models:
                field = { }
                field['modelid']=dm.id
                field[ 'manufacture' ] = dm.manufacture
                field[ 'model' ] = dm.model
                field[ 'from_year' ] = dm.from_year
                field[ 'to_year' ] = dm.to_year
                field[ 'representation' ] = dm.representation                
                initial.append( field )
            
            if dismantle_models.count() > 0:
                DismantleModelFormSet = formset_factory(DismantleModelForm, max_num=50, extra=0)
            
            models_formset = DismantleModelFormSet( prefix='models', initial=initial )
             
            #initing pictures
            contragent_pictures = ContragentPicture.objects.filter( contragent = dismantle_id ).exclude(title='logo')
            initial = []
            for cp in contragent_pictures:
                field = { }
                field['imageid']=cp.id
                field['title'] = cp.title
                field['description']=cp.description
                field['picture']=cp.picture
                initial.append( field )
                
            if contragent_pictures.count() > 0:
                ImageFormSet = formset_factory(ImageForm, max_num=20, extra=1 )
                
           
            images_formset = ImageFormSet( prefix='images', initial=initial )
            
            
            

    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    return render_to_response( 'core/dismantle-add.html', 
                            {'region_name':oRegion.ru_title,
                            'region_label':u'регион:',
                            'models_formset':models_formset,
                            'images_formset':images_formset,
                            'form':form,
                            'locale_names':locale_names,
                            'meta':meta,
                            }, context_instance=RequestContext(request)  )
                            

def dismantle_view( request, dismantle_id ):
    try:
        d = Dismantle.objects.get( id=dismantle_id )
    except:
        raise Http404
    locale_names = {}
    check_contragent_coordinates( d )
    dismantle_models = DismantleModel.objects.filter( dismantle=d )
    contragent_pictures = ContragentPicture.objects.filter( contragent=d )
    
    manufactures = set()
    for i in dismantle_models:
        manufactures.add( i.manufacture.logo_url_mini() )
    
    main_form_data = { 'title':d.title,
                                'logo':d.logo,
                                'foundation_year':d.foundation_year,
                                'state':d.state,
                                'region':d.region,
                                'city':d.city,
                                'address':d.address,
                                'car_service':d.car_service,
                                'purchase_vehicles':d.purchase_vehicles,
                                'new_parts':d.new_parts,
                                'contract_motor':d.contract_motor,
                                'send_regions':d.send_regions,
                                'local_delivery':d.local_delivery,
                                'schedule':d.schedule,
                                'phone':d.phone,
                                'fax':d.fax,
                                'email':d.email,
                                'url':d.url,
                                'skype':d.skype,
                                'jabber':d.jabber,
                                'icq':d.icq,
                                'short_remark':d.short_remark,
                                'remark':d.remark,
                                'html':d.html, 
                                'dismantle_id': dismantle_id }
                                
    form = DismantleAddForm( main_form_data )
    edit_user = False
    if request.user.is_authenticated():
        u = User.objects.get( id = request.user.pk  )                          
        if d.owner_id == u.id or u.is_superuser:
            edit_user = True
    
    print request
    print( dir( request ) )
    print( request.read() )
    print( request.path )
    
    currentlink = ( request.path, d.title )
    meta = {'title':'не задано','keywords':'не задано','description':'не задано'}
    
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    
    resp = render_to_response( 
                            'core/dismantle-view.html', 
                            {'dismantle':form,
                             'd':d,
                            'dismantle_models':dismantle_models,
                            'contragent_pictures':contragent_pictures,
                            'locale_names':locale_names,
                            'manufactures':manufactures,
                            'edit_user':edit_user,
                            'meta':meta,
                            'region_label':u'регион:',
                            'region_name':oRegion.ru_title,
                            }, context_instance=RequestContext(request)  )
    resp.content = strip_empty_lines( resp.content )
    return resp
    
#----------------------------------------
def todolist(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
 
    TodoItemFormSet = formset_factory(TodoItemForm, max_num=10, formset=RequiredFormSet)
 
    if request.method == 'POST': # If the form has been submitted...
        todo_list_form = TodoListForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        todo_item_formset = TodoItemFormSet(request.POST, request.FILES)
 
        if todo_list_form.is_valid() and todo_item_formset.is_valid():
            todo_list = todo_list_form.save()
            for form in todo_item_formset.forms:
                todo_item = form.save(commit=False)
                todo_item.list = todo_list
                todo_item.save()
 
            return HttpResponseRedirect('/') # Redirect to a 'success' page
    else:
        todo_list_form = TodoListForm()
        todo_item_formset = TodoItemFormSet()
 
    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
    c = {'todo_list_form': todo_list_form,
         'todo_item_formset': todo_item_formset,
        }
    c.update(csrf(request))
 
    return render_to_response('core/todo.html', c)