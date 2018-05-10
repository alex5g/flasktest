from flask import Flask,render_template,redirect,session,url_for,flash,send_from_directory
from flask_bootstrap import Bootstrap
from fun import mywtform,mynav
from flask_sqlalchemy import SQLAlchemy
import os
from xlwt import *

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']="you guess"#post csrf
app.config['BOOTSTRAP_SERVE_LOCAL']=True#bootstrap本地加载
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
db.create_all()

Bootstrap(app)
mynav.topnav.init_app(app)


@app.route('/')     #主页 目前比较简单 后期完善
def index():
    return render_template('index.html')

@app.route('/iwanttoknowyou',methods=['GET','POST'])    #表格信息第一次录入页面,需要输入密码,表格名,表格项数,返回表格id
def IWantToKnowYou():
    name='输入你的信息'
    form=mywtform.introtocreate()
    if form.validate_on_submit():
        session['tablename']=tablename=form.tablename.data
        session['password']=password=form.tablepassword.data
        session['tablecols']=tablecols=form.tablenum.data
        db.create_all()
        tableid=getuniquetableid()
        session['tableid']=tableid
        addnewtable(tableid,password,tablecols,tablename)
        return redirect(url_for('IWantToKnowYouCreate'))
    return (render_template('iwantokonwyou.html', form=form, name=name))


@app.route('/iwantoknowyou/create',methods=['GET','POST'])      #动态输出表格项名表单
def IWantToKnowYouCreate():
    if(session is None):
        return redirect(url_for('IWantToKnowYou'))
    tableid=session['tableid']
    tablecols=session['tablecols']
    i=1
    while(i<=tablecols):
        setattr(mywtform.DynamicForm,str(i),mywtform.StringField('第'+str(i)+'项'))
        i=i+1
    setattr(mywtform.DynamicForm,"sure",mywtform.SubmitField("我准备好了~"))
    form=mywtform.DynamicForm()
    if form.validate_on_submit():
        i=1
        datas=[]
        while(i<=tablecols):
            datas.append(form.__getattribute__(str(i)).data)
            i=i+1
        addnewtablecolnames(tablecols,tableid,datas)
    return render_template('iwantoknowyou_create.html',form=form,tableid=tableid)

@app.route('/knowmore')     #comingsoon页面
def KnowMore():
    return render_template('comingsoon.html')

@app.route('/verifyid',methods=['GET','POST'])
def verifyid():
    form=mywtform.verifyidform()
    if form.validate_on_submit():
        tableid=form.tableid.data
        if(checkuniqueid(tableid) is None):
            pass#暂缺,提示信息错误
        else:
            session['checkid']=True
            session['tableid']=tableid
            return redirect(url_for('fillintheform'))
    return render_template('verifyid.html', form=form)

@app.route('/fillintheform',methods=['GET','POST'])
def fillintheform():
    if(session['checkid']==True):
        tablecols=gettablecols(session['tableid'])
        names=tablecolsname.query.get(session['tableid'])
        nameslist=[]
        i=1
        while(i<=tablecols):
            nameslist.append(names.__getattribute__('name'+str(i)))
            setattr(mywtform.fillform,str(i),mywtform.StringField(str(i)+'.'+nameslist[i-1]))
            i=i+1
        i=1
        setattr(mywtform.fillform,'sure',mywtform.SubmitField('over~'))
        form=mywtform.fillform()
        if(form.validate_on_submit()):
            datas = []
            while(i<=tablecols):
                datas.append(form.__getattribute__(str(i)).data)
                i=i+1
            db.create_all()
            writetotable(session['tableid'], tablecols, datas)
    return render_template('fillinthefom.html',form=form)


@app.route('/readytoverify',methods=['GET','POST'])        #逻辑页面,是则重定向到信息录入页面,否则重定向到iwantoknowyou
def readytoverify():
    form=mywtform.readytocreate()
    if form.validate_on_submit():
        if form.sel.data=='1':
            return redirect(url_for('IWantToKnowYou'))
        elif(form.sel.data=='2'):
            return redirect('verifyid')
        else:
            return  redirect(url_for('readytofill'))
    return render_template('readytoverify.html', form=form)


@app.route('/readytofill',methods=['GET','POST'])
def readytofill():
    form=mywtform.readytofillform()
    if form.validate_on_submit():
        tableid=form.id.data
        password=form.password.data
        result = tableinfo.query.filter_by(tableid=tableid,password=password).first()
        if(result is None):
            pass
        else:
            session['password']=password
            session['tableid']=tableid
            return redirect(url_for('thelastofus'))
    return render_template('readytofill.html',form=form)

@app.route('/thelastofus',methods=['GET','POST'])       #
def thelastofus():
    if session['password'] is None:
        pass #flash
    else:
        tableobj=tableinfo.query.get(session['tableid'])
        tablecols=tableobj.tablecols
        tablename=tableobj.tablename
        i=tablecontent.query.filter_by(tableid=session['tableid']).count()#计数,填写表格人数
        form=mywtform.thelastusform()
        if form.validate_on_submit():
            filename = tablename+session['tableid']+'.xls'
            if os.path.exists(filename):
                os.remove(filename)
            book= Workbook(encoding='utf-8')
            sheet= book.add_sheet('Sheet1',cell_overwrite_ok=True)
            colsnameobj=tablecolsname.query.filter_by(id=session['tableid']).first()
            temp=1
            while(temp<=tablecols):
                sheet.write(0,temp-1, colsnameobj.__getattribute__('name' + str(temp)))
                temp=temp+1
            datas=tablecontent.query.filter_by(tableid=session['tableid']).all()
            flag=1
            for data in datas:
                index=1
                while(index<=tablecols):
                    sheet.write(flag,index-1,data.__getattribute__('name'+str(index)))
                    index=index+1
                flag=flag+1
            book.save(filename)
            directory = os.getcwd()
            send_from_directory(directory, filename, as_attachment=True)

    return render_template('thelastofus.html',i=i,form=form)


