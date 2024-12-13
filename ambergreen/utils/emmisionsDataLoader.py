import json
from typing import Dict, List, Optional

import pandas as pd


class EmissionsDataLoader:
    def __init__(self, emission_factors: Dict[str, float]):
        self.emission_factors = emission_factors
        self.data = None

    def load_from_json(self, json_path: str) -> pd.DataFrame:
        json_data = self.process_json_path(json_path)
        return self.process_json_data(json_data)

    def load_from_json_data(self, json_data: List[Dict]) -> pd.DataFrame:
        return self.process_json_data(json_data)

    def process_json_data(self, json_data: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(json_data)

        df['date'] = pd.to_datetime(df['month'])

        df['co2_electricity'] = df['energy_kwh'] * self.emission_factors['electricity']
        df['co2_gas'] = df['gas_m3'] * self.emission_factors['gas']
        df['co2_water'] = df['water_m3'] * self.emission_factors['water']

        df['co2_emissions'] = df['co2_electricity'] + df['co2_gas'] + df['co2_water']

        self.data = df
        return df

    def get_emissions_data(self) -> Optional[pd.DataFrame]:
        return self.data

    def get_total_emissions(self) -> Optional[float]:
        if self.data is not None:
            return self.data['co2_emissions'].sum()
        return None

    @staticmethod
    def process_json_path(json_path: str) -> List[Dict]:
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        return json_data