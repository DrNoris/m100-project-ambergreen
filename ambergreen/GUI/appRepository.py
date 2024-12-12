import psycopg2

class AccountAppRepository:
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

    def getDataGraph(self, param):
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
                        consumption_data.month,
                        consumption_data.year,
                        SUM(consumption_data.energy_consumption) AS total_energy_consumption,
                        SUM(consumption_data.water_consumption) AS total_water_consumption,
                        SUM(consumption_data.gas_consumption) AS total_gas_consumption
                    FROM consumption_data
                    JOIN institutions ON consumption_data.institution_id = institutions.id
                    WHERE consumption_data.institution_id = 2
                    GROUP BY consumption_data.year, consumption_data.month
                    ORDER BY consumption_data.year DESC, consumption_data.month DESC
                    LIMIT 6;
                """,
                (id,)
            )

            data = cursor.fetchall()

            result = [
                {
                    "month": row[0],
                    "year": row[1],
                    "total_energy_consumption": row[2],
                    "total_water_consumption": row[3],
                    "total_gas_consumption": row[4]
                }
                for row in data
            ]

            return result

        except Exception as e:
            print(f"Error: {e}")

        finally:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()


class GuestAppRepository:
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
