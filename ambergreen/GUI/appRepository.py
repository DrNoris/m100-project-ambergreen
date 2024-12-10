import psycopg2

class AppRepository:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def getData(self, id):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = self.connection.cursor()

            cursor.execute(
                """
                SELECT 
                    institutions.name, 
                    institutions.address, 
                    SUM(consumption_data.energy_consumption) AS energy_consumption,
                    SUM(consumption_data.water_consumption) AS water_consumption,
                    SUM(consumption_data.gas_consumption) AS gas_consumption
                FROM consumption_data
                JOIN institutions ON consumption_data.institution_id = institutions.id
                WHERE consumption_data.institution_id = %s
                GROUP BY institutions.name, institutions.address
                """,
                (id,)
            )

            results = cursor.fetchone()

            return results

        except Exception as e:
            return str(e)

        finally:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
