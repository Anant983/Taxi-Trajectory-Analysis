import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("train.csv")

# 1. Filter rows where the "POLYLINE" column contains lists with either no pairs or only one pair of latitude and longitude
df = df[df['POLYLINE'].apply(lambda x: len(eval(x))) > 1]

# 2. For rows with duplicate "TRIP_ID", keep the one with the longer values in the "POLYLINE" column
df = df.sort_values('POLYLINE', key=lambda x: x.str.len(), ascending=False).drop_duplicates(subset='TRIP_ID', keep='first')

# 3. Change the datatype of "ORIGIN_STAD" and "ORIGIN_CALL" columns to VARCHAR
df[['ORIGIN_STAND', 'ORIGIN_CALL']] = df[['ORIGIN_STAND', 'ORIGIN_CALL']].astype(str)

# Convert the "POLYLINE" column to the desired format 'LINESTRINGM(... ..., ... ..., and so on.)'
def convert_to_linestring_with_timestamp(polyline, timestamp):
    coords = eval(polyline)
    linestring = 'LINESTRINGM('
    first_point = True
    for coord in coords:
        if not first_point:
            linestring += ', '
            timestamp += 15  # Increment timestamp by 15 seconds
        linestring += f'{coord[0]} {coord[1]} {timestamp}'
        first_point = False
    linestring += ')'
    return linestring

# Add timestamps to each point on the line string
df['POLYLINE'] = df.apply(lambda row: convert_to_linestring_with_timestamp(row['POLYLINE'], row['TIMESTAMP']), axis=1)

# 7. Remove rows where "MISSING_DATA" column is true
df = df[df['MISSING_DATA'] != True]

# 8. Remove the "DAY_TYPE" column
df = df.drop(columns=['DAY_TYPE'])

# Save the modified DataFrame to a new CSV file
df.to_csv("modified_data.csv", index=False)
