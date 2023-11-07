import pyodbc

class UserDatabase:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-MOCT6PF;DATABASE=cafe;')
        self.cursor=self.conn.cursor()

    def get_user(self, id):
        query=f"SELECT * FROM USERS WHERE id={id}"
        self.cursor.execute(query)
        user_dict={}
        result = self.cursor.fetchone()
        if result is not None:
            user_dict["id"],user_dict["username"],user_dict["password"]=result
            return user_dict
        else:
            return None

    def add_user(self, username, password):
        query=f"INSERT INTO USERS (username,password) VALUES ('{username}','{password}')"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except pyodbc.IntegrityError:
            return False
    def delete_user(self, id):
        query=f"DELETE FROM USERS where id='{id}'"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True


    def verify_user(self, username, password):
        print(password)
        query=f"SELECT id FROM USERS where username = '{username}' and password = '{password}'"
        a = self.cursor.execute(query)

        result = self.cursor.fetchone()
        if result is None:
            return False
        return result[0]




