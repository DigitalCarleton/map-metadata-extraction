import re 
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Read in the file
index_df = pd.read_csv("outputs/index_to_place_and_date_and_mapmaker_names_with_date_estimates.csv")

# Add a column for the object type
index_df["Map or Book"] = None

# Loop through the rows, even though this isn't typically the best way to do things in pandas,
# it's clear and the data is small enough that performance isn't a concern
for i, row in index_df.iterrows():
    # if the first character is a number, then it's a map
    if row["map_or_book_id"][0].isdigit():
        index_df.at[i, "Map or Book"] = "Map"

    # if the first character is a letter, then it's a book
    elif row["map_or_book_id"][0].isalpha():
        index_df.at[i, "Map or Book"] = "Book"

    else:
        logging.warning(f"Could not determine the object type for row {i}. map_or_book_id: {row['map_or_book_id']}")

# Add a column to denote whether the map/book is the original edition or not
index_df["Original Edition"] = None

# Loop through the rows
for i, row in index_df.iterrows():
    # if there's a period in the map_or_book_id, then it's not the original edition
    if "." in row["map_or_book_id"]:
        index_df.at[i, "Original Edition"] = "No"

    # if there's no period in the map_or_book_id, then it's the original edition
    else:
        index_df.at[i, "Original Edition"] = "Yes"

# Save the DataFrame to a CSV file
index_df.to_csv("outputs/index_to_place_and_date_mapmaker_names_dates_estimates_object_types.csv", index=False)