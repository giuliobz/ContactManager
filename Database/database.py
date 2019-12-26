import sqlite3

class Database:

    def __init__(self):
        super().__init__()

        self.connection = sqlite3.connect("Database/database.db")
        self.cursor = self.connection.cursor()
        self.connection.execute("CREATE TABLE IF NOT EXISTS CONTACTS(C_ID TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, TELEPHONE TEXT, EMAIL TEXT, NOTES TEXT, TAGS TEXT)")
        self.connection.commit()

    # save contact in database
    def saveContact(self, id, first_name, last_name, telephone, e_mail, notes, tags):
        self.connection.execute("INSERT INTO CONTACTS VALUES(?,?,?,?,?,?,?)", (id, first_name, last_name, telephone, e_mail, notes, tags))
        self.connection.commit()

    # get all contact of the database order by name
    def getContacts(self):
        result = self.cursor.execute("SELECT * FROM CONTACTS ORDER BY lower(FIRST_NAME) ASC, LOWER(LAST_NAME) ASC")
        return result.fetchall()
    
    # update a contact with new data
    def updateContact(self,first_name, last_name, telephone, email, notes, tags, id):
        self.connection.execute("""UPDATE CONTACTS SET FIRST_NAME=?, LAST_NAME=?,TELEPHONE=?, EMAIL=?, NOTES=?, TAGS=? WHERE C_ID=?""", (first_name,last_name,telephone,email ,notes, tags, id))
        self.connection.commit()

    #delete a contact
    def deleteContact(self, id):
        self.connection.execute("DELETE FROM CONTACTS WHERE C_ID = ?", (id,))
        self.connection.commit()

    

