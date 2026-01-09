# SHARK ATTACKS #

# %% Importing libraries
import requests # For downloading the file from the webpage
from pathlib import Path # For defining the path where the file is downloaded
import pandas as pd
import matplotlib.pyplot as plt
import os

# %%
SCRIPT_DIR = Path(__file__).resolve().parent # Seting working directory to script location
os.chdir(SCRIPT_DIR)
print("Working directory set to:", SCRIPT_DIR)


# %% Downloading the shark attack data and saving them to my assignment directory.
url = "https://www.sharkattackfile.net/spreadsheets/GSAF5.xls" # URL to download the file
filename = "sharkattacks.xls" # Defines name of the file to be used when saving the file
file_path = SCRIPT_DIR/filename

response = requests.get(url) #Communication with server
response.raise_for_status()
file_path.write_bytes(response.content)
print("Download complete:", file_path) # Displays message with the file path. If a file with a same name is in the folder, it will be replaced.

# %% Reading nad cleaning data:
attacks = pd.read_excel("C:/Users/269713/GitHub/datasteward_project/assignment/sharkattacks.xls") # Reads the excel
attacks["Country"] = attacks["Country"].str.upper() # Converts the country names to upper case
if attacks["Year"].isna().any(): # Converts Year variable to integer
    attacks["Year"] = attacks["Year"].astype("Int64")  # nullable integer in case missing values are present in the dataset
else:
    attacks["Year"] = attacks["Year"].astype(int)
print(attacks.head()) # Prints first rows of the dataset

# %% Function to select a year
def select_year(df, year_col): # Script to define the function
    min_year = int(df[year_col].min()) # Defining minimum year 
    max_year = int(df[year_col].max()) # Defining maximum year
    print(f"The dataset contains incidents occurring from {min_year} to {max_year}.") # Prints a message to inform user about the range of years for which the data is available
    
    while True: # Asking for year to be visualized
        year = int(input("Enter the year you are interested in: ")) # Asks for input (which year) and saves the input as integer 
        if min_year <= year <= max_year: # Condition - the value must fit to the available range
            break  # If condition is fulfilled, the loop stops
        else: # If not fulfilled, it asks for the year again:
            print(f"Please enter a year between {min_year} and {max_year}.")
    
    print(f"Filtering data for {year}.") # One the year is correctly selected, it prints the message about filtering the data
    filtered_df = df[(df[year_col] == year)].reset_index(drop=True) # It filters the data based on the selected year and saves in new dataframe
    
    print("The dataset is ready. Preparing visualization") # Informs the user about the readiness of the dataset and preparation of output.
    return filtered_df # the function returns filtered dataset

attacks_filtered = select_year(attacks, "Year") # Calling the function to actually filter the dataset
# print (attacks_filtered.head) 

# %% Calculating the number of incidents per country in the selected year and plotting ten countries with the highest number of incidents.
def plot_incidents(df, country_col, year_col, top_n): # Function definition
    
    country_counts = df[country_col].value_counts() # Calculating the number of incidents per country. .value_counts() counts how many times each unique value appears.
    top_countries = country_counts.head(top_n) # Selects countries with highest number of incidents. Sorts automatically.

    year = int(df[year_col].iloc[0]) # Since only one year was selected, this extracts value from the first row of "Year" variable 
    file_path = SCRIPT_DIR / f"top_countries_plot_{year}.png" # Defines where the plot will be saved and under which name
     
    plt.figure(figsize=(10,6)) # Ploting the countries - preparing plot
    top_countries.plot(kind='bar', color='skyblue') # Difining plot type and color of bars
    plt.title(f"Top {top_n} Countries by Number of Incidents in {year}") # Defining title
    plt.xlabel("Country") # X-axis label
    plt.ylabel("Number of Incidents") # Y-axis label
    plt.xticks(rotation=45, ha="right") #Rotates the axis labels
    plt.tight_layout() # Adjust spacing
    plt.savefig(file_path, dpi=300)  # save the figure 
    plt.show()                       # display the figure 
    plt.close()       
    print ("Your output has been created")

plot_incidents(df=attacks_filtered, country_col = "Country", year_col = "Year", top_n=10) # Calling the function
