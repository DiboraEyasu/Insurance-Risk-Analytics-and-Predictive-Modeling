import pandas as pd
import numpy as np


class Cleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.threshold = 30

    def remove_nulls(self):
        print("Shape of data before handling nulls:", self.df.shape)
        # Get the count of nulls in each column
        null_counts = self.df.isnull().sum()
                # Get the percentage of nulls
        null_percentages = (self.df.isnull().sum() / len(self.df)) * 100

        # Combine them into a handy summary DataFrame
        missing_data_summary = pd.DataFrame({
            'Null Count': null_counts,
            'Null Percentage': null_percentages
        })
        # Impute TotalClaims with 0 where it's missing
        self.df['TotalClaims'].fillna(0, inplace=True)
        print("✅ 'TotalClaims' NaNs filled with 0.")
        cols_to_drop = missing_data_summary[missing_data_summary['Null Percentage'] > 70].index

        if not cols_to_drop.empty:
            self.df.drop(columns=cols_to_drop, inplace=True)
            print(f"✅ Dropped columns with >{70}% nulls: {list(cols_to_drop)}")
        else:
            print("✅ No columns exceeded the null percentage threshold.")

            # Define your critical columns
        critical_cols = [
            'SumInsured', 'TotalPremium', 'CalculatedPremiumPerTerm',
            'Make', 'Model', 'RegistrationYear', 'Province'
        ]

        # Keep only the critical columns that actually exist in the DataFrame
        existing_critical_cols = [col for col in critical_cols if col in self.df.columns]

        # Drop rows where any of these critical columns are null
        initial_rows = len(self.df)
        self.df.dropna(subset=existing_critical_cols, inplace=True)
        rows_dropped = initial_rows - len(self.df)

        if rows_dropped > 0:
            print(f"✅ Dropped {rows_dropped} rows with missing critical information.")
        else:
            print("✅ No rows with missing critical information found.")


    def drop_duplicate_values(self):
        initial_shape = self.df.shape
        self.df.drop_duplicates(inplace=True)
        final_shape = self.df.shape
        print(f"✅ Dropped {initial_shape[0] - final_shape[0]} duplicate rows.")

        return self.df
    

    def logical_data_filter(self):
        initial_rows = len(df)

        # Filter for valid premiums
        df = df[df['TotalPremium'] > 0]

        # Filter for realistic registration years
        current_year = pd.to_datetime('today').year
        df = df[(df['RegistrationYear'] > 1980) & (df['RegistrationYear'] <= current_year)]

        rows_dropped = initial_rows - len(df)

        if rows_dropped > 0:
            print(f"✅ Dropped {rows_dropped} rows with logically invalid data (e.g., zero premium, invalid year).")
        else:
            print("✅ No logically invalid rows found.")