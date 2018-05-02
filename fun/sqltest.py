import sqlite3
def trysql(name,sex):
    name=name
    sex=sex
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    #cursor.execute('create table user (name varchar(20) primary key, sex varchar(20))')
    cursor.execute("insert into user (name,sex) values (\"%s\",\"%s\")" %(name,sex))
    cursor.close()
    conn.commit()
    conn.close()
    return