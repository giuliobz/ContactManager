import os
import cv2
import sqlite3

class Database:

    def __init__(self):
        super().__init__()

        self.connection = sqlite3.connect("Database/database.db")
        self.cursor = self.connection.cursor()
        self.connection.execute("CREATE TABLE IF NOT EXISTS CONTACTS(C_ID TEXT, PHOTO TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, TELEPHONE TEXT, EMAIL TEXT, NOTES TEXT, TAGS TEXT)")
        self.connection.commit()

    # save contact in database
    def saveContact(self, id, photo, first_name, last_name, telephone, e_mail, notes, tags):
        image_path = 'Database/imageDatabase/' + first_name + '_' + last_name + '.png'
        self.connection.execute("INSERT INTO CONTACTS VALUES(?,?,?,?,?,?,?,?)", (id, image_path, first_name, last_name, telephone, e_mail, notes, tags))
        cv2.imwrite(image_path, cv2.imread(photo))
        self.connection.commit()
        return image_path

    # get all contact of the database order by name
    def getContacts(self):
        result = self.cursor.execute("SELECT * FROM CONTACTS ORDER BY lower(FIRST_NAME) ASC, LOWER(LAST_NAME) ASC")
        return result.fetchall()
    
    # update a contact with new data
    def updateContact(self, photo, first_name, last_name, telephone, email, notes, tags, id):
        img =  cv2.imread(photo)
        if [path for path in os.listdir('Database/imageDatabase/') if first_name in path or last_name in path]:
            os.remove(['Database/imageDatabase/' + path for path in os.listdir('Database/imageDatabase/') if first_name in path or last_name in path][0])
        image_path = 'Database/imageDatabase/' + first_name + '_' + last_name + '.png'
        self.connection.execute("""UPDATE CONTACTS SET PHOTO=?, FIRST_NAME=?, LAST_NAME=?,TELEPHONE=?, EMAIL=?, NOTES=?, TAGS=? WHERE C_ID=?""", (image_path, first_name,last_name,telephone,email ,notes, tags, id))
        cv2.imwrite(image_path, img)
        self.connection.commit()

    #delete a contact
    def deleteContact(self, id, photo):
        self.connection.execute("DELETE FROM CONTACTS WHERE C_ID = ?", (id,))
        os.remove(photo)
        self.connection.commit()
