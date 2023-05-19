import sqlite3




class Mydb:
    '''
    Database class
    '''

    def __init__(self) -> None:
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        #self.cursor.execute (f"""
        #PRAGMA table_info(data_table);
        #""")
#
        #res = self.cursor.fetchall()
        #print(res)

    def load_data(self, tag: str) -> str:
        self.cursor.execute(f"""
        SELECT * from data_table 
        WHERE tag = '{tag}';
        """)

        res = self.cursor.fetchall()
        try:
            return res[0][2]
        except IndexError:
            return "No such tag"

    def load_data_system(self, tag: str) -> str:
        self.cursor.execute(f"""
        SELECT * from system_table 
        WHERE tag = '{tag}';
        """)

        res = self.cursor.fetchall()
        try:
            return res[0][1]
        except IndexError:
            return "No such tag"

    def insert_data(self, tag: str, pattern: str, response: str) -> None:
        self.cursor.execute(f"""
        INSERT INTO data_table VALUES 
        ('{tag}', '{pattern}', '{response}');
        """)

        self.connection.commit()

    def delete_data(self, tag: str) -> None:
        self.cursor.execute(f"""
        DELETE from data_table 
        WHERE tag = '{tag}';
        """)
        self.connection.commit()
    
    def update_data2(self, tag : str, pattern : str, response : str) ->None :
        self.cursor.execute(f"""
        UPDATE data_table 
        SET patterns = '{pattern}'
        WHERE tag = '{tag}';
        """)
        self.cursor.execute(f"""
        UPDATE data_table 
        SET responses = '{response}'
        WHERE tag = '{tag}';
        """)

        self.connection.commit()

    def set_attr(self, tag: str, value: str) -> None:
        self.cursor.execute(f"""
        INSERT INTO system_table VALUES 
        ('{tag}', '{value}');
        """)

        self.connection.commit()

    def get_attr(self, attr: str) -> str:
        self.cursor.execute(f"""
        SELECT value from system_table
        WHERE tag = '{attr}'
        """)
        l = self.cursor.fetchall()
        try:
            s = list(l[0])[0]

        except IndexError:
            return ''
        return s

    def update_data(self, tag: str, value: str) -> None:
        self.cursor.execute(f"""
        UPDATE system_table 
        SET value = '{value}'
        WHERE tag = '{tag}'
        """)
        self.connection.commit()

    def get_tags(self) -> list:
        self.cursor.execute("""
        SELECT tag from data_table;
        """)

        l = self.cursor.fetchall()
        res = []
        try:
            for li in l:
                li = list(li)
                res.append(li[0])
        except IndexError:
            pass
        return res

    def get_responses(self, tag: str) -> list:
        self.cursor.execute(f"""
        SELECT responses from data_table
        WHERE tag = '{tag}'
        """)
        l = self.cursor.fetchall()
        try:
            s = list(l[0])[0]
            res = s.split('&')
            res.reverse()
            res.pop()
        except IndexError:
            return []
        return res

    def get_patterns(self, tag: str) -> list:
        self.cursor.execute(f"""
        SELECT patterns from data_table
        WHERE tag = '{tag}'
        """)
        l = self.cursor.fetchall()
        try:
            s = list(l[0])[0]
            res = s.split('&')
            res.reverse()
            res.pop()
        except IndexError:
            return []
        return res


db = Mydb()

db.update_data2('test', '&hello&', '&hi&')