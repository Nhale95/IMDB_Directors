import numpy as np
import os
import matplotlib.pyplot as plt
import imdb
import pandas as pd

# Function which takes in the director name as a string and return the director's IMDB film ratings and years of release as arrays and saves them as a CSV in the data subfolder
def get_director_data(name):

    # Define the relative path to the Excel file
    data_dir = 'data'
    file = name.replace(' ', '_') + "_movies.csv"
    csv_file = os.path.join(data_dir, file)

    # Check if the directory exists
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Directory '{data_dir}' does not exist.")

    # Check if the file exists
    if not os.path.exists(csv_file):
        IMDB.extract_movie_data(name)
    # Read the Excel file into a pandas DataFrame
    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading '{csv_file}': {e}")

    # Extract the 2nd and 3rd columns as numpy arrays
    years = df.iloc[:, 1].values  # 2nd column (index 1)
    ratings = df.iloc[:, 2].values  # 3rd column (index 2)
    
    return [years,ratings]


# Function which takes in the director names as a list and plots the directors films as a function of time
def plot_director_films(names):
    fig1, ax1 = plt.subplots(1, figsize=(17, 10), dpi=100, facecolor='#2e2e2e')
    fontsize = 20
   
    for file in names:
        #print(file)
        [years,ratings] = get_director_data(file)
         # Plot the data with modern aesthetics
        ax1.plot(years, ratings, marker='o', linestyle='-', linewidth=2, markersize=8)
   # Set up the figure and axis with a dark background
    
    ax1.set_facecolor('#2e2e2e')

    # Plot the data with modern aesthetics
 

    # Customize the ticks and labels
    fontsize = 22
    ax1.tick_params(axis='x', which='major', labelsize=fontsize-1, colors='white')
    ax1.tick_params(axis='y', which='major', labelsize=fontsize, colors='white')

    # Set axis labels with a larger font size and color
    ax1.set_ylabel("Rating (/10)", fontsize=fontsize+15, labelpad=20, color='white')
    ax1.set_xlabel("Year of Release", fontsize=fontsize+15, labelpad=20, color='white')

    # Set the title with a larger font size and color
    ax1.set_title('IMBD Director Film Ratings', fontsize=fontsize+10, pad=20, color='white')

    # Customize the grid
    ax1.grid(color='#444444')

    # Customize the spines (borders of the plot)
    ax1.spines['top'].set_color('#444444')
    ax1.spines['bottom'].set_color('#444444')
    ax1.spines['left'].set_color('#444444')
    ax1.spines['right'].set_color('#444444')

    # Set the color of the plot background and figure background
    ax1.patch.set_alpha(0.7)
    fig1.patch.set_alpha(0.7)
    legend = ax1.legend(names,fontsize = fontsize,facecolor='#444444', edgecolor='white')
    for text in legend.get_texts():
        text.set_color('white')
    # Save the figure
    fig1.savefig("Director_films.png", dpi=300, facecolor=fig1.get_facecolor())

# Function which takes in the director names and plots their mean rating against their number of films
def plot_director_comparison(names):
    fig1, ax1 = plt.subplots(1, figsize=(20, 12), dpi=300, facecolor='#2e2e2e')
    fontsize = 20
    i = 0
    for file in names:
        [years,ratings] = get_director_data(file)
        N_ = len(ratings)
        print
        mean = np.mean(ratings)
        #ax1.plot(N_,mean,marker='x', color='r',markersize = fontsize)
        ax1.plot(N_,mean,marker='.', color='w',markersize = fontsize-9)
        ax1.annotate(file, (N_, mean), textcoords="offset points", xytext=(0, -15*(-1)**i-4), ha='center',fontsize = fontsize-7,color='white')
         # Plot the data with modern aesthetics
        i = i + 1

    ax1.set_facecolor('#2e2e2e')

    # Plot the data with modern aesthetics
 

    # Customize the ticks and labels
    fontsize = 22
    ax1.tick_params(axis='x', which='major', labelsize=fontsize-1, colors='white')
    ax1.tick_params(axis='y', which='major', labelsize=fontsize, colors='white')

    # Set axis labels with a larger font size and color
    ax1.set_ylabel("Mean Rating (/10)", fontsize=fontsize+15, labelpad=20, color='white')
    ax1.set_xlabel("Number of Feature-length Films", fontsize=fontsize+15, labelpad=20, color='white')

    # Set the title with a larger font size and color
    ax1.set_title('IMBD Director Comparison', fontsize=fontsize+10, pad=20, color='white')

    # Customize the grid
    ax1.grid(color='#444444')

    # Customize the spines (borders of the plot)
    ax1.spines['top'].set_color('#444444')
    ax1.spines['bottom'].set_color('#444444')
    ax1.spines['left'].set_color('#444444')
    ax1.spines['right'].set_color('#444444')

    # Set the color of the plot background and figure background
    ax1.patch.set_alpha(0.7)
    fig1.patch.set_alpha(0.7)
    fig1.savefig("Director_comparison.png", dpi=300, facecolor=fig1.get_facecolor())


# Function to extract movie data
def extract_movie_data(director_name):
    # Create an instance of IMDb
    ia = imdb.IMDb()
        # Directory and filename for saving data
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    csv_file = os.path.join(data_dir, director_name.replace(' ', '_') + "_movies.csv")

    directors = ia.search_person(director_name)
    # Take the first director (most relevant result)
    director = directors[0]
    ia.update(director, 'filmography')
    
    # Get the filmography entries for 'director' category
    filmography = director.get('filmography').get('director')
    
    # Function to check if a movie has only one director and is longer than 60 minutes
    def is_valid_movie(movie):
        ia.update(movie)
        directors = movie.get('directors')
        runtime = movie.get('runtimes')
        if directors and len(directors) == 1:
            if runtime:
                runtime_minutes = int(runtime[0])
                if runtime_minutes >= 60<= 4*60:
                    return True
        return False

    # List to hold movie data
    movies_data = []
    
    # Iterate through each movie and collect relevant information
    for movie in filmography:
        if is_valid_movie(movie):
            title = movie['title']
            print(title)
            year = movie.get('year')
            rating = movie.get('rating')
            movies_data.append({
                'Title': title,
                'Year': year,
                'Rating': rating
            })
    
    # Create a DataFrame
    df = pd.DataFrame(movies_data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)
    
    return df

#plot_director_films(['Steven Spielberg','Christopher Nolan','James Cameron','Stanley Kubrick'])

#plot_director_comparison(['Steven Spielberg','Christopher Nolan',"Quentin Tarantino",'James Cameron','Stanley Kubrick','Alfred Hitchcock','Billy Wilder','Clint Eastwood','Danny Boyle', "David Lean","David Fincher","Ingmar Bergman","John Ford", "Martin Scorsese","Ridley Scott","Roman Polanski"])