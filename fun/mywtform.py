from wtforms import StringField,SubmitField,IntegerField,PasswordField,RadioField
from wtforms.validators import required,NumberRange
from flask_wtf import FlaskForm


class introtocreate(FlaskForm):
    tablename=StringField('1.表格的主题?比如,金融工程三班同学信息汇集',validators=[required()])
    tablenum=IntegerField('2.有多少项内容?比如,班级,姓名,共两项,输入2即可,最少需要1项,最多支持10项',validators=[NumberRange(1,10)])
    tablepassword=PasswordField('3.输入一个密码,凭借此密码和表格id才可录入信息',validators=[required()])
    submit=SubmitField('嗯,确认过了,下一步')


class DynamicForm(FlaskForm):
        pass

class readytocreate(FlaskForm):
    sel=RadioField(choices=[('1','是'),('2','你猜'),('3','好好看看我是谁')])
    submit=SubmitField('我已经遵从我内心的选择')

class verifyidform(FlaskForm):
    tableid=StringField('告诉我你的真身,master',validators=[required()])
    submit=SubmitField('来吧')

class readytofillform(FlaskForm):
    id=StringField('告诉我你需要导出的表的唯一id',validators=[required()])
    password=StringField('输入密码,确保你是创建者',validators=[required()])
    submit=SubmitField('未来可期')

class fillform(FlaskForm):
    pass

class thelastusform(FlaskForm):
    submit=SubmitField('来日方长,see you again')
#class checkid