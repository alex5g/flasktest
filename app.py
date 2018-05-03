from flask import Flask,render_template,redirect,session,url_for,flash
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

@app.route('/iwanttoknowyou',methods=['GET','POST'])
def IWantToKnowYou():
    name='输入你的信息'
    form=mywtform.createform()
    if form.validate_on_submit():
        session['name']=form.tablenum.data
        session['password']=form.tablepassword.data
        session['num']=form.tablenum.data
        return redirect(url_for('IWantToKnowYouCreate'))
    return (render_template('user.html',form=form,name=name))


@app.route('/iwantoknowyou/create',methods=['GET','POST'])
def IWantToKnowYouCreate():
    if(session is None):
        #flash("请勿直接创建表格")
        return redirect(url_for('IWantToKnowYou'))
    name='输入你的表单项,最少需要输入一项'
    form=mywtform.createtable()
    return render_template('tableinfo.html',form=form,name=name)

@app.route('/knowmore')
def KnowMore():
    return render_template('cominglater.html')


@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run()
