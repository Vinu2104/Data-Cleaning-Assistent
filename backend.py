import pandas as pd

class DataCleaner:

    def __init__(self, dataframe):
        self.df = dataframe

    def missing_values(self):
        return self.df.isnull().sum()

    def duplicates(self):
        return self.df[self.df.duplicated()]

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self.df

    def fill_missing(self):
        for col in self.df.columns:

            if self.df[col].dtype == "object":
                self.df[col] = self.df[col].fillna("Unknown")

            else:
                self.df[col] = self.df[col].fillna(self.df[col].mean())

        return self.df

    def outliers(self):

        numeric = self.df.select_dtypes(include='number')

        outlier_info = {}

        for col in numeric.columns:

            q1 = numeric[col].quantile(0.25)
            q3 = numeric[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outlier_info[col] = self.df[(self.df[col] < lower) | (self.df[col] > upper)]

        return outlier_info

    def clean(self):

        self.fill_missing()
        self.remove_duplicates()

        return self.df