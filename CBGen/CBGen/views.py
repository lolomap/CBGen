"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from CBGen import app
import random
import numpy as np
import cv2
import time
import io
import base64
import math
import asyncio

flag_path = 'CBGen/static/'
alphabet = 'абвгдеёжзиклмнопрстуфхыэюя'
glas = 'аааааааааааааааеееееееееееееееёиииииииииииииииоооооооооооооооууууууууууууэюяы'
glas_b = 'еёиюя'
glas_soed = 'аоие'
sogl = 'бвгржзклмнпрстфх'
CountryPostfixes = ["стан", "лэнд", "ия", "бург"]
CountryTypes = ["Государство", "Рейх", "Империя", "Королевство", "Царство", "Ханство", "Республика", "Коммуна"]
CountryIdeologies = {0: ["Фашизм", "Национал-социализм", "Неофашизм", "Фалангизм", "Национализм", "Консерватизм"],
                     1: ["Социализм", "Национал-большевизм"],
                     2: ["Анархо-коммунизм", "Анархо-примитивизм", "Анархо-индивидуализм", "Анархо-капитализм"],
                     3: ["Радикальный центризм", "Либерализм", "Социал-демократия", "Популизм", "Охлократия", "Консерватизм"]}
CountryGovtypes = {0: ["Абсолютная монархия", "Дуалистическая монархия"],
                   1: ["Диктатура пролетариата"],
                   2: ["Народный совет"],
                   3: ["Президент", "Парламент", "Президент и парламент"],
                   4: ["Военная диктатура", "Вождизм"]}

FlagTemplates = ['cross', 'cross_stand', 'plus', 'star', 'circle', 'horizontal', 'vertical', 'div_block', 'div', 'div_db',
                 'random']

def name_create():
    result = ''
    slogs = random.randint(1, 7)

    result += alphabet[random.randint(0, len(alphabet) - 1)].upper()
    for i in range(slogs+1):
        if result[-1] in glas:
            result += sogl[random.randint(0, len(sogl) - 1)]
        else:
            if random.randint(1, 100) > 95:
                if random.randint(0, 1) == 0:
                    result += 'ь'
                else:
                    result += 'ъ'
                result += glas_b[random.randint(0, len(glas_b) - 1)]
            else:
                result += glas[random.randint(0, len(glas) - 1)]
        if random.randint(1, 10) < 6:
            if result[-1] in glas:
                result += sogl[random.randint(0, len(sogl) - 1)]
            else:
                if random.randint(1, 10) > 95:
                    if random.randint(0, 1) == 0:
                        result += 'ь'
                    else:
                        result += 'ъ'
                    result += glas_b[random.randint(0, len(glas_b) - 1)]
                else:
                    result += glas[random.randint(0, len(glas) - 1)]
    
    if len(result) < 6:
        if random.randint(1, 10) < 2:
            if random.randint(0, 1) == 1:
                result += glas_soed[random.randint(0, len(glas_soed) - 1)]
            result += CountryPostfixes[random.randint(0, len(CountryPostfixes) - 1)]
    
    return result

def cross_stand_paint(img, shape, start):
    x = random.randint(start[0], shape[1])
    y = random.randint(start[1], shape[0])
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    thickness = random.randint(20, 70)
    cv2.line(img, (x, start[1]), (x, shape[0]), color, thickness)
    cv2.line(img, (start[0], y), (shape[1], y), color, thickness)

