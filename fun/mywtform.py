from wtforms import StringField,SubmitField,IntegerField,PasswordField,FieldList,FormField
from wtforms.validators import required,NumberRange
from flask_wtf import FlaskForm


class createform(FlaskForm):
    tablename=StringField('1.表格的主题?比如,金融工程三班同学信息汇集',validators=[required()])
    tablenum=IntegerField('2.有多少项内容?比如,班级,姓名,共两项,输入2即可,最多支持20项',validators=[NumberRange(20)])
    tablepassword=PasswordField('3.输入一个密码,凭借此密码和表格id才可录入信息',validators=[required()])
    submit=SubmitField('嗯,确认过了,下一步')

class createtable(FlaskForm):
    col1=StringField('项目1.',validators=[required()])
    col2=StringField('项目2.')
    col3=StringField('项目3.')
    col4=StringField('项目4.')
    col5=StringField('项目5.')
    col6=StringField('项目6.')
    col7=StringField('项目7.')
    col8=StringField('项目8.')
    col9=StringField('项目9.')
    col10=StringField('项目10.')
    submit=SubmitField('are you ok?i am ok')

class tableist(FlaskForm):
    col=FieldList(FormField(createtable))

def MakeAList(obj):
    cols=[]
    cols.append(obj.col1.data)
    if (obj.col2.data!=''):
        cols.append(obj.col2.data)
    if (obj.col3.data != ''):
        cols.append(obj.col3.data)
    if (obj.col4.data != ''):
        cols.append(obj.col4.data)
    if (obj.col5.data != ''):
        cols.append(obj.col5.data)
    if (obj.col6.data != ''):
        cols.append(obj.col6.data)
    if (obj.col7.data != ''):
        cols.append(obj.col7.data)
    if (obj.col8.data != ''):
        cols.append(obj.col8.data)
    if (obj.col9.data != ''):
        cols.append(obj.col9.data)
    if (obj.col10.data != ''):
        cols.append(obj.col10.data)
    return cols

