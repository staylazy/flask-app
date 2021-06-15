from flask import Flask
from flask import render_template

app = Flask(__name__) 

@app.route("/")
def hello():
    return " <html><head></head> <body> Hello World! </body></html>"


@app.route("/data_to")
def data_to():
    
    some_pars = {'user':'Ivan','color':'red'}
    some_str = 'Hello my dear friends!'
    some_value = 10
    return render_template('simple.html', some_str = some_str,
    some_value = some_value, some_pars=some_pars) 


from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from  wtforms.fields.html5 import IntegerField

from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY


app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcfWDAbAAAAAHDbidfGSi2OmsZpWknvgoE5g44A'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcfWDAbAAAAAA5kZ00T6ys5AcJu73PbO_K-nPnR'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

class NetForm(FlaskForm):
    
    openid = StringField('openid', validators = [DataRequired()])

    upload = FileField('Load image', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
  
    recaptcha = RecaptchaField()
   
    submit = SubmitField('send')

from wtforms import validators
class CropForm(FlaskForm):
    
    pic1 = IntegerField('Number of first part: ', validators=[validators.NumberRange(min=1, max=4)]) 
    pic2 = IntegerField('Number of second part: ', validators=[validators.NumberRange(min=1, max=4)]) 
    pic3 = IntegerField('Number of third part: ', validators=[validators.NumberRange(min=1, max=4)]) 
    pic4 = IntegerField('Number of forth part: ', validators=[validators.NumberRange(min=1, max=4)])  

    upload = FileField('Load image', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
  
    recaptcha = RecaptchaField()
   
    submit = SubmitField('send')

from werkzeug.utils import secure_filename
import os

import net as neuronet

@app.route("/net",methods=['GET', 'POST'])
def net():
    
    form = NetForm()
   
    filename=None
    neurodic = {}
  
    if form.validate_on_submit():
        
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10,'./static')
        decode = neuronet.getresult(fimage)

        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]

        form.upload.data.save(filename)
        print(filename)

    return render_template('net.html',form=form,image_name=filename,neurodic=neurodic) 

from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json

@app.route("/apinet",methods=['GET', 'POST'])
def apinet():
    neurodic = {}
    
    if request.mimetype == 'application/json': 
    
        data = request.get_json()
    
        filebytes = data['imagebin'].encode('utf-8')
        
        cfile = base64.b64decode(filebytes)

        img = Image.open(BytesIO(cfile))
        
        decode = neuronet.getresult([img])
        neurodic = {}
        for elem in decode:
            neurodic[elem[0][1]] = str(elem[0][2])
            print(elem)
    
    ret = json.dumps(neurodic)
    
    resp = Response(response=ret,
    status=200,
    mimetype="application/json")
   
    return resp

import lxml.etree as ET
@app.route("/apixml",methods=['GET', 'POST'])
def apixml():
    #парсим xml файл в dom
    dom = ET.parse("./static/xml/file.xml")
    #парсим шаблон в dom
    xslt = ET.parse("./static/xml/file.xslt")
    #получаем трансформер
    transform = ET.XSLT(xslt)
    #преобразуем xml с помощью трансформера xslt
    newhtml = transform(dom)
    #преобразуем из памяти dom в строку, возможно, понадобится указать кодировку
    strfile = ET.tostring(newhtml)
    return strfile

import crop

@app.route("/cropimage",methods=['GET', 'POST'])
def cropimage():
    form = CropForm()
    filename=None
    parts=None
    graphs=None
    pics_range=[]
    if form.validate_on_submit():
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        form.upload.data.save(filename)
        parts, graphs = crop.get_croped_images(filename)# массив с кусочками изображения 
        pics_range.append(int(form.pic1.data))
        pics_range.append(int(form.pic2.data))
        pics_range.append(int(form.pic3.data))
        pics_range.append(int(form.pic4.data))
        print(pics_range)
    return render_template('cropimage.html', form=form, parts=parts, graphs=graphs, pics_range=pics_range)

