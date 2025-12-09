import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import os


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.date_cols = []
        self.original_shape = self.df.shape
        self.transformations = []
        self.DATE_COLS = ["TransactionMonth", "VehicleIntroDate"]

        self.BOOL_STR_COLS = [
            "WrittenOff", "Rebuilt", "Converted", "CrossBorder"
        ]

        self.BOOL_BOOL_COLS = ["IsVATRegistered"]

        self.NUMERIC_COLS = [
            "mmcode", "Cylinders", "cubiccapacity", "kilowatts", "NumberOfDoors",
            "CustomValueEstimate", "CapitalOutstanding", "NumberOfVehiclesInFleet","RegistrationYear"
            "SumInsured", "CalculatedPremiumPerTerm", "TotalPremium", "TotalClaims"
        ]



    def load_data(self: str) -> pd.DataFrame:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        
        try:
            self.df = pd.read_csv(self.file_path, sep="|", header=0)
            print(f"✅✅ Data loaded successfully from {self.file_path}.")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.file_path} was not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the data: {e}")
    
        if self.df.empty:
            raise ValueError("The loaded data is empty.")
        
        return self.df
    

    def convert_dtypes(self):
         # -------------------------------------------------------
        # 2️⃣ Clean column names
        # -------------------------------------------------------
        self.df.columns = self.df.columns.str.strip()

        # -------------------------------------------------------
        # 3️⃣ Clean string/object columns
        # -------------------------------------------------------
        obj_cols = self.df.select_dtypes(include=["object"]).columns
        for col in obj_cols:
            self.df[col] = self.df[col].astype(str).str.strip()

        # -------------------------------------------------------
        # 4️⃣ Safe date conversion
        # -------------------------------------------------------
        for col in self.DATE_COLS:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

        # -------------------------------------------------------
        # 5️⃣ Numeric conversion with fallback
        # -------------------------------------------------------
        for col in self.NUMERIC_COLS:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # -------------------------------------------------------
        # 6️⃣ Convert boolean string columns (Yes/No → True/False)
        # -------------------------------------------------------
        for col in self.BOOL_STR_COLS:
            if col in self.df.columns:
                self.df[col] = (
                    self.df[col]
                    .str.strip()
                    .str.title()   # Ensures "yes", "YES" all become "Yes"
                    .map({"Yes": True, "No": False})
                )

            

        # -------------------------------------------------------
        # 7️⃣ Clean True/False columns
        # -------------------------------------------------------
        for col in self.BOOL_BOOL_COLS:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(bool)

        return self.df