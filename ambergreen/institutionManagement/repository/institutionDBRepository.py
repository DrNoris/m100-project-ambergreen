from ambergreen.institutionManagement.entity.institution import Institution
from ambergreen.sharedInfrastructure.abstractPostgresRepository import AbstractPostgresRepository


class InstitutionDBRepository(AbstractPostgresRepository[Institution]):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)


    def add(self, institution: Institution):
        self.cursor.execute(
                "INSERT INTO " + self.getTableName() + " (name, address, energy_provider, water_provider, gas_provider) VALUES (%s, %s, %s, %s, %s)",
                (institution.getName(), institution.getAddress(), institution.getEnergyProvider(), institution.getWaterProvider(), institution.getGasProvider())
            )
        self.connection.commit()

    def update(self, institution: Institution):
        self.cursor.execute(
            """
            UPDATE institutions
            SET name = %s, address = %s, energy_provider = %s, water_provider = %s, gas_provider = %s
            WHERE id = %s
            """,
            (institution.getName(), institution.getAddress(), institution.getEnergyProvider(), institution.getWaterProvider(), institution.getGasProvider(), institution.getId())
        )
        self.connection.commit()

    def createTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS institutions (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        address TEXT NOT NULL,
                        energy_provider TEXT NOT NULL,
                        water_provider TEXT NOT NULL,
                        gas_provider TEXT NOT NULL,
                        foreign key (energy_provider) REFERENCES providers(provider_name),
                        foreign key (water_provider) REFERENCES providers(provider_name),
                        foreign key (gas_provider) REFERENCES providers(provider_name)
                )
        """)
        self.connection.commit()

    def getTableName(self) -> str:
        return "institutions"

    def mapRowToEntity(self, row) -> Institution:
        institution_id = int(row[0])
        name = row[1]
        address = row[2]
        if row[3] is None:
            energy_provider = None
        else: energy_provider = row[3]

        if row[4] is None:
            water_provider = None
        else: water_provider = row[4]

        if row[5] is None:
            gas_provider = None
        else: gas_provider = row[5]

        return Institution(name, address, energy_provider, water_provider, gas_provider, institution_id)

