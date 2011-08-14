# -*- coding: utf-8 -*-
from django.db import models
import datetime 

nowdate = datetime.datetime.now()

PAYMENT_IN, PAYMENT_OUT = 1, 2
PAYMENT_DIRECTION = [
    (PAYMENT_IN, 'Поступление'),
    (PAYMENT_OUT, 'Платеж'),
] 

APUBLISHED, ADRAFT, AREMOVED, AARCHIVE = 1, 2, 3, 4
ARTICLE_STATUS = [ 
    (APUBLISHED, 'Опубликована' ),
    (ADRAFT, 'Черновик' ),
    (AREMOVED, 'Удалена' ),
    (AARCHIVE, 'Архивная' ),
]
PERSENT_VALUE = [ (x, str(x)) for x in range(5, 101, 5) ]
FOUNDATION_YEAR = [ (x, str(x)) for x in range( nowdate.year, 1850, -1) ]

SEDAN, HATCHBACK, WAGON, COUPE, SUV, PICKUP, CONVERTIBLE, ROADSTER, MINIVAN, VAN, MICROVAN, BUS, LIMOUSINE, TRUCK = [ x for x in range(1, 15) ]
BODY_TYPE = [ 
  (SEDAN, u'Седан'),
  (HATCHBACK, u'Хетчбэк'),
  (WAGON, u'Универсал'),
  (COUPE, u'Купе'),
  (SUV, u'Внедорожник'),
  (PICKUP, u'Пикап'),
  (CONVERTIBLE, u'Кабриолет'),
  (ROADSTER, u'Родстер'),
  (MINIVAN, u'Минивэн'),
  (VAN, u'Фургон'),
  (MICROVAN, u'Микроавтобус'),
  (BUS, u'Автобус'),
  (LIMOUSINE, u'Лимузин'),
  (TRUCK, u'Грузовик'),
]

WHITE, SILVER, GRAY, YELLOW, ORANGE, BEIGE, GOLD, PINK,RED, VINOUS, BROWN, GREEN, BLUE, BLACK, PURPLE, AQUA, TURQUOISE = [ x for x in range(1, 18) ]
COLOR = (
  ( WHITE, u'Белый' ),
  ( SILVER, u'Серебристый' ),
  ( GRAY, u'Серый' ),
  ( YELLOW, u'Желтый' ),
  ( ORANGE, u'Оранжевый' ),
  ( BEIGE, u'Бежевый' ),
  ( GOLD, u'Золотой' ),
  ( PINK, u'Розовый' ),
  ( RED, u'Красный' ),
  ( VINOUS, u'Бордовый' ),
  ( BROWN, u'Коричневый' ),
  ( GREEN, u'Зеленый' ),
  ( BLUE, u'Синий' ),
  ( BLACK, u'Черный' ),
  ( PURPLE, u'Пурпурный' ),
  ( AQUA, u'Голубой' ),
  ( TURQUOISE, u'Бирюзовый' ),
)

KM, MILE = [1, 2]
MILEAGE_UNIT = (
  ( KM, u'км' ),
  ( MILE, u'миль' ),
)

VELOURS, LEATHER, TISSUE = [1, 2, 3]
SALON = (
  (VELOURS, u'велюр'),
  (LEATHER, u'кожа'),
  (TISSUE, u'ткань'),
)

INTERIOR = (
  (BLACK, u'черный'),
  (GRAY, u'серый'),
  (BEIGE, u'бежевый'),
  (BROWN, u'коричневый'),
)

CLIMATE_ONE, CLIMATE_TWO, CLIMATE_THREE = [1,2,3]
CLIMATE_CONTROL = (
  (CLIMATE_ONE, u'1 зонный'),
  (CLIMATE_TWO, u'2-х зонный'),
  (CLIMATE_THREE, u'3-х и более зонный'),
)

HEATED_FRONT, HEATED_ALL = [1, 2]
HEATED_SEATS = (
  (HEATED_FRONT, u'передний'),
  (HEATED_ALL, u'все'),
)

ADJUSTABLE_ONE, ADJUSTABLE_TWO = [1, 2]
ADJUSTABLE_STEERING = (
  (ADJUSTABLE_ONE, u'1 положение'),
  (ADJUSTABLE_TWO, u'2 положения'),
)

CAST, FORGED, STEEL = [1, 2, 3]
WHEELS = (
  (CAST, u'литые'),
  (FORGED, u'кованые'),
  (STEEL, u'стальные'),
)

WHEEL_SIZE = ( [ (x, u'R'+str(x)) for x in range(7,41)] )

SUMMER, WINTER, SUMMER_WINTER, ALL_SEASON = [1, 2, 3, 4]
TIRES = (
  ( SUMMER, u'лето'),
  ( WINTER, u'зима'),
  ( SUMMER_WINTER, u'лето+зима'),
  ( ALL_SEASON, u'всесезонка'),
)

