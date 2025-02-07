import io
import sqlite3
import sys
from io import BytesIO

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>992</width>
    <height>579</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTextEdit" name="input_unheal">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>0</y>
      <width>371</width>
      <height>91</height>
     </rect>
    </property>
   </widget>
   <widget class="QTextEdit" name="input_disease">
    <property name="geometry">
     <rect>
      <x>570</x>
      <y>0</y>
      <width>421</width>
      <height>91</height>
     </rect>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>240</y>
      <width>791</width>
      <height>181</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="btn_zapros">
    <property name="geometry">
     <rect>
      <x>310</x>
      <y>140</y>
      <width>311</width>
      <height>51</height>
     </rect>
    </property>
    <property name="text">
     <string>Обработать запрос</string>
    </property>
    <property name="autoRepeat">
     <bool>false</bool>
    </property>
   </widget>
   <widget class="QPushButton" name="btn_save">
    <property name="geometry">
     <rect>
      <x>700</x>
      <y>440</y>
      <width>121</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>сохранить результат</string>
    </property>
   </widget>
   <widget class="QPushButton" name="btn_open">
    <property name="geometry">
     <rect>
      <x>780</x>
      <y>500</y>
      <width>161</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>Открыть вторую форму</string>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>370</x>
      <y>0</y>
      <width>191</width>
      <height>101</height>
     </rect>
    </property>
    <property name="text">
     <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p align=&quot;center&quot;&gt;&lt;span style=&quot; color:#0000ff;&quot;&gt;В поле слева нужно вести&lt;/span&gt;&lt;/p&gt;&lt;p align=&quot;center&quot;&gt;&lt;span style=&quot; color:#0000ff;&quot;&gt;ваш симптом.&lt;br/&gt;В поле справа - ваши болезни,&lt;/span&gt;&lt;/p&gt;&lt;p align=&quot;center&quot;&gt;&lt;span style=&quot; color:#0000ff;&quot;&gt;которые могут являться&lt;/span&gt;&lt;/p&gt;&lt;p align=&quot;center&quot;&gt;&lt;span style=&quot; color:#0000ff;&quot;&gt;противопоказанием.&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
    </property>
   </widget>
   <widget class="QPushButton" name="search">
    <property name="geometry">
     <rect>
      <x>400</x>
      <y>500</y>
      <width>201</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Где ближайшая аптека??</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>992</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>'''


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        design = io.StringIO(template)
        uic.loadUi(design, self)
        self.search.clicked.connect(self.open_Search)
        self.btn_zapros.clicked.connect(self.spros)
        self.btn_save.clicked.connect(self.save_results)
        self.btn_open.clicked.connect(self.open_Change)
        self.con = sqlite3.connect('films_db.sqlite')

    def spros(self):
        symptom = self.input_unheal.toPlainText()
        disease = self.input_disease.toPlainText()
        query = f"""SELECT title FROM prepare
                    WHERE unheal = '{symptom}' AND danger <> '{disease}'"""
        cursor = self.con.cursor()
        try:
            result = cursor.execute(query).fetchall()
            if not result:
                raise Exception
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setHorizontalHeaderLabels(["Название препарата"])
            for i, row in enumerate(result):
                item = QTableWidgetItem(str(row[0]))
                self.tableWidget.setItem(i, 0, item)
            self.tableWidget.resizeColumnsToContents()
            self.statusbar.showMessage('')
        except Exception:
            self.statusbar.showMessage('По этому запросу ничего не найдено')

    def save_results(self):
        valid = QMessageBox.question(self, '',
                                     'Сохранить лекарства в файл result.txt?',
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            file = open("result.txt", "w", encoding='utf-8')
            for row in range(self.tableWidget.rowCount()):
                value = self.tableWidget.item(row, 0).text()
                file.write(value + '\n')
            file.close()

    def open_Change(self):
        self.second_form = Change()
        self.second_form.show()

    def open_Search(self):
        self.second_form = Search()
        self.second_form.show()


temp = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="verticalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>280</x>
      <y>110</y>
      <width>511</width>
      <height>231</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout">
     <item>
      <widget class="QLineEdit" name="input_name"/>
     </item>
     <item>
      <widget class="QLineEdit" name="input_unheal"/>
     </item>
     <item>
      <widget class="QLineEdit" name="input_danger"/>
     </item>
    </layout>
   </widget>
   <widget class="QWidget" name="verticalLayoutWidget_2">
    <property name="geometry">
     <rect>
      <x>0</x>
      <y>110</y>
      <width>241</width>
      <height>231</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout_2">
     <item>
      <widget class="QLineEdit" name="lineEdit_2">
       <property name="text">
        <string>Введите имя лекарства:</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QLineEdit" name="lineEdit_3">
       <property name="text">
        <string>Введите сиптомы, которые лечит лекарство:</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QLineEdit" name="lineEdit">
       <property name="text">
        <string>Введите противопоказания:</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class="QTextEdit" name="textEdit">
    <property name="geometry">
     <rect>
      <x>200</x>
      <y>30</y>
      <width>351</width>
      <height>51</height>
     </rect>
    </property>
    <property name="html">
     <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p align=&quot;center&quot; style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt; color:#aa55ff;&quot;&gt;Добавление новых лекарств&lt;br /&gt;в базу данных&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
    </property>
   </widget>
   <widget class="QPushButton" name="save_res">
    <property name="geometry">
     <rect>
      <x>450</x>
      <y>380</y>
      <width>251</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Сохранить</string>
    </property>
   </widget>
   <widget class="QPushButton" name="btn_del">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>380</y>
      <width>251</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Удалить</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>'''


