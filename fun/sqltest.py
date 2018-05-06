'''
class tableinfo(db.Model):
    __tablename__='roles'
    tableid=db.Column(db.Integer,primary_key=True)
    password=db.Column(db.String(64),unique=True)
    tablecols=db.Column(db.Integer,unique=True)
    tablename=db.Column(db.String(64),unique=True)

    def __init__(self,tableid,password,tablecols,tablename):
        self.tableid=tableid
        self.password=password
        self.tablecols=tablecols
        self.tablename=tablename

class tablecolsname(db.Model):
    __tablename__='colsname'
    id = db.Column(db.Integer,primary_key=True)
    name1= db.Column(db.String(64), unique=True)
    name2 = db.Column(db.String(64), unique=True)
    name3 = db.Column(db.String(64), unique=True)
    name4 = db.Column(db.String(64), unique=True)
    name5 = db.Column(db.String(64), unique=True)
    name6 = db.Column(db.String(64), unique=True)
    name7 = db.Column(db.String(64), unique=True)
    name8 = db.Column(db.String(64), unique=True)
    name9 = db.Column(db.String(64), unique=True)
    name10 = db.Column(db.String(64), unique=True)

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

def addnewtable(tableid,password,tablecols,tablename):
    table=tableinfo(tableid,password,tablecols,tablename)
    db.session.add(table)
    db.session.commit()

'''
