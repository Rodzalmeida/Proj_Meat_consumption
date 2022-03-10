# import the necessary packages

import pandas as pd
import lxml
import geopandas
import folium as folium

# Get the data from the web and subset the first table found, also subset only the necessary data
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_meat_consumption'
table_meat = pd.read_html(url)

table = table_meat[0]
table_sel = table[["Country","kg/person (2002)[9][note 1]"]]

# optmize the dataframe, its optional
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 200)

# Get the map canvas, the source is the geopandas website in this case
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# Merge the data from the meat consumption table and the data from the map selected using the country name column
ftable = world.merge(table_sel, how='left', left_on=['name'], right_on=['Country'])

# clean the data of missing values so they dont show (NA values)
ftable = ftable.dropna(subset=['kg/person (2002)[9][note 1]'])

# Map setup from the geopandas website, standard config changing only the necessary inputs
mapa = folium.Map()

folium.Choropleth(
   geo_data=ftable,
   name="choropleth",
   data=ftable,
   columns=["Country", "kg/person (2002)[9][note 1]"],
   key_on="feature.properties.name",
   fill_color="YlGn",
   fill_opacity=0.7,
   line_opacity=0.2,
   legend_name="Meet consumption per Country"
    ).add_to(mapa)

# Save the map on a HTML file for you to open and see in your browser
mapa.save('meat.html')