ONE_AIRBAG, TWO_AIRBAG, MORE_AIRBAG = [ 1, 2, 3 ]
AIRBAG = (
  ( ONE_AIRBAG, u'1'),
  ( TWO_AIRBAG, u'2'),
  ( MORE_AIRBAG, u'4 и более'),
)

GLASS_FRONT, GLASS_ALL = [1, 2]
GLASS = (
  ( GLASS_FRONT, u'передние'),
  ( GLASS_ALL, u'все'),
)

CS_BASE, CS_PAYED, CS_UNPAID, CS_UNPAID_HIDE, CS_REMOVED, CS_FREE = [1,2,3,4,5,6]

CONTRAGENT_STATUS = (
  (CS_BASE, u'Базовый'),
  (CS_PAYED, u'Оплаченный'),
  (CS_UNPAID, u'Неоплаченный'),
  (CS_UNPAID_HIDE, u'Неоплаченный скрытый'),
  (CS_REMOVED, u'Удаленный'),
  (CS_FREE, u'Бесплатный'),
)

CONTACT_ACTIVE, CONTACT_BLOCKED, CONTACT_HIDE, CONTACT_REMOVED = [ 1, 2, 3, 4 ]
CONTACT_STATUS = (
  (CONTACT_ACTIVE, u'Активный'),
  (CONTACT_BLOCKED, u'Заблокированный'),
  (CONTACT_HIDE, u'Скрыт'),
  (CONTACT_REMOVED, u'Удаленный'),
)

DOORS_COUNT = ( [(x,str(x)) for x in range(1,10)] ) 

KPP_MECHANIC, KPP_AUTO, KPP_VARIATOR = [ 1, 2, 3 ]
KPP_TYPE = ( 
  (KPP_MECHANIC, u'механическая'),
  (KPP_AUTO, u'автоматическая'),
  (KPP_VARIATOR, u'вариатор'),
)

PETROL_INJECTOR, PETROL_CARBURETOR, PETROL_COMPRESSOR, PETROL_TURBINE, PETROL_ROTOR, DIESEL, DESEL_TURBINE, ELECTRIC, HYBRID = [1,2,3,4,5,6,7,8,9]
CAR_POWER = (
    (u'Бензиновый', (
                    (PETROL_INJECTOR, u'инжектор'),
                    (PETROL_CARBURETOR, u'карбюратор'),
                    (PETROL_COMPRESSOR, u'компрессор'),
                    (PETROL_TURBINE, u'с турбиной'),
                    (PETROL_ROTOR, u'ротороный')
                   )),
   (u'Дизельный',   (
                    (DIESEL, u'без турбины'),
                    (DESEL_TURBINE, u'с турбиной'),
                    )),
  (ELECTRIC, u'Электромобиль'),
  (HYBRID, u'Гибридный'),
)

WD_FRONT, WD_REAR, WD_FULL = [ 1, 2, 3]
WHEEL_DRIVE = ( 
  (WD_FRONT, u'Передний'),
  (WD_REAR, u'Задний'),
  (WD_FULL, u'Полный'),
)

LEFT, RIGHT = [1, 2]

HAND_LOCATION = (
  ( LEFT, u'Левый'),
  ( RIGHT, u'Правый'),
)

NO_WARRANTY, LESS_YEAR_WARRANTY, YEAR_MORE_WARRANTY, TWO_MORE_WARRANTY, THREEE_MORE_WARRANTY = [1, 2, 3, 4, 5]
WARRANTY = ( 
  ( NO_WARRANTY, u'Нет гарантии' ),
  ( LESS_YEAR_WARRANTY, u'Менее года' ),
  ( YEAR_MORE_WARRANTY, u'Год и более' ),
  ( TWO_MORE_WARRANTY, u'Два года и более' ),
  ( THREEE_MORE_WARRANTY, u'Три года и более' ),
)

COND_NEW, COND_BEST, COND_GOOD, COND_MEDIUM, COND_BAD, COND_CRASH = [1, 2, 3, 4, 5, 6]
CONDITION = (
  ( COND_NEW, u'Новое' ),
  ( COND_BEST, u'Отличное' ),
  ( COND_GOOD, u'Хорошее' ),
  ( COND_MEDIUM, u'Среднее' ),
  ( COND_BAD, u'Плохое' ),
  ( COND_CRASH, u'Аварийное' ),
)

RUB, DOLLAR, EURO = [ 1, 2, 3 ]
CURRENCY = (
  ( RUB, u'RUR' ),
  ( DOLLAR, u'$USD' ),
  ( EURO, u'€EURO' ),
)

INVOICE_CREATED, INVOICE_PAYED, INVOICE_CANCELED, INVOICE_REMOVED = 1, 2, 3, 4
INVOICE_STATUS = [ 
    (INVOICE_CREATED, 'Выписан' ),
    (INVOICE_PAYED, 'Оплачен' ),
    (INVOICE_CANCELED, 'Отменен' ),
    (INVOICE_REMOVED, 'Удален' ),
]


