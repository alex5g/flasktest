from flask import Flask,render_template,redirect,session,url_for,flash
from flask_bootstrap import Bootstrap
from fun import mywtform,mynav
from flask_sqlalchemy import SQLAlchemy
import os

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iwanttoknowyou',methods=['GET','POST'])
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


@app.route('/iwantoknowyou/create',methods=['GET','POST'])
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

@app.route('/knowmore')
def KnowMore():
    return render_template('cominglater.html')

@app.route('/checkmaster')
def checkmaster():
    if(session['check']=='true'):
        form=mywtform.checkmaster()

        return render_template('checkmaster.html',form=form)

@app.route('/areyoumymaster',methods=['GET','POST'])
def areyoumymaster():
    form=mywtform.readytocreate()
    if form.validate_on_submit():
        if form.sel.data=='false':
            return redirect(url_for('IWantToKnowYou'))
        else:
            session['check']=form.sel.data
            return redirect('checkmaster')
    return render_template('areyoumymaster.html',form=form)

class tableinfo(db.Model):
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

class uniquetable(db.Model):
    __tablename__='uniquetable'
    uniquetableid=db.Column(db.Integer,primary_key=True,unique=False)

    def __init__(self,uniquetableid):
        self.uniquetableid=uniquetableid


class tablecolsname(db.Model):
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

def addnewtablecolnames(tablecols,tableid,datas):
    table=tablecolsname(tableid,name1=None,name2=None,name3=None,name4=None,name5=None,name6=None,name7=None,name8=None,name9=None,name10=None)
    i=0
    while(i<tablecols):
        setattr(table, "name"+str(i+1),datas[i])
        print(datas[i])
        i=i+1
    db.session.add(table)
    db.session.commit()


@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run()
