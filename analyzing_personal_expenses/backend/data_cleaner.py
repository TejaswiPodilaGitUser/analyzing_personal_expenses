class DataCleaner:
    def __init__(self, df, categories_df, subcategories_df):
        self.df = df
        self.categories_df = categories_df
        self.subcategories_df = subcategories_df


    def fill_missing_subcategory_name(self):
        """Fills missing 'subcategory_name' with the mode (most frequent value) of the respective category."""
        # Fill missing subcategory_name using the mode (most frequent value) per category
        self.df['subcategory_name'] = self.df.groupby('category_name')['subcategory_name'].transform(
            lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 'Miscellaneous')
        )

    def fill_missing_amount_paid(self):
        """Fills missing 'amount_paid' with the mean of the respective subcategory."""
        # Fill missing 'amount_paid' with the mean value of 'amount_paid' per subcategory_name
        self.df['amount_paid'] = self.df.groupby('subcategory_name')['amount_paid'].transform(
            lambda x: x.fillna(x.mean() if not x.isna().all() else 0)
        )

    def drop_null_subcategory_and_amount(self):
        """Drops rows where both 'subcategory_name' and 'amount_paid' are NaN."""
        self.df.dropna(subset=['subcategory_name', 'amount_paid'], how='all', inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def fill_missing_category_id(self):
        """Fills missing category_id based on category_name."""
        if 'category_name' in self.categories_df.columns and 'category_id' in self.categories_df.columns:
            self.df = self.df.merge(self.categories_df[['category_name', 'category_id']], on='category_name', how='left')
        else:
            raise KeyError("Missing 'category_name' or 'category_id' in categories_df.")
        
        # Fill missing category_id with -1 for consistency
        self.df['category_id'] = self.df['category_id'].fillna(-1)

    def fill_missing_subcategory_id(self):
        """Fills missing subcategory_id based on subcategory_name."""
        if 'subcategory_name' in self.subcategories_df.columns and 'subcategory_id' in self.subcategories_df.columns:
            self.df = self.df.merge(
                self.subcategories_df[['subcategory_name', 'subcategory_id']],
                on='subcategory_name',
                how='left'
            )
        else:
            raise KeyError("Missing 'subcategory_name' or 'subcategory_id' in subcategories_df.")
        
        # Fill missing subcategory_id with -1 for consistency
        self.df['subcategory_id'] = self.df['subcategory_id'].fillna(-1)

    def clean_data(self):
        """Performs all data cleaning steps."""

        self.drop_null_subcategory_and_amount()  # Drop rows where both 'subcategory_name' and 'amount_paid' are NaN
        self.fill_missing_subcategory_name()  # Fill missing subcategory_name with mode
        self.fill_missing_amount_paid()  # Fill missing amount_paid with mean
        self.fill_missing_category_id()  # Fill missing category_id based on category_name
        self.fill_missing_subcategory_id()  # Fill missing subcategory_id based on subcategory_name
        
        return self.df

