import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import scipy
import seaborn as sns

PLOT = [False, False, False, False, False]

plt.style.use("ggplot")
# column shown
# pd.set_option("max_columns")

df = pd.read_csv("coaster_db.csv")
# df = pd.read_csv("coaster_db.csv", index_col="coaster_name")

print(df.shape)
print(df.head())
print(df.columns)
df.info()

print(df.describe())

# use only specific columns
df1 = df[["coaster_name",
          # "Length", "Speed",
          "Location", "Status",
          # "Opening date",
          # "Type",
          "Manufacturer",
          # "Height restriction", "Model", "Height",
          # "Inversions", "Lift/launch system", "Cost", "Trains", "Park section",
          # "Duration", "Capacity", "G-force", "Designer", "Max vertical angle",
          # "Drop", "Soft opening date", "Fast Lane available", "Replaced",
          # "Track layout", "Fastrack available", "Soft opening date.1",
          # "Closing date",
          #  "Opened",
          # "Replaced by", "Website",
          # "Flash Pass Available", "Must transfer from wheelchair", "Theme",
          # "Single rider line available", "Restraint Style",
          # "Flash Pass available", "Acceleration", "Restraints", "Name",
          "year_introduced",
          "latitude", "longitude", "Type_Main",
          "opening_date_clean",
          # "speed1", "speed2", "speed1_value", "speed1_unit",
          "speed_mph",
          # "height_value", "height_unit",
          "height_ft",
          "Inversions_clean", "Gforce_clean"]].copy()

df1.info()

# drop columns
df2 = df1.drop(["Manufacturer"], axis=1).copy()

# to daterime
df1["opening_date_clean"] = pd.to_datetime(df1["opening_date_clean"])
# to numeric
# pd.to_numeric(df[""])

df1.info()

# RENAME COLUMN
new_column_dict = {}
for column_name in df1.columns:
    new_column_name = "_".join(name.title() for name in column_name.split("_"))
    new_column_dict[column_name] = new_column_name

df1 = df1.rename(columns=new_column_dict).copy()
df1.info()

# check number of NaN items in columns
print(df1.isna().sum())
# check if duplicated columns
print(df1.loc[df1.duplicated()])

# check if duplicated elements in columns
print(df1.loc[df1.duplicated(subset=["Coaster_Name"])].head())

print(df1.query(("Coaster_Name == 'Crystal Beach Cyclone'")))

print(df1.loc[df1.duplicated(subset=["Coaster_Name", "Location", "Opening_Date_Clean"])])
df1 = (df1.loc[~df1.duplicated(subset=["Coaster_Name", "Location", "Opening_Date_Clean"])]
       .reset_index(drop=True).copy())

print(df1.shape)
print(df1.isna().sum())
plot = df1["Year_Introduced"].value_counts().head(10).plot(
    kind="bar",
    title="Top Years coaster Introduced", )
plot.set_xlabel("Year introduced")
plot.set_ylabel("Count")

plt.show()

plot_2 = df1["Speed_Mph"].plot(
    kind="hist",
    bins=20,
    title="Coaster Speed mph", )
plt.show()

plot_3 = df1["Speed_Mph"].plot(
    kind="kde",
    title="Coaster Speed mph")
plot_3.set_xlabel("speed (mph)")
plt.show()

scatter_plot = df1.plot(kind="scatter",
                        x="Speed_Mph",
                        y="Height_Ft",
                        title="Coaster Speed vs Height")
plt.show()

sns.scatterplot(data=df1,
                x="Speed_Mph",
                y="Height_Ft",
                hue="Year_Introduced")
plt.show()

# many charts depicting relationships between data.
sns.pairplot(data=df1,
             vars=["Year_Introduced", "Speed_Mph", "Height_Ft","Inversions_Clean", "Gforce_Clean"],
             # x_vars=["Speed_Mph"],
             # y_vars=["Height_Ft"],
             hue="Type_Main")
plt.show()

# drop na values
corr = (df1[["Year_Introduced", "Speed_Mph", "Height_Ft","Inversions_Clean", "Gforce_Clean"]]
        .dropna().corr())

sns.heatmap(corr, annot=True)
plt.show()


# finding locations with the highest mean speed of Coasters
example = (df1.query("Location != 'Other'")
           .groupby("Location")["Speed_Mph"]
           .agg(["mean", "count"])
           .query("count >= 10")
           .sort_values("mean")["mean"])

example.plot(kind="barh", figsize=(12, 5), title=("Average Coaster Speed by location"))
plt.show()

print(example)
