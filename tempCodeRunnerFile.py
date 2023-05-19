def update_data(self, tag : str, pattern : str, response : str) ->None :
        self.cursor.execute(f"""
        UPDATE data_table 
        SET pattern = '{pattern}'
        response = '{response}'
        WHERE tag = '{tag}'
        """)
        self.connection.commit()