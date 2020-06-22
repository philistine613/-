import sys,os, codecs, sqlite3
from interface2 import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pygame
from pygame import mixer
mixer.init()
from tinytag import TinyTag


class MyWin(QtWidgets.QMainWindow):    
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 


        start_katalog_name="C:\\Users\\pc" #начальная по умолчанию
        self.ui.lineEdit.setText(start_katalog_name)
        self.ui.pushButton.clicked.connect(self.get_dirs)
        self.ui.pushButton_4.clicked.connect(self.get_start_katalog)

    def get_dirs(self):

        self.path=[]
            
        self.p=self.ui.lineEdit.text()
        print("search procces started")
        for root, dirs, files in os.walk(str(self.p)):
            for file in files:
                if file.endswith(".mp3"):
                    k = str(os.path.join(root, file)) #полный путь к тому или иному файлу
                    stroka=k.replace("\\","\\")
                    s=len(stroka.split("\\"))
                    spisok_strok=stroka.split("\\")
                    directory_name=""
                    for i in range (s-1):
                        directory_name= directory_name + spisok_strok[i] + "\\\\"
                    self.path.append(directory_name[:-2])
        print("search procces finished")
        
        self.path = dict(zip(self.path, self.path)).values()

        
        self.ui.comboBox.clear()
        for item in self.path:
            self.ui.comboBox.addItem(item)


    def get_start_katalog(self):

        self.ui.listWidget.clear()
        self.ui.listWidget_2.clear()
        self.get_dirs_for_start_katalog()
        self.create_db_tables()
        self.startitems()

    def get_dirs_for_start_katalog(self):

        self.artist= []
        self.genre= []
        self.year= []
        self.album= []
        self.songname=[]
        self.katalog_path=[] #здесь будут храниться директории ко всем найденным файлам
        self.cortezhi=[]

        for root, dirs, files in os.walk(self.ui.comboBox.currentText()):
            for file in files:
                if file.endswith(".mp3"):
                    k = str(os.path.join(root, file))
                    self.katalog_path.append(k.replace('\\','\\'))


        for i in range(len(self.katalog_path)):
            self.fullpath=self.katalog_path[i].replace('\\','\\\\')
            self.title=self.fullpath.split('\\')[-1]
            
            tag = TinyTag.get(self.fullpath)
            a = '%s' % tag.artist
            g = '%s' % tag.genre
            y = '%s' % tag.year
            al = '%s' % tag.album

            kat=[a,g,y,al]
            for kategory in kat:
                if kategory=="":
                    kategory="None"
                else:
                    pass
        
            self.artist.append(a)
            self.genre.append(g)
            self.year.append(y)
            self.album.append(al)
            self.songname.append(self.title)
            self.katalog_path.append(self.fullpath)


        for i in range(len(self.songname)):
            self.cortezh=[self.songname[i],self.katalog_path[i],self.artist[i],self.album[i],self.year[i],self.genre[i]]
            self.cortezhi.append(self.cortezh)

        

        self.ui.listWidget.currentTextChanged.connect(self.getinfo)
        self.ui.listWidget_2.currentTextChanged.connect(self.getinfo2)
        self.ui.pushButton_2.clicked.connect(self.playmusic)
        self.ui.pushButton_3.clicked.connect(self.stopmusic)

    
    def create_db_tables(self):
        con = sqlite3.connect('mydatabase2.db')

        cursorObj = con.cursor()

        from sqlite3 import Error
        def sql_connection():

            try:

                con = sqlite3.connect('mydatabase2.db')

                return con

            except Error:

                print(Error)

        sql_connection()

        def sql_fetch(con):

            cursorObj = con.cursor()

            cursorObj.execute('DROP table if exists musicmetadata2')

            con.commit()

        sql_fetch(con)

        def sql_table(con):

            cursorObj = con.cursor()
            
            cursorObj.execute("CREATE TABLE if not exists musicmetadata2(title text, fullpath text, artist text, album text, year integer, genre text)")

            con.commit()

        con = sql_connection()

        sql_table(con)

        def sql_insert(con):
            cursorObj = con.cursor()


            for element in self.cortezhi:


                cursorObj.execute('INSERT INTO musicmetadata2 VALUES(?, ?, ?, ?, ?,?)', element)

            con.commit()

                

        sql_insert(con)
     

    #блок интеграции программы и базы

    con = sqlite3.connect('mydatabase2.db')

    def startitems(self):
        self.ui.listWidget.clear()
        column_names=['all','artist','album','year','genre']
        for name in column_names:
            self.ui.listWidget.addItem(str(name))

        self.dirs_name=[]


    def getinfo(self):
        self.counter=1
        con = sqlite3.connect('mydatabase2.db')
        self.flag=0
        try:
            self.catname=self.ui.listWidget.currentItem().text()
        except AttributeError:
            print('эхххх')
        else:
            print('dbf')
        finally:
            print("you can ran")
            self.dirs_name.append(self.catname)
        cursorObj = con.cursor()
        if (self.catname=='all'):
            self.tmp="all"
            cursorObj.execute('SELECT DISTINCT title FROM musicmetadata2')
            rows = cursorObj.fetchall()
            self.ui.listWidget_2.clear() 
            #s=list(set(rows))
            for row in rows:
                self.ui.listWidget_2.addItem((str(row))[2:-3])
            self.flag=1
        elif (self.catname=='artist'):
            self.tmp="artist"
            cursorObj.execute('SELECT DISTINCT artist FROM musicmetadata2 WHERE artist!="None"')
            rows = cursorObj.fetchall()
            self.ui.listWidget_2.clear()
            #s=list(set(rows))
            for row in rows:
                self.ui.listWidget_2.addItem((str(row))[2:-3])
            self.flag=1
        elif (self.catname=='album'):
            self.tmp="album"
            cursorObj.execute('SELECT DISTINCT album FROM musicmetadata2 WHERE album!="None"')
            rows = cursorObj.fetchall()
            self.ui.listWidget_2.clear()
            #s=list(set(rows))
            for row in rows:
                self.ui.listWidget_2.addItem((str(row))[2:-3])
            self.flag=1
        elif (self.catname=='year'):
            self.tmp="year"
            cursorObj.execute('SELECT year FROM musicmetadata2 WHERE year!="None"')
            rows = cursorObj.fetchall()
            self.ui.listWidget_2.clear()
            s=list(set(rows))
            for i in range(len(s)-1):
                for j in range(len(s)-i-1):
                    if str(s[j]) > str(s[j+1]):
                        s[j], s[j+1] = s[j+1], s[j]
            for element in s:
                self.ui.listWidget_2.addItem(str(element).strip("(',')"))
            self.flag=1
        elif (self.catname=='genre'):
            self.tmp="genre"
            cursorObj.execute('SELECT DISTINCT genre FROM musicmetadata2 WHERE genre!="None"')
            rows = cursorObj.fetchall()
            self.ui.listWidget_2.clear()
            #s=list(set(rows))
            for row in rows:
                self.ui.listWidget_2.addItem((str(row))[2:-3])
            self.flag=1
        self.counter=0


    def getinfo2(self):
        con = sqlite3.connect('mydatabase2.db')
        try:
            self.choicename=self.ui.listWidget_2.currentItem().text()
            print('ok')
        except AttributeError:
            print('hz che delat')
        else:
            print('dbf')
        finally:
            print(self.choicename)
            self.dirs_name.append(self.choicename)

        cursorObj = con.cursor()
        if(self.tmp=="all"):
            self.flag=1
        elif (self.tmp == "artist"):
            if self.counter==0:
                self.flag=0
                cursorObj.execute('SELECT DISTINCT * FROM musicmetadata2')
                self.ui.listWidget_2.clear()
                while (True):
                    row = cursorObj.fetchone()
                    if row == None:
                        break
                    if row[2]==self.choicename:
                        self.ui.listWidget_2.addItem(str(row[0]).strip("(',')"))
            else:
                self.flag=1
        elif (self.tmp == "album"):
            if self.counter==0:
                self.flag=0
                cursorObj.execute('SELECT DISTINCT * FROM musicmetadata2')
                self.ui.listWidget_2.clear()
                while (True):
                    row = cursorObj.fetchone()
                    if row == None:
                        break
                    if row[3]==self.choicename:
                        self.ui.listWidget_2.addItem(str(row[0]).strip("(',')"))
                
            else:
                self.flag=1
        elif (self.tmp == "year"):
            if self.counter==0:
                self.flag=0
                cursorObj.execute('SELECT DISTINCT * FROM musicmetadata2')
                self.ui.listWidget_2.clear()
                while (True):
                    row = cursorObj.fetchone()
                    if row == None:
                        break
                    if str(row[4])==str(self.choicename):
                        self.ui.listWidget_2.addItem(str(row[0]).strip("(',')"))
                
            else:
                self.flag=1
        else:
            if self.counter==0:
                self.flag=0
                cursorObj.execute('SELECT DISTINCT * FROM musicmetadata2')
                self.ui.listWidget_2.clear()
                while (True):
                    row = cursorObj.fetchone()
                    if row == None:
                        break
                    if str(row[5])==str(self.choicename):
                        self.ui.listWidget_2.addItem(str(row[0]).strip("(',')"))
                
            else:
                self.flag=1
        self.counter=1

    def playmusic(self):

        con = sqlite3.connect('mydatabase2.db')

        if self.flag==1:
            mixer.music.stop()
            self.selitem=""
            try:
                self.selitem= self.ui.listWidget_2.currentItem().text()
                print('ok')
            except AttributeError:
                print('neznau')
            else:
                print('ran')
            finally:
                print(self.selitem)
            cursorObj = con.cursor()
            cursorObj.execute('SELECT DISTINCT * FROM musicmetadata2 WHERE title=="'+self.selitem+'" ')
            put=cursorObj.fetchone()
            mixer.music.stop()
            mixer.music.load(u''+put[1])

            mixer.music.play()
        self.flag=0

    def stopmusic(self):
        mixer.music.stop()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())