class Change(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        file = io.StringIO(temp)
        uic.loadUi(file, self)
        self.con = sqlite3.connect('films_db.sqlite')
        self.save_res.clicked.connect(self.save_prepare)
        self.btn_del.clicked.connect(self.delete_prepare)

    def save_prepare(self):
        valid_name = QMessageBox.question(self, '',
                                     'Сохранить данные в базу данных? Это действие будет сложно отменить.',
                                     QMessageBox.Yes, QMessageBox.No)
        if valid_name == QMessageBox.Yes:
            input_name = self.input_name.text()
            input_unheal = self.input_unheal.text()
            input_danger = self.input_danger.text()
            cursor = self.con.cursor()
            cursor.execute("INSERT INTO prepare (title, unheal, danger) VALUES (?, ?, ?)",
                           (input_name, input_unheal, input_danger))
            self.con.commit()

    def delete_prepare(self):
        valid_name_del = QMessageBox.question(self, '',
                                          'Удалить данные из базы данных? Это действие будет сложно отменить.',
                                          QMessageBox.Yes, QMessageBox.No)
        if valid_name_del == QMessageBox.Yes:
            name = self.input_name.text()
            unheal = self.input_unheal.text()
            danger = self.input_danger.text()
            cursor = self.con.cursor()
            cursor.execute(f"""DELETE FROM prepare WHERE title = ?
             AND unheal = ? AND danger = ?""", (name, unheal, danger))
            self.con.commit()


t = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>585</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTextEdit" name="zapros">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>90</y>
      <width>311</width>
      <height>21</height>
     </rect>
    </property>
    <property name="html">
     <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;br /&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
    </property>
   </widget>
   <widget class="QPushButton" name="btn_res">
    <property name="geometry">
     <rect>
      <x>180</x>
      <y>210</y>
      <width>361</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>results</string>
    </property>
   </widget>
   <widget class="QTextEdit" name="textEdit">
    <property name="geometry">
     <rect>
      <x>230</x>
      <y>30</y>
      <width>341</width>
      <height>31</height>
     </rect>
    </property>
    <property name="html">
     <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p align=&quot;center&quot; style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-size:12pt; font-style:italic; text-decoration: underline; color:#aa00ff;&quot;&gt;Где же все аптеки?&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
    </property>
   </widget>
   <widget class="QTextEdit" name="textEdit_2">
    <property name="geometry">
     <rect>
      <x>350</x>
      <y>90</y>
      <width>451</width>
      <height>21</height>
     </rect>
    </property>
    <property name="html">
     <string>&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p align=&quot;justify&quot; style=&quot; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;&quot;&gt;&lt;span style=&quot; font-weight:600; font-style:italic; text-decoration: underline;&quot;&gt;&amp;lt;---- Туда стоит вписывать адрес. Пример: Людиново, Московского, 1&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="pharmacy_name">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>150</y>
      <width>191</width>
      <height>20</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="pharmacy_address">
    <property name="geometry">
     <rect>
      <x>260</x>
      <y>150</y>
      <width>251</width>
      <height>20</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="pharmacy_hours">
    <property name="geometry">
     <rect>
      <x>550</x>
      <y>150</y>
      <width>201</width>
      <height>20</height>
     </rect>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class Search(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        file = io.StringIO(t)
        uic.loadUi(file, self)
        self.btn_res.clicked.connect(self.search_apt)

    def search_apt(self):
        def par(x, y):
            coordx = str(float(x[0]) - float(y[0]))
            coordy = str(float(x[1]) - float(y[1]))
            return [coordx, coordy]

        def get_map_params(toponym_coordinates, toponym_upcorner, toponym_lowercorner):
            delta = par(toponym_upcorner, toponym_lowercorner)
            longitude, latitude = toponym_coordinates.split(" ")
            ll = ",".join([longitude, latitude])
            spn = ",".join(delta)
            return ll, spn

        def get_nearest_pharmacy(ll):
            search_api_server = "https://search-maps.yandex.ru/v1/"
            search_params = {
                "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
                "text": "аптека",
                "lang": "ru_RU",
                "ll": ll,
                "type": "biz",
            }
            response = requests.get(search_api_server, params=search_params)
            response.raise_for_status()

            json_response = response.json()
            organizations = json_response["features"]
            if len(organizations) > 0:
                organization = organizations[0]
                org_name = organization["properties"]["name"]
                org_address = organization["properties"]["description"]
                org_hours = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
                return {
                    "name": org_name,
                    "address": org_address,
                    "hours": org_hours,
                    "coordinates": organization["geometry"]["coordinates"],
                }
            else:
                return None

        toponym_to_find = self.zapros.toPlainText()

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"
        }

        response = requests.get(geocoder_api_server, params=geocoder_params)
        response.raise_for_status()

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coordinates = toponym["Point"]["pos"]
        toponym_upcorner = toponym['boundedBy']['Envelope']['upperCorner'].split()
        toponym_lowercorner = toponym['boundedBy']['Envelope']['lowerCorner'].split()

        ll, spn = get_map_params(toponym_coordinates, toponym_upcorner, toponym_lowercorner)

        map_params = {
            "ll": ll,
            "spn": spn,
            "l": "map",
            "pt": f"{ll},pm2dgl"
        }

        nearest_pharmacy = get_nearest_pharmacy(ll)
        if nearest_pharmacy:
            pharmacy_name = nearest_pharmacy["name"]
            pharmacy_address = nearest_pharmacy["address"]
            pharmacy_hours = nearest_pharmacy["hours"]
            pharmacy_coordinates = nearest_pharmacy["coordinates"]
            map_params["pt"] += f"~{pharmacy_coordinates[0]},{pharmacy_coordinates[1]},pm2dgl"

            self.pharmacy_name.setText(f"Ближайшая аптека: {pharmacy_name}")
            self.pharmacy_address.setText(f"Адрес: {pharmacy_address}")
            self.pharmacy_hours.setText(f"Время работы: {pharmacy_hours}")
        else:
            self.pharmacy_address.setText(f"Аптеки поблизости не найдены.")
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        response.raise_for_status()

        Image.open(BytesIO(response.content)).show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
        
