import geopandas as gpd

def load_haz_waste_shp(haz_waste_shp_url='https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/HW_Sites_EPSG4326.zip'):
    # Description: Load hazardous waste facility shapefile
    # haz_waste_shp_url: Hazardous waste facility shapefile URL
    haz_waste_gdf = gpd.read_file(haz_waste_shp_url)
    return haz_waste_gdf
import geopandas as gpd

def load_tract_shp(tract_shp_url='https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/tract_37_EPSG4326.zip'): 
    """
    Load NC tract boundary shapefile
    tract_shp_url: Tract boundary shapefile URL
    """
    tract_gdf = gpd.read_file(tract_shp_url)

    return tract_gdf
def spatial_join(haz_waste_gdf, tract_gdf):
    """
    Spatially joining Hazardous Waste GeoDataFrame with NC Tracts GeoDataFrame
    haz_waste_gdf: Hazardous waste facility GeoDataFrame
    tract_gdf: NC tract boundary GeoDataFrame
    """
    # make sure both GeoDataFrames are in the same projection
    haz_waste_gdf = haz_waste_gdf.to_crs(tract_gdf.crs)

    # perform the spatial join
    joined_gdf = gpd.sjoin(tract_gdf, haz_waste_gdf, how="inner", op="intersects")

    # Removing duplicate rows that may have been made in the join
    joined_gdf = joined_gdf.drop_duplicates(subset=["GEOID"])


    return joined_gdf
import pandas as pd

def load_tract_pop_csv(tract_pop_csv_url='https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/NC_tract_population.csv'):
    """
    Load NC tract population CSV

    Parameters:
    tract_pop_csv_url: string (default='https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/NC_tract_population.csv')
        URL string to the location of the NC tract population CSV

    Returns:
    pandas DataFrame
        DataFrame of the loaded NC tract population CSV

    """
    tract_pop_df = pd.read_csv(tract_pop_csv_url, dtype={'GEOID': str})
    tract_pop_df.dropna(subset=['GEOID', 'TotalPopulation'], inplace=True)
    return tract_pop_df
def join_pop(joined_gdf, tract_pop_df):
    """
    Join population data with spatially joined dataset for Hazardous Waste Sites and NC Tracts

    Parameters:
    joined_gdf: GeoPandas GeoDataFrame
        GeoDataFrame of spatially joined Hazardous Waste Sites with NC Tracts
    tract_pop_df: Pandas DataFrame
        DataFrame of tract population data

    Returns:
    GeoPandas GeoDataFrame
        Merged GeoDataFrame with population data
    """
    # convert the GEOID column to string in both dataframes to ensure joining success
    joined_gdf['GEOID'] = joined_gdf['GEOID'].astype(str)
    tract_pop_df['GEOID'] = tract_pop_df['GEOID'].astype(str)

    # merge the dataframes using GEOID as the key, keep only the columns needed
    pop_joined_gdf = joined_gdf.merge(tract_pop_df[['GEOID', 'TotalPopulation']],
                                      on='GEOID', how='left')

    return pop_joined_gdf
def compute_pop(pop_joined_gdf):
    """
    Compute total population for tracts with hazardous waste sites

    Parameters:
    pop_joined_gdf: GeoPandas GeoDataFrame
        GeoDataFrame of population data for NC tracts with hazardous waste sites

    Returns:
    int
        Total population for tracts with hazardous waste sites
    """
    # Calculate the total population in the hazardous waste sites in NC
    total_pop = pop_joined_gdf['TotalPopulation'].sum()

    return total_pop
import matplotlib.pyplot as plt

