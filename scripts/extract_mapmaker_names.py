import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Open up the cleaned file
with open('cleaned-ocr-text/table_of_contents.txt') as f:
    table_of_contents = f.read()

# Split the table of contents into a list of lines
table_of_contents = table_of_contents.split('\n')

# Create a list to store the names of the mapmakers
mapmakers = []

# Pull out each mapmaker ID number and name
for line in table_of_contents:
    # grab everything before the /
    mapmaker_id = line.split('/')[0]
    mapmaker_id = mapmaker_id.strip()

    # grab everything before the dots
    rest_of_line = line.split('/')[1]
    mapmaker_name = rest_of_line.split('.')[0]
    mapmaker_name = mapmaker_name.strip()

    # Append the mapmaker ID and name to the list
    mapmakers.append({"Mapmaker ID": mapmaker_id, "Mapmaker Name": mapmaker_name})

logging.info(f"Found {len(mapmakers)} mapmakers")

# Convert the list of mapmakers to a pandas DataFrame
mapmakers_df = pd.DataFrame(mapmakers)

# Sort by the mapmaker ID for humans
mapmakers_df["Mapmaker ID"] = mapmakers_df["Mapmaker ID"].astype(int)
mapmakers_df = mapmakers_df.sort_values(by="Mapmaker ID")

logging.info("Mapmakers DataFrame:")
logging.info(mapmakers_df)
logging.info("Mapmakers DataFrame datatypes:")
logging.info(mapmakers_df.dtypes)

# Save the mapmakers DataFrame to a CSV file
mapmakers_df.to_csv("outputs/mapmakers.csv", index=False)