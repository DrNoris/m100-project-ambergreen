from ambergreen.institutionManagement.entity.institution import Institution
from ambergreen.sharedInfrastructure.abstractPostgresRepository import AbstractPostgresRepository


class InstitutionDBRepository(AbstractPostgresRepository[Institution]):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)


    def add(self, institution: Institution):
        self.cursor.execute(
                "INSERT INTO " + self.getTableName() + " (name, address) VALUES (%s, %s)",
                (institution.getName(), institution.getAddress())
            )
        self.connection.commit()

    def update(self, institution: Institution):
        self.cursor.execute(
            """
            UPDATE institutions
            SET name = %s, address = %s
            WHERE id = %s
            """,
            (institution.getName(), institution.getAddress(), institution.getId())
        )
        self.connection.commit()

    def createTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS institutions (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        address TEXT NOT NULL
                    )        
        """)
        self.connection.commit()

    def getTableName(self) -> str:
        return "institutions"

    def mapRowToEntity(self, row) -> Institution:
        institution_id = int(row[0])
        name = row[1]
        address = row[2]
        return Institution(name, address, institution_id)

