from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from fun import sqltest,mywtform,mynav
#from jinja2.ext import loopcontrols

app = Flask(__name__)
app.config['SECRET_KEY']="you guess"
app.config['BOOTSTRAP_SERVE_LOCAL']=True


Bootstrap(app)
mynav.topnav.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getinfo',methods=['GET','POST'])
def getinfo():
    name='输入你的信息'
    form=mywtform.createform()
    '''if form.validate_on_submit():    #sql实验部分
        name=form.name.data
        sex=form.sex.data           
        sqltest.trysql(name,sex)
    '''
    if form.validate_on_submit():
        global num
        num=form.tablenum.data
    return (render_template('user.html',form=form,name=name))


@app.route('/getinfo/create',methods=['GET','POST'])
def create():
    name='输入你的表单项,最少需要输入一项'
    form=mywtform.createtable()
    cols=mywtform.MakeAList(form)
    for col in cols:
        pass
    return render_template('tableinfo.html',form=form,name=name)



if __name__ == '__main__':
    app.run()