class tableinfo(db.Model):      #表格信息类(以表格id为主键,记录密码,表格名,表格项数)
    __tablename__='tableinfo'
    tableid=db.Column(db.Integer,primary_key=True)
    password=db.Column(db.String(64),unique=False)
    tablecols=db.Column(db.Integer,unique=False)
    tablename=db.Column(db.String(64),unique=False)

    def __init__(self,tableid,password,tablecols,tablename):
        self.tableid=tableid
        self.password=password
        self.tablecols=tablecols
        self.tablename=tablename

class tablecontent(db.Model):
    __tablename__='tablecontent'
    tableid = db.Column(db.Integer,unique=False)
    count=db.Column(db.Integer,primary_key=True)
    name1 = db.Column(db.String(64), unique=False)
    name2 = db.Column(db.String(64), unique=False)
    name3 = db.Column(db.String(64), unique=False)
    name4 = db.Column(db.String(64), unique=False)
    name5 = db.Column(db.String(64), unique=False)
    name6 = db.Column(db.String(64), unique=False)
    name7 = db.Column(db.String(64), unique=False)
    name8 = db.Column(db.String(64), unique=False)
    name9 = db.Column(db.String(64), unique=False)
    name10 = db.Column(db.String(64), unique=False)

    def __init__(self, count,tableid, name1, name2, name3, name4, name5, name6, name7, name8, name9, name10):
        self.tableid = tableid
        self.count=count
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.name4 = name4
        self.name5 = name5
        self.name6 = name6
        self.name7 = name7
        self.name8 = name8
        self.name9 = name9
        self.name10 = name10

class uniquetable(db.Model):        #记录唯一表格id
    __tablename__='uniquetable'
    uniquetableid=db.Column(db.Integer,primary_key=True,unique=False)

    def __init__(self,uniquetableid):
        self.uniquetableid=uniquetableid

class tablecolsname(db.Model):      #表格项目名类,id为主键
    __tablename__='colsname'
    id = db.Column(db.Integer,primary_key=True)
    name1= db.Column(db.String(64), unique=False)
    name2 = db.Column(db.String(64), unique=False)
    name3 = db.Column(db.String(64), unique=False)
    name4 = db.Column(db.String(64), unique=False)
    name5 = db.Column(db.String(64), unique=False)
    name6 = db.Column(db.String(64), unique=False)
    name7 = db.Column(db.String(64), unique=False)
    name8 = db.Column(db.String(64), unique=False)
    name9 = db.Column(db.String(64), unique=False)
    name10 = db.Column(db.String(64), unique=False)

    def __init__(self,id,name1,name2,name3,name4,name5,name6,name7,name8,name9,name10):
        self.id=id
        self.name1=name1
        self.name2=name2
        self.name3=name3
        self.name4=name4
        self.name5=name5
        self.name6=name6
        self.name7=name7
        self.name8=name8
        self.name9=name9
        self.name10=name10

def addnewtable(tableid,password,tablecols,tablename):      #创建新的表格信息
    table=tableinfo(tableid,password,tablecols,tablename)
    db.session.add(table)
    db.session.commit()

def getuniquetableid():
    uniquetableobj=uniquetable.query.first()
    uniquetableid=uniquetableobj.uniquetableid
    uniquetableobj.uniquetableid=uniquetableid+1
    db.session.commit()
    return uniquetableid    #获取唯一表格id 并更新(+1)

def addnewtablecolnames(tablecols,tableid,datas):   #添加表格项目名到数据库
    table=tablecolsname(tableid,name1=None,name2=None,name3=None,name4=None,name5=None,name6=None,name7=None,name8=None,name9=None,name10=None)
    i=0
    while(i<tablecols):
        setattr(table, "name"+str(i+1),datas[i])
        i=i+1
    db.session.add(table)
    db.session.commit()

def checkuniqueid(tableid):
    result=tablecolsname.query.filter_by(id=tableid).first()    #tableinfo内虽然可能有tablecols,但colsname可能没录入
    return result

def gettablecols(tableid): #通过tableinfo返回cols
    cols=tableinfo.query.get(tableid)#待修改
    cols=cols.tablecols
    return cols

def writetotable(tableid,tablecols,datas):
    Tablecontent=tablecontent(count=None,tableid=tableid,name1=None,name2=None,name3=None,name4=None,name5=None,name6=None,name7=None,name8=None,name9=None,name10=None)
    i=1
    while(i<=tablecols):
        setattr(Tablecontent, "name" + str(i), datas[i-1])
        i=i+1
    if(tablecontent.query.filter_by(count=1).first() is None):
        setattr(Tablecontent,"count",1)
    db.session.add(Tablecontent)
    db.session.commit()

@app.route('/about')        #the page just you and me know
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run()
