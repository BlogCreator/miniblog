import sqlite3
import os

class DB:
    insert_disc = {
        "blog":"insert into blog (title,file,pic,desc,date,cls) values(?,?,?,?,?,?)",
        "access_number":"inert into access_number (blog_id,number) values(?,?)",
        "cls":"insert into cls (name) values(?)",
        "comment":"insert into comment (blog_id,content) values(?,?)",
    }
    def __init__(self,db):
        self.connect = sqlite3.connect(db)

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
        for i,j in zip(column,values):
            expr += i+'="'+j+'" '
        sql = "update %s set %s where %s=?"%(table,expr,match[0])
        print(sql)
        self.connect.execute(sql,(match[1],))
        self.connect.commit()


    def search(self,table,match):
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
