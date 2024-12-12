from ambergreen.providersManagement.entity.provider import Provider
from ambergreen.sharedInfrastructure.abstractPostgresRepository import AbstractPostgresRepository


class ProviderDBRepository(AbstractPostgresRepository[Provider]):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)

    def add(self, provider: Provider):
        self.cursor.execute(
            "INSERT INTO providers (provider_name, emission_factor, service_provided) VALUES (%s, %s, %s)",
            (provider.getId(), provider.getEmissionFactor(), provider.getServiceProvided())
        )
        self.connection.commit()

    def update(self, provider: Provider):
        self.cursor.execute(
            """
            UPDATE providers
            SET emission_factor = %s, service_provided = %s
            WHERE provider_name = %s
            """,
            (provider.getEmissionFactor(), provider.getServiceProvided(), provider.getId())
        )
        self.connection.commit()

    def createTable(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS providers (
                provider_name TEXT PRIMARY KEY,
                emission_factor DECIMAL(10, 2),
                service_provided TEXT
            )
        """)
        self.connection.commit()

    def getTableName(self) -> str:
        return "providers"

    def mapRowToEntity(self, row) -> Provider:
        provider_name = row[0]
        emission_factor = float(row[1]) if row[1] is not None else None
        service_provided = row[2]
        return Provider(provider_name, emission_factor, service_provided)

    def get(self, provider_name) -> Provider | None:
        if isinstance(provider_name, str):
            self.cursor.execute(
                "SELECT * FROM " + self.getTableName() + " WHERE provider_name = %s",
                (provider_name,)
            )
            result = self.cursor.fetchone()

            if result is None:
                raise KeyError(f"Entity with provider name {provider_name} not found")

            return self.mapRowToEntity(result)