def cross_paint(img, shape, start):
    x = random.randint(start[0], shape[1])
    y = random.randint(start[1], shape[0])
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    thickness = random.randint(20, 70)
    angle = math.radians(random.randint(10, 70))

    l1top = int(x + y // math.tan(angle))
    l1bot = int(y + x * math.tan(angle))
    l2top = int(y - x * math.tan(angle))
    l2bot = int(l1top)

    cv2.line(img, (start[0], l1bot), (l1top, start[1]), color, thickness)
    cv2.line(img, (start[0], l2top), (l2bot, shape[0]), color, thickness)

def circle_paint(img, shape, start):
    x = random.randint(start[0], shape[1])
    y = random.randint(start[1], shape[0])
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    radius = random.randint(50, 300)
    cv2.circle(img, (x, y), radius, color, -1)

def div_block_paint(img, shape, start):
    x = random.randint(50, 300)
    y = random.randint(50, 300)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    oriantation = random.randint(1, 4)
    if oriantation == 1:
        cv2.rectangle(img, (start[0], start[1]), (x, y), color, -1)
        fs = (0, 0)
    elif oriantation == 2:
        cv2.rectangle(img, (shape[1] - x, start[1]), (start[0], y), color, -1)
        fs = (shape[1] - x, start[1])
    elif oriantation == 3:
        cv2.rectangle(img, (shape[1] - x, shape[0] - y), (shape[1], shape[0]), color, -1)
        fs = (shape[1] - x, shape[0] - y)
    elif oriantation == 4:
        cv2.rectangle(img, (start[0], shape[0] - y), (x, start[1]), color, -1)
        fs = (start[0], shape[0] - y)
    fsh = (fs[1] + y, fs[0] + x)
    return (fs, fsh)

def paint(img):
    templates_num = random.randint(1, 3)
    flag_shape = img.shape
    flag_start = (0, 0)
    for i in range(templates_num):
        templ = FlagTemplates[random.randint(0, len(FlagTemplates) - 1)]
        if templ == 'cross_stand':
            cross_stand_paint(img, flag_shape, flag_start)
        elif templ == 'cross':
            cross_paint(img, flag_shape, flag_start)
        elif templ == 'circle':
            circle_paint(img, flag_shape, flag_start)
        elif templ == 'div_block':
            flag_start, flag_shape = div_block_paint(img, flag_shape, flag_start)
        else:
            continue

def flag_create():
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = np.full((512, 512, 3), color, np.uint8)
    print('paint start')
    paint(img)
    print('paint finnished')
    fn = str(time.time())
    is_success, buffer = cv2.imencode('.jpg', img)
    fio = io.BytesIO(buffer)
    fio.seek(0)
    url = base64.b64encode(fio.getvalue()).decode()
    print('file saved')
    return 'data:image/jpeg;base64, {}'.format(url)

@app.route("/", methods=["POST"])
def generate():
    print('generation started')
    name = ''

    rideo = random.randint(0, len(CountryIdeologies) - 1)
    rsubideo = random.randint(0, len(CountryIdeologies[rideo]) - 1)
    ideology = CountryIdeologies[rideo][rsubideo]

    allowed_types = []
    if rideo == 0:
        allowed_types = CountryTypes[:6]
    elif rideo == 1:
        allowed_types = [CountryTypes[6]]
    elif rideo == 2:
        allowed_types = [CountryTypes[7]]
    elif rideo == 3:
        allowed_types = CountryTypes[3:7]
    rtype = allowed_types[random.randint(0, len(allowed_types) - 1)]
    if rtype in CountryTypes[3:6] and rideo == 3:
        govtype = 'Парламентская монархия'
    elif rideo == 0:
        if rtype in CountryTypes[2:6]:
            govtype = CountryGovtypes[0][random.randint(0, len(CountryGovtypes[0]) - 1)]
        else:
            govtype = CountryGovtypes[4][random.randint(0, len(CountryGovtypes[4]) - 1)]
    else:
        govtype = CountryGovtypes[rideo][random.randint(0, len(CountryGovtypes[rideo]) - 1)]
        

    name += rtype
    name += ' ' + name_create()

    print('flag generation started')
    flag = flag_create()

    print('done')
    return render_template('index.html', title='Home Page', BallFlag = flag,
                           BallName=name, BallIdeology=ideology, BallGovtype=govtype)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
