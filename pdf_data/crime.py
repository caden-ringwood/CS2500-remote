import pandas as pd
import tabula
import numpy as np

# Path to your PDF
pdf_path = "crime_data.pdf"

try:
    # Extract tables from the PDF
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

    if not tables:
        raise ValueError("No tables found in the PDF.")

    cleaned_tables = []

    for table in tables:
        df = table.dropna(how='all').dropna(axis=1, how='all')

        # Find the header row
        header_idx_series = df[df.iloc[:,0].astype(str).str.contains('Country|Year', na=False)].index
        if not header_idx_series.empty:
            header_idx = header_idx_series[0]
            # Use only English part of header
            df.columns = [str(col).split('/')[0].strip() for col in df.iloc[header_idx]]
            df = df[(header_idx+1):].reset_index(drop=True)
        else:
            # If no header found, keep as-is
            df = df.reset_index(drop=True)

        # Remove French duplicates
        mask_french_dup = df.iloc[:,0].astype(str).str.startswith(('Pays','Total, tous'))
        df = df[~mask_french_dup]

        # Remove French region rows
        french_keywords = [
            'Afrique', 'septentrionale', 'Amériques', 'Asie', 'Caraïbes', 'orientale', 'du Sud-Est',
            'sub-saharienne', 'Amérique', 'latine', 'et', 'Central', 'Europe', 'occidentale',
            'méridionale', 'de l’Est', 'Océanie', 'Australie', 'Nouvelle-Zélande',
            'Micronésie', 'Mélanésie', 'Polynésie'
        ]
        mask_french_region = df.iloc[:,0].astype(str).str.contains('|'.join(french_keywords), na=False)
        df = df[~mask_french_region]

        # Replace '...' with NaN
        df = df.replace('...', np.nan)

        # Forward-fill country/area column
        df.iloc[:,0] = df.iloc[:,0].ffill()

        # Keep only columns with actual data
        df = df.loc[:, df.notna().any()]

        # Convert numeric columns (skip first column)
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        cleaned_tables.append(df)

    # Concatenate all cleaned tables
    final_df = pd.concat(cleaned_tables, ignore_index=True)
    print(final_df.head(10))

except Exception as e:
    print(f"Error extracting tables: {e}")
