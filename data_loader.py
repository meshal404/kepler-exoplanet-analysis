import os
import pandas as pd

# Where the dataset live (relative path).
DEFAULT_PATH = os.path.join("data", "cumulative.csv")

# Documenting every column we use, with its meaning and unit.
# Source: Kepler KOI table descriptions (NASA Exoplanet Archive / Kaggle page).
COLUMN_INFO = {
    # --- identifier and label ---
    "kepoi_name":        {"description": "Kepler Object of Interest (KOI) name; one row = one KOI", "unit": "none (text ID)"},
    "koi_disposition":   {"description": "Archive label: CONFIRMED, CANDIDATE or FALSE POSITIVE", "unit": "category"},
    "koi_tce_delivname": {"description": "Kepler data release (pipeline run) that produced the row", "unit": "category"},
 
    # --- transit signal features ---
    "koi_period":        {"description": "Orbital period (time for one orbit)", "unit": "days"},
    "koi_duration":      {"description": "Transit duration (how long the star is dimmed)", "unit": "hours"},
    "koi_depth":         {"description": "Transit depth (fraction of starlight blocked)", "unit": "ppm (parts per million)"},
    "koi_model_snr":     {"description": "Transit signal-to-noise ratio (signal strength)", "unit": "ratio (no unit)"},
    "koi_impact":        {"description": "Impact parameter (0 = transit across star centre, ~1 = star edge)", "unit": "fraction of star radius"},
 
    # --- planet properties ---
    "koi_prad":          {"description": "Planetary radius", "unit": "Earth radii"},
    "koi_teq":           {"description": "Planet equilibrium temperature", "unit": "Kelvin"},
    "koi_insol":         {"description": "Insolation flux (starlight received by the planet)", "unit": "Earth flux (Earth = 1)"},
 
    # --- star properties ---
    "koi_steff":         {"description": "Star effective temperature", "unit": "Kelvin"},
    "koi_slogg":         {"description": "Star surface gravity", "unit": "log10(cm/s^2)"},
    "koi_srad":          {"description": "Star radius", "unit": "Solar radii"},
    "koi_kepmag":        {"description": "Star brightness in the Kepler band", "unit": "magnitude (mag)"},
}

# The columns the analysis cannot work without.
REQUIRED_COLUMNS = set(COLUMN_INFO.keys())


# Read the CSV file int a DataFrame
def load_data(path=DEFAULT_PATH):
    #Problem 1: the file does not exist.
    if not os.path.exists(path):
        print(f"Error: file not found: {path}")
        return None

    try:
        # skips any '#' lines.
        df = pd.read_csv(path, comment="#")

    except pd.errors.EmptyDataError:
        # Problem 2: the file exists but has no data.
        print(f"Error: the file is empty: {path}")
        return None
    
    except pd.errors.ParserError as error:
        # Problem 3: the file is not a valid CSV.
        print(f"Error: could not parse {path} as CSV: {error}")
        return None

    print(f"Loaded {len(df)} rows from {path}")
    return df


# Check that every required column exists in the DataFrame.
def validate_columns(df, required=REQUIRED_COLUMNS):
    missing = required - set(df.columns)

    if missing:
        print(f"Error: missing required columns: {sorted(missing)}")
        print("Check the CSV file and the spelling in COLUMN_INFO.")

    else:
        print("All required columns are present.")

    return missing


# Print and return the basic structure of the dataset.
def inspect_data(df):

    if df is None:
        print("Nothing to inspect: no data was loaded.")
        return {}

    info = {
        "shape": df.shape,                              # (rows, columns)
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),      # column name -> type as text
    }

    rows, cols = info["shape"]
    print(f"Shape:{rows} rows x {cols} columns")
    print("Data types of the columns we use:")

    for name in sorted(REQUIRED_COLUMNS & set(df.columns)):
        print(f"  {name:<16} {info['dtypes'][name]:<10} unit: {COLUMN_INFO[name]['unit']}")


    return info




if __name__ == "__main__":
    data = load_data()
    if data is not None:
        if not validate_columns(data):
            inspect_data(data)