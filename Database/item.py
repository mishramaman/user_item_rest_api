import pyodbc


class ItemDatabase:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-MOCT6PF;DATABASE=cafe;')
        self.cursor=self.conn.cursor()


    def get_Items(self):
        result=[]
        query="SELECT * FROM ITEM"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item = {}
            item["id"] = row[0]
            item["name"] = row[1]
            item["balls"]=row[2]
            item["runs"]=row[3]
            item["out"]=row[4]

            result.append(item)
        print(result)
        return result


    def get_Item(self, team_id):

        query = f"select * from ITEM where id='{team_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():

            item_dict = {}
            item_dict["id"] = row[0]
            item_dict["name"] = row[1]
            item_dict["balls"] = row[2]
            item_dict["runs"] = row[3]
            item_dict["out"] = row[4]
            return [item_dict]

    def add_Item(self,id,request_data):
        query=f"insert into ITEM (id,name,balls,runs,out) values('{id}','{request_data['name']}','{request_data['balls']}','{request_data['runs']}','{request_data['out']}')"
        self.cursor.execute(query)
        self.conn.commit()


    def update_Item(self,id,request_data):
        query=f"update ITEM set name='{request_data['name']}',balls='{request_data['balls']}',runs='{request_data['runs']}',out='{request_data['out']}' where id = '{id}' "
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True

    def delete_Item(self, id):
        query=f"delete from ITEM where id ='{id}'"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.cursor.commit()
            return True


