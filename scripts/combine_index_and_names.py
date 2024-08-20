import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Read in the files
mapmakers_df = pd.read_csv("outputs/mapmakers.csv")
index_df = pd.read_csv("outputs/index_to_place_and_date_v3.csv")

# Merge the DataFrames
combined_df = pd.merge(index_df, mapmakers_df, left_on="mapmaker_id", right_on="Mapmaker ID", how="left")
# What's up with left and right?
# The left dataframe is index_df (it's on the left side of the merge function)
# The right dataframe is mapmakers_df (it's on the right side of the merge function)
# We need to specify which columns to merge on
# index_df has a column called "mapmaker_id"
# mapmakers_df has a column called "Mapmaker ID"
# The final argument, how="left", specifies that we want to keep all the rows from index_df

# Keep the naming of the columns consistent
combined_df = combined_df.drop(columns=["Mapmaker ID"])
combined_df = combined_df.rename(columns={"Mapmaker Name": "mapmaker_name"})

# Move the mapmaker_name column to the front
cols = combined_df.columns.tolist()
cols = cols[-1:] + cols[:-1]
combined_df = combined_df[cols]

# Visually see where the mapmaker names are missing
# Likely due to incorrect OCR in the index file
rows_with_no_mapmaker = combined_df[combined_df["mapmaker_name"].isnull()]
logging.info(f"Found {len(rows_with_no_mapmaker)} rows with no mapmaker")
logging.info(rows_with_no_mapmaker)

# Save the combined DataFrame to a CSV file
combined_df.to_csv("outputs/index_to_place_and_date_and_mapmaker_names.csv", index=False) 

