import os
import pickle

import pandas as pd
from prophet import Prophet


class EmissionsPredictor:
    """
    Enhanced Predictor that accounts for equipment upgrades and climate change
    """

    def __init__(self,
                 seasonality_mode: str = 'multiplicative',
                 model_dir: str = 'models',
                 equipment_growth_rate: float = 0.03,
                 temperature_trend: float = 0.02):
        """
        Initialize the enhanced predictor

        Args:
            seasonality_mode: Type of seasonality
            model_dir: Directory for model storage
            equipment_growth_rate: Annual rate of increase in equipment power consumption
            temperature_trend: Annual rate of increase in HVAC needs due to climate change
        """
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            seasonality_mode=seasonality_mode
        )
        self.equipment_growth_rate = equipment_growth_rate
        self.temperature_trend = temperature_trend
        self.model_dir = model_dir
        self.trained = False
        self.forecast = None
        self.training_end_date = None

        os.makedirs(model_dir, exist_ok=True)

    def add_growth_regressors(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add additional regressors for equipment and climate trends
        """
        start_date = df['ds'].min()
        df['years_from_start'] = (df['ds'] - start_date).dt.total_seconds() / (365.25 * 24 * 60 * 60)

        df['equipment_factor'] = (1 + self.equipment_growth_rate) ** df['years_from_start']

        df['temperature_factor'] = (1 + self.temperature_trend) ** df['years_from_start']

        return df

    def train(self, df: pd.DataFrame) -> None:
        """
        Train the model with additional regressors
        """
        prophet_df = pd.DataFrame({
            'ds': df['date'],
            'y': df['co2_emissions']
        })

        prophet_df = self.add_growth_regressors(prophet_df)

        self.model.add_regressor('equipment_factor')
        self.model.add_regressor('temperature_factor')

        self.model.fit(prophet_df)
        self.trained = True
        self.training_end_date = df['date'].max()

    def predict(self, months_ahead: int = 24) -> pd.DataFrame:
        """
        Generate predictions incorporating growth factors
        """
        if not self.trained:
            raise RuntimeError("Model must be trained before making predictions")

        future_dates = self.model.make_future_dataframe(periods=months_ahead, freq='M')

        future_dates = self.add_growth_regressors(future_dates)

        self.forecast = self.model.predict(future_dates)

        current_date = self.training_end_date

        predictions = pd.DataFrame({
            'date': self.forecast['ds'],
            'predicted_co2': self.forecast['yhat'],
            'equipment_trend': self.forecast['equipment_factor'],
            'temperature_trend': self.forecast['temperature_factor']
        })

        predictions = predictions[predictions['date'] > current_date]

        return predictions

    def save_model(self, model_name: str) -> str:
        """Save the trained model with its parameters"""
        if not self.trained:
            raise RuntimeError("Cannot save untrained model")

        if not model_name.endswith('.pkl'):
            model_name += '.pkl'

        model_path = os.path.join(self.model_dir, model_name)

        model_data = {
            'model': self.model,
            'trained': self.trained,
            'forecast': self.forecast,
            'equipment_growth_rate': self.equipment_growth_rate,
            'temperature_trend': self.temperature_trend,
            'training_end_date': self.training_end_date
        }

        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)

        return model_path

    def load_model(self, model_name: str) -> None:
        """Load a trained model with its parameters"""
        if not model_name.endswith('.pkl'):
            model_name += '.pkl'

        model_path = os.path.join(self.model_dir, model_name)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No model found at {model_path}")

        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.trained = model_data['trained']
        self.forecast = model_data['forecast']
        self.equipment_growth_rate = model_data['equipment_growth_rate']
        self.temperature_trend = model_data['temperature_trend']
        self.training_end_date = model_data['training_end_date']