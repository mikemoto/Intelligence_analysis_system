import mysql.connector

import sys
sys.path.append('/home/dinosaur/projects/Intelligence_analysis_system')
from db_controlter import DB_controlter

class WebSite(DB_controlter):
    def __init__(self):
        DB_controlter.__init__(self)
        self.items = []
        self.get_items_from_db()
        for i in self.items:
            print i

    def get_items_from_db(self):
        self.cursor.execute("SELECT * FROM WebPage_website")
        self.items = self.cursor.fetchall()

    def get_allowed_domains(self):
        return [i[2] for i in self.items]
           
    def get_start_urls(self):
        return [i[3] for i in self.items]
