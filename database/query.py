import sqlite3
import os

class DB:
    insert_disc = {
        "blog":"insert into blog (title,file,pic,desc,date,cls) values(?,?,?,?,?,?)",
        "click":"insert into click (blog_title,number) values(?,?)",
        "cls":"insert into cls (name) values(?)",
        "comment":"insert into comment (article_title,name,date,content,ip) values(?,?,?,?,?)",
    }
    def __init__(self,db):
        self.connect = sqlite3.connect(db)
        self.connect.row_factory = sqlite3.Row
    def insert(self,table,values):
        """
        insert a new column to a table
        it may throw a sqlite3.IntegrityError exception
        :param table:a table name.
        :param values: a tumple represent a row
        :return: None
        """
        self.connect.execute(self.insert_disc[table],values)
        self.connect.commit()

    def delete(self,table,match):
        """
        delete a matching column
        :param table:a table name
        :param match:a directory has two elements the first one
        is a column name and the second one isthe matching value
        :return:None
        """
        self.connect.execute("delete from %s where %s=?"%(table,match[0]),(match[1],))
        self.connect.commit()

    def row_delete(self,sql):
        """
        use 'delete' to delete a row is recommended unless 'row_delete' is necessary
        """
        self.connect.execute(sql)
        self.commit()

    def update(self,table,column,values,match):
        """
        :param table:
        :param column:
        :param values:
        :param match:
        :return:
        """
        expr = ""
        for i in column[:-1]:
            expr += i+"=?,"
        expr += column[-1]+"=?"

        sql = "update %s set %s where %s=?"%(table,expr,match[0])
        print(sql)
        self.connect.execute(sql,(*values,match[1],))
        self.connect.commit()


    def search(self,table,match:tuple):
        """
        :param table:
        :param match:
        :return:
        """
        sql = "select * from %s where %s=?"%(table,match[0])
        cursor = self.connect.execute(sql,(match[1],))
        return cursor.fetchall()

    def close(self):
        """
        close the database's connection
        """
        self.connect.close()

    def all(self,table):
        return self.connect.execute("select * from %s"%table).fetchall()
