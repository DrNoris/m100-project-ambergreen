import psycopg2

class LoginDBRepository:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def login(self, username, password):
        try:
            # Establish the database connection
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = self.connection.cursor()

            # Execute the query to fetch user and institution data
            cursor.execute(
                """
                SELECT 
                    institution_users.username, 
                    institution_users.password,
                    institution_users.institution_id,
                    institutions.name AS institution_name,
                    institutions.address AS institution_address
                FROM institution_users
                JOIN institutions ON institution_users.institution_id = institutions.id
                WHERE institution_users.username = %s AND institution_users.password = %s
                """,
                (username, password)
            )

            # Fetch the result
            user_data = cursor.fetchone()

            if not user_data:
                return {"success": False, "message": "Invalid username or password"}

            result = {
                "success": True,
                "institution": {
                    "id": user_data[2],
                    "name": user_data[3],
                    "address": user_data[4],
                }
            }
            return result

        except Exception as e:
            return {"success": False, "message": str(e)}

        finally:
            # Ensure the connection is closed
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
