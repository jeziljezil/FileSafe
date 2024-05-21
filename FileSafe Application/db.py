import sqlite3

class Database:
  def __init__(self, db):
    self.conn = sqlite3.connect(db)
    self.cur = self.conn.cursor()
    self.cur.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, file)")
    self.conn.commit()

  def fetch(self):
    self.cur.execute("SELECT * FROM files")
    rows = self.cur.fetchall()
    return rows
  
  def insert(self, file):
    self.cur.execute("INSERT INTO files VALUES (NULL, ?)", (file,))
    self.conn.commit()
  
  def remove(self, id):
    self.cur.execute("DELETE FROM files WHERE id=?", (id,))
    self.conn.commit()
  

  def __del__(self):
    self.conn.close()


# WARNING: if there is no 'file.db' in the folder uncomment the line 33
#          and run this 'sub_db.py' file once and comment out the line 33         
# db = Database('file.db')