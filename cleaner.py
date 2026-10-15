
import pandas as pd


class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()

    def missing_values(self):
        return self.df.isnull().sum()

    def count_missing(self):
        return int(self.df.isnull().sum().sum())

    def duplicates(self):
        return self.df[self.df.duplicated()]

    def count_duplicates(self):
        return int(self.df.duplicated().sum())

    def count_outliers(self):
        numeric = self.df.select_dtypes(include="number")
        total = 0

        for col in numeric.columns:
            values = numeric[col].dropna()

            if values.empty:
                continue

            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1

            if iqr == 0:
                continue

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            total += int(
                ((self.df[col] < lower) |
                 (self.df[col] > upper)).sum()
            )

        return total

    def clean(self):
        cleaned = self.df.copy()

        # Fill missing numerical values with the median
        for col in cleaned.select_dtypes(include="number").columns:
            if cleaned[col].isnull().any():
                median = cleaned[col].median()

                if pd.notna(median):
                    cleaned[col] = cleaned[col].fillna(median)

        # Fill missing text values
        for col in cleaned.select_dtypes(
            include=["object", "string", "category"]
        ).columns:
            cleaned[col] = cleaned[col].fillna("Unknown")

        # Remove duplicate rows
        cleaned = cleaned.drop_duplicates()

        return cleaned
