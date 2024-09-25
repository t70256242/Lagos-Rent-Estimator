import json
from sklearn.tree import DecisionTreeRegressor
import joblib
import pandas as pd


class Artifacts:
    def __init__(self):
        self.columns = []
        self.location = []
        self.p_type = []
        self.mean_price_list = []
        self.model = None
        self.load_artifacts()

    def load_artifacts(self):
        with open("./static/assets/rent_house_columns.json", "r") as f:
            data = json.load(f)['data_columns']
            self.columns = data
            self.location = data[14:]
            self.p_type = data[2:-27]

        with open("./static/assets/mean_house_rent.json", "r") as f:
            bata = json.load(f)
            self.mean_price_list = bata

        self.model = joblib.load("./static/assets/rent_house_prices_model.joblib")