def generate_choropleth_map(tract_gdf, tract_pop_df):
    """
    Generate population choropleth map for all tract polygons

    Parameters:
    tract_gdf: geopandas GeoDataFrame
        GeoDataFrame of the tract boundaries
    tract_pop_df: pandas DataFrame
        DataFrame of the population per tract

    Returns:
    matplotlib Figure
        Figure of the choropleth map of population for all tract polygons
    """

    # Join tract polygons GeoDataFrame with tract population DataFrame, by 'GEOID' column
    tract_gdf['GEOID'] = tract_gdf['GEOID'].astype(int)
    tract_pop_df['GEOID'] = tract_pop_df['GEOID'].astype(int)
    tract_gdf = tract_gdf.merge(tract_pop_df, on='GEOID')

    # Generate the choropleth map
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    tract_gdf.plot(column='TotalPopulation', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    ax.set_title('Population by Tract', fontdict={'fontsize': '25', 'fontweight' : '3'})
    ax.annotate('Source: US Census Bureau',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

    return fig
import matplotlib.pyplot as plt
def highlight_polygons(pop_joined_gdf, choropleth_map):
    """
    Highlight borders of tracts that have hazardous waste facilities

    Parameters:
    pop_joined_gdf : geopandas.GeoDataFrame
    The geodataframe that includes the tract boundaries that have hazardous waste facilities.

    choropleth_map : matplotlib.Figure
    The choropleth map figure to which the highlight of hazardous waste facility containing tracts will be added.

    Returns:
    matplotlib.Figure
        The choropleth map with highlighted borders of tracts that have hazardous waste facilities.
    """
    # map plotting
    ax = choropleth_map.axes[0]
    pop_joined_gdf.plot(ax=ax, color='none', edgecolor='black')
    ax.set_axis_off()
    plt.show()
    return choropleth_map
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def assembly_solution():
    def load_haz_waste_shp(haz_waste_shp_url='https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/HW_Sites_EPSG4326.zip'):
        haz_waste_gdf = gpd.read_file(haz_waste_shp_url)
        return haz_waste_gdf

    def load_tract_shp(tract_shp_url='https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/tract_37_EPSG4326.zip'):
        tract_gdf = gpd.read_file(tract_shp_url)
        return tract_gdf

    def spatial_join(haz_waste_gdf, tract_gdf):
        haz_waste_gdf = haz_waste_gdf.to_crs(tract_gdf.crs)
        joined_gdf = gpd.sjoin(tract_gdf, haz_waste_gdf, how="inner", op="intersects")
        joined_gdf = joined_gdf.drop_duplicates(subset=["GEOID"])
        return joined_gdf

    def load_tract_pop_csv(tract_pop_csv_url='https://github.com/gladcolor/LLM-Geo/raw/master/overlay_analysis/NC_tract_population.csv'):
        tract_pop_df = pd.read_csv(tract_pop_csv_url, dtype={'GEOID': str})
        tract_pop_df.dropna(subset=['GEOID', 'TotalPopulation'], inplace=True)
        return tract_pop_df

    def join_pop(joined_gdf, tract_pop_df):
        joined_gdf['GEOID'] = joined_gdf['GEOID'].astype(str)
        tract_pop_df['GEOID'] = tract_pop_df['GEOID'].astype(str)
        pop_joined_gdf = joined_gdf.merge(tract_pop_df[['GEOID', 'TotalPopulation']],on='GEOID', how='left')
        return pop_joined_gdf

    def compute_pop(pop_joined_gdf):
        total_pop = pop_joined_gdf['TotalPopulation'].sum()
        return total_pop

    def generate_choropleth_map(tract_gdf, tract_pop_df):
        tract_gdf['GEOID'] = tract_gdf['GEOID'].astype(int)
        tract_pop_df['GEOID'] = tract_pop_df['GEOID'].astype(int)
        tract_gdf = tract_gdf.merge(tract_pop_df, on='GEOID')
        tract_gdf = tract_gdf.dropna(subset=['TotalPopulation'])
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))
        tract_gdf.plot(column='TotalPopulation', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
        ax.set_title('Population by Tract', fontdict={'fontsize': '25', 'fontweight' : '3'})
        ax.annotate('Source: US Census Bureau',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
        return fig

    def highlight_polygons(pop_joined_gdf, choropleth_map):
        ax = choropleth_map.axes[0]
        pop_joined_gdf.plot(ax=ax, color='none', edgecolor='black')
        ax.set_axis_off()
        plt.show()
        return choropleth_map

    tract_shp = load_tract_shp()
    haz_waste_shp = load_haz_waste_shp()
    joined_df = spatial_join(haz_waste_shp, tract_shp)

    tract_pop_df = load_tract_pop_csv()
    pop_joined_gdf = join_pop(joined_df, tract_pop_df)

    Total_pop=compute_pop(pop_joined_gdf)
    print("Total population for tracts with hazardous waste sites in NC: ",Total_pop)

    choropleth_map = generate_choropleth_map(tract_shp, tract_pop_df)
    choropleth_map = highlight_polygons(pop_joined_gdf, choropleth_map)

    choropleth_map.savefig('D:\\Project\\LargeModels\\LLM-Geo\\solutions\\b48a2ad7-fa6e-40e2-84c2-196667f0cbff\\output\\NC_Choropleth_Map.png')

assembly_solution()