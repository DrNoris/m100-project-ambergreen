from ambergreen.institutionUserManagement.entity.institutionUser import InstitutionUser
from ambergreen.sharedInfrastructure.abstractPostgresRepository import AbstractPostgresRepository


class InstitutionUserDBRepository(AbstractPostgresRepository[InstitutionUser]):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)

    def add(self, institutionUser: InstitutionUser):
        self.cursor.execute(
            f"INSERT INTO {self.getTableName()} "
            f"(institution_id, username, password) "
            f"VALUES (%s, %s, %s)",
            (
                institutionUser.getInstitutionId(),
                institutionUser.getUsername(),
                institutionUser.getPassword()
            )
        )
        self.connection.commit()

    def update(self, institutionUser: InstitutionUser):
        self.cursor.execute(
            f"UPDATE {self.getTableName()} SET username = %s, password = %s WHERE institution_id = %s",
            (institutionUser.getUsername(), institutionUser.getPassword(), institutionUser.getId())
        )
        self.connection.commit()

    def createTable(self):
        self.cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS institution_users (
                                                instiution_id INT PRIMARY KEY,
                                                username TEXT NOT NULL,
                                                password TEXT NOT NULL,
                                                constraint fk_institution FOREIGN KEY (instiution_id) REFERENCES Institutions(id) ON DELETE CASCADE
                                            )        
                                """)

    def getTableName(self) -> str:
        return "institution_users"

    def mapRowToEntity(self, row) -> InstitutionUser:
        institutionId = row[0]
        username = row[1]
        password = row[2]
        return InstitutionUser(username, password, institutionId)