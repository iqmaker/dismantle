# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from core.models import Contragent, Manufacture, Model, State, Region, City, Person
from urllib import FancyURLopener
from random import choice
import urllib
import urllib2
import datetime
import re
from core.models import Dismantle
from settings import *
from django.utils.encoding import force_unicode
from django.template import Node, Library
from core.forms import DismantleForm, DismantleSearchForm, user_registration_form, user_profile_form, restore_password_form
import sys
import time
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
import smtplib
from email.mime.text import MIMEText


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
    
class MyOpener(FancyURLopener, object):
    version = choice(user_agents)

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
            address = oState.title.lower() + ', ' + oRegion.title.lower() + u', ' + city.title.lower()
            coord = get_coordinates_yandex( address )
            #print( address.encode( "utf-8" ), coord  )
            city.latitude, city.longitude = coord
            city.save()
        
def update_contragent_coordinates():
    contragents = Contragent.objects.order_by('title')
    for i in contragents:
        if (not i.latitude or not i.longitude) or (i.latitude==0.0 or i.longitude==0.0):
            coord = get_coordinates_yandex( i.address )
            i.latitude, i.longitude = coord
            i.save()

def blogs(request):
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    return render_to_response( 'core/blogs.html', 
                                {'region_name':oRegion.title,
                                 'region_label':u'Регион:',
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
    from django.core import serializers
    print request.GET
    json_subcat = serializers.serialize("json", Model.objects.filter(manufacture=request.GET['id']))
    return HttpResponse(json_subcat, mimetype="application/javascript")
        
def dismantle_add(request):
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    return render_to_response( 'core/dismantle-add.html', 
                            {'region_name':oRegion.title,
                            'region_label':u'Регион:',
                            }, context_instance=RequestContext(request)  )
    
def about(request):
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    return render_to_response( 'core/about.html', 
                            {'region_name':oRegion.title,
                            'region_label':u'Регион:',
                            }, context_instance=RequestContext(request)  )
    
def feedback(request):
    regionid = get_region( request )
    oRegion = Region.objects.get( id=regionid )
    return render_to_response( 'core/feedback.html', 
                            {'region_name':oRegion.title,
                            'region_label':u'Регион:',
                            }, context_instance=RequestContext(request)  )
  

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

def city_center_by_region( regionid ):
    city = City.objects.get( region = regionid, regional_center=1 )
    city.latitude = str(city.latitude)
    city.longitude = str(city.longitude)
    return city
    
def region(request):

    regionid = get_region( request )
    AREGIONS = ','.join( [ str(x) for x in [ 1, ] ] )
    states = State.objects.extra(where=['id IN ( %s )' % AREGIONS  ])
    regions = Region.objects.extra( where=['state_id IN ( %s )' % AREGIONS ] )
    
    for i, j in enumerate( regions ):
        if str(j.id) == str(regionid):
            j.selected = 'yes'
        if i>0 and i%10 == 0:
            j.nextline = 'yes'
     
    oRegion = Region.objects.get( id=regionid )
    resp = render_to_response (  'core/region.html', 
                                { 'states':states, 
                                'regions':regions, 
                                'region_label':u'Регион:',
                                'region_name':oRegion.title,
                                'MEDIA_URL':settings.MEDIA_URL }, 
                                context_instance=RequestContext(request)  )
                                
    set_cookie( resp, 'regionid', regionid ) #Moscow
    resp.content = strip_empty_lines( resp.content )
    return resp


def alias_index( request, region_title, manufacture_title, model_title, page_num ):
    print( region_title, manufacture_title, model_title, page_num )
    return index( request, pageid=page_num )
    
def index( request, regionid=None, manufactureid=None, modelid=None, pageid=None ):
    update_contragent_coordinates()
    #update_city_coordinates()
    contragents = Dismantle.objects.order_by('title')
    manufacture = Manufacture.objects.order_by('title')
    for sub in manufacture:
        sub.file_name = '_'.join( sub.title.replace('-',' ').lower().split() )
        
    for sub in contragents:
        sub.latitude = str(sub.latitude)
        sub.longitude = str(sub.longitude)
        print sub.latitude, sub.longitude

    if request.method == 'POST':        
        form = DismantleSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else: 
        data = { 'manufacture':manufactureid, 'model':modelid }
        form = DismantleSearchForm(  data )
            
    if not regionid:
        regionid = get_region( request )

    if regionid.isdigit(): 
        if Region.objects.filter( id=regionid ).count() == 0:
            regionid = 4 #default Moscow
    else:
            regionid = 4
    
    oRegion = Region.objects.get( id=regionid )
    city_center = city_center_by_region( regionid )
    
    resp = render_to_response( 'core/index.html', 
                            { 'contragents':contragents,
                            'city_center':city_center,
                            'manufacture':manufacture, 
                            'MEDIA_URL':settings.MEDIA_URL,
                            'total':len(contragents),
                            'region_label':u'Регион:',
                            'region_name':oRegion.title,
                            'DismantleSearchForm':form,
                            }, 
                            context_instance=RequestContext(request) )
                            
    set_cookie( resp, 'regionid', regionid ) #Moscow
    resp.content = strip_empty_lines( resp.content )
    return resp

def mylogout(request):
    logout(request)
    return HttpResponseRedirect( "/" )

def registration( request ):
    if request.method == 'POST':
        form = user_registration_form( request.POST )
        if form.is_valid():
            last, first, second = [ x.strip() for x in form.cleaned_data['username'].split(',') ]
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
                        account_state = 0.0 )
            p.save()
            auser = authenticate(username=u.username, password=p.raw_password)
            login( request, auser)
            return HttpResponseRedirect( "/" )
    else:
        form = user_registration_form()
        
    return render_to_response( 'core/registration.html',
                            {'form': form,
                             'next': 'core/profile.html',
                            }, 
                            context_instance=RequestContext(request))

def restorepassword( request ):
    if request.user.is_authenticated():
        return HttpResponseRedirect( "/profile" )
    
    if request.method == 'POST':
        form = restore_password_form( request.POST )
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
                raise
                form.message = u'Пользователь с таким логином не найден'
            
    else:
        form = restore_password_form()
        
    return render_to_response( 'core/restorepassword.html',
                            {'form': form,
                             'next': 'core/restorepassword.html',
                            }, 
                            context_instance=RequestContext(request))  
                            
        
def profile( request ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect( "/login" )
        
    if request.method == 'POST':
        form = user_profile_form( request.POST )
        if form.is_valid():
            last, first, second = [ x.strip() for x in form.cleaned_data['username'].split(',') ]
            
            u = User.objects.get( id = request.user.pk )
            p = Person.objects.get( user = u )
            
            u.username = form.cleaned_data['login'].strip()
            u.email = form.cleaned_data['email'].strip()
            u.first_name = first
            u.last_name = last;
            u.set_password( form.cleaned_data["password"].strip() )
            
            p.second_name = second

            u.save()
            p.save()
            form.message = True
        else:
            print 'not valid form data'
    else:
        u = User.objects.get( id = request.user.pk )
        
        p = Person.objects.get( user = u )
        data = { 'username' : ', '.join( [u.last_name, u.first_name, p.second_name] ), 
                 'login':u.username, 
                 'email':u.email, 
                 'password':p.raw_password,
                 'account_state':p.account_state,
                 }
        form = user_profile_form( data )
        
        
        
    return render_to_response( 'core/profile.html',
                            {'form': form,
                             'next': 'core/profile.html',
                            }, 
                            context_instance=RequestContext(request))    