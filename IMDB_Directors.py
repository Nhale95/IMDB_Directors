import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import imdb

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



#function which takes in an array and normalises it, returns normalised array
def normalize_list(elements):
    print("unormalised = {}".format(elements))
    min = np.min(elements)
    max = np.max(elements)
    range = max-min
    normalized = (elements-min)/range
    return normalized

#Function which takes in the name of a director as a string and if the full name if formed from more than 2 names initialises the first 2 names. Returns a string.
def convert_name(name):

    parts = name.split()
    if len(parts) >= 3:
        # Convert first two names to initials
        initials = parts[0][0].upper() + ". " + parts[1][0].upper() + ". " + parts[2]
        return initials
    else:
        # If there are less than 3 parts, just use the original name
        return name

# Function which takes in a direction as a string and returns a tuple direction
def get_opposite_direction(direction):
    opposite_directions = {
        "up": (0, -20),
        "up-right": (0, -20),
        "right": (0, 0),
        "down-right": (0, 20),
        "down": (0, 20),
        "down-left": (0, 20),
        "left": (0, 0),
        "up-left": (0, -20),
        "unknown": (0, 0)
    }
    return opposite_directions.get(direction, (0, 0))

# function which takes in a string for a director name and checks if there is a csv file for the movie data. If there is no csv data it extracts it using IMDBs api. Returns a list of [years,ratings,titles] where years and ratings are arrays and titles is a list of strings
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
        extract_movie_data(name)
    # Read the Excel file into a pandas DataFrame
    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading '{csv_file}': {e}")

    # Extract the 2nd and 3rd columns as numpy arrays
    years = df.iloc[:, 1].values  # 2nd column (index 1)
    ratings = df.iloc[:, 2].values  # 3rd column (index 2)
    titles = df.iloc[:, 0].values  # 3rd column (index 2)
    
    return [years,ratings,titles]

# Function which takes in a list of names for directors and plots each film rating as a function of year of release
def plot_director_films(names):
    fig1, ax1 = plt.subplots(1, figsize=(26, 12), dpi=300, facecolor='#2e2e2e')
    fontsize = 20
   
    for file in names:
        [years,ratings,titles] = get_director_data(file)
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
    ax1.set_title('IMDB Director Film Ratings Over Time', fontsize=fontsize+10, pad=20, color='white')

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
    legend = ax1.legend(names,fontsize = fontsize-2,facecolor='#444444', edgecolor='white')
    for text in legend.get_texts():
        text.set_color('white')

    ax1.text(-0.07,-0.1,"Source: IMDB", transform=ax1.transAxes,fontsize =fontsize  -7, color='white')
    fig1.subplots_adjust(left=0.07,
                    bottom=0.1, 
                    right=0.97, 
                    top=0.92)
    # Save the figure
    fig1.savefig("Director_films.png", dpi=300, facecolor=fig1.get_facecolor())

# Function which takes in the normalised film number and mean rating values as well as a single point and returns the nearest points to that point
def find_closest_points_with_directions(norm_nums,norm_ratings, point, max_points=3):
    def get_direction(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        if dy > 0 and abs(dx) == 0:
            return "up"
        elif dy > 0 and dx > 0:
            return "up-right"
        elif dx > 0 and  abs(dy)==0:
            return "right"
        elif dy < 0 and dx > 0:
            return "down-right"
        elif dy < 0 and abs(dx) ==0:
            return "down"
        elif dy < 0 and dx < 0:
            return "down-left"
        elif dx < 0 and abs(dy)==0:
            return "left"
        elif dy > 0 and dx < 0:
            return "up-left"
        else:
            return "unknown"
    
    
    # Normalize num_movies and mean_ratings
    normalized_num_movies = norm_nums
    normalized_mean_ratings = norm_ratings
    

    print("norm_pont = {}".format(point))
    # Create normalized points array
    normalized_points = np.column_stack((normalized_num_movies, normalized_mean_ratings))
    #print("norm_ponts = {}".format(normalized_points))
    # Calculate distances and find closest points
    distances = []
    for i, other_point in enumerate(normalized_points):
        if not np.array_equal(other_point, point):
            distance = np.linalg.norm(point - other_point)
            distances.append((distance, normalized_points[i]))
    
    distances.sort(key=lambda d: d[0])
    
    closest_points = [distances[i][1] for i in range(min(len(distances), max_points))]
    directions = [get_direction(point, cp) for cp in closest_points]

    return closest_points, directions

# Function which takes in a list of names for directors and plots their mean ratings against number of films and saves plot as a png in directory
def plot_director_comparison_df(names,custom_ha = [],highlight = " "):
    # Example DataFrame creation
    data = pd.DataFrame(columns=['Director Name', 'Mean Rating', 'Number of Films'])

    fontsize = 20

    points = []
    for file in names:
        [years,ratings,titles] = get_director_data(file)
        N_ = len(ratings)
        mean = np.mean(ratings)
        points.append((N_, mean))
        new_row = {
            'Director Name': file,
            'Mean Rating': mean,
            'Number of Films':N_
        }
        data = data.append(new_row, ignore_index=True)
    data['Mean Rating Norm'] = normalize_list(data["Mean Rating"])
    data['Number of Films Norm'] = normalize_list(data["Number of Films"])

    
    fig1, ax1 = plt.subplots(1, figsize=(26, 12), dpi=300, facecolor='#2e2e2e')
    for i in range(0,len(names)):
        current_num = data.iloc[i]['Number of Films']
        current_num_norm = data.iloc[i]['Number of Films Norm']
        current_mean = data.iloc[i]['Mean Rating']
        current_mean_norm = data.iloc[i]['Mean Rating Norm']
        current_name = data.iloc[i]['Director Name']
        

        
        closest_ponts,directions = find_closest_points_with_directions(data['Number of Films Norm'],data['Mean Rating Norm'],(current_num_norm, current_mean_norm))
        print("director = {} opposite direction = {}, nearest director point = {}".format(current_name,directions[0],closest_ponts[0]))
        #ax1.plot(current_num,current_mean,marker='.', color='w',markersize = fontsize-9)
        ax1.semilogx(current_num,current_mean,marker='.', color='w',markersize = fontsize-9)
        direction = directions[0]
        direction_num = get_opposite_direction(directions[0])
            
        if "right" in direction:
            xytext = (-5, 0)
            horizantal_offset = "right"
        elif "left" in direction:
            xytext = (5, 0)
            horizantal_offset = "left"
        else:
            horizantal_offset = "center"

        if "up" in direction:
            xytext = (0, -5)
            vertical_offset = "top"
        elif "down" in direction:
            xytext = (0, 5)
            vertical_offset = "bottom"
        else:
            vertical_offset = "top"
        
        name_ = convert_name(current_name)
        if custom_ha:
            
            first_strings = [sublist[0] for sublist in custom_ha]
            
            if current_name in first_strings:
                pos = first_strings.index(current_name)
                horizantal_offset = custom_ha[pos][1]
        ax1.annotate(name_, (current_num, current_mean),textcoords="offset points", xytext=xytext, ha=horizantal_offset,va = vertical_offset,fontsize = fontsize-5,color='w')
            
    
    fontsize = 20

    ax1.set_facecolor('#2e2e2e')

    # Plot the data with modern aesthetics
 

    # Customize the ticks and labels
    fontsize = 22
    ax1.tick_params(axis='x', which='major', labelsize=fontsize-1, colors='white')
    ax1.tick_params(axis='y', which='major', labelsize=fontsize, colors='white')

    # Set axis labels with a larger font size and color
    ax1.set_ylabel("Mean Rating (/10)", fontsize=fontsize+15, labelpad=20, color='white')
    ax1.set_xlabel("Number of Feature-length Films", fontsize=fontsize+15, labelpad=20, color='white')


        # Set the specific x-ticks and labels
    ticks = [6,7,8,9,10, 20, 30, 40, 50]
    ax1.set_xticks(ticks)
    ax1.set_xticklabels([str(tick) for tick in ticks])

    # Adding gridlines at specific x-tick positions
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Ensure the gridlines are shown for the specified ticks
    for tick in ticks:
        ax1.axvline(x=tick, color='grey', linestyle='--', linewidth=0.5)

    # Set the title with a larger font size and color
    ax1.set_title('Comparison of Top IMDB Directors', fontsize=fontsize+10, pad=20, color='white')
    ax1.set_xlim(5.8,60)
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
    ax1.text(-0.07,-0.1,"Source: IMDB", transform=ax1.transAxes,fontsize =fontsize  -7, color='white')
    fig1.subplots_adjust(left=0.07,
                    bottom=0.1, 
                    right=0.97, 
                    top=0.92)

    fig1.savefig("Director_comparison.jpeg", dpi=300, facecolor=fig1.get_facecolor())

# Function which takes in a list of strings for directors and creates a cat-and-whiskers plot showing the median, mean and range of each director with their best and worst films being labelled. Plot is saved as a png
def director_box_plot(names):
    # Example DataFrame creation
    data = pd.DataFrame(columns=['Director Name', 'Mean Rating', 'Number of Films'])
    fig1, ax1 = plt.subplots(1, figsize=(28, 12), dpi=300, facecolor='#2e2e2e')
    fontsize = 20
    colors = ['cyan', 'lightgreen', 'lightblue', 'orange']
    
    for i, file in enumerate(names):
        [years,ratings,titles] = get_director_data(file)
        N_ = len(ratings)
        mean = np.mean(ratings)
        median = np.median(ratings)
        
 
            # Create a box plot
        box = ax1.boxplot(ratings, positions=[i+1], widths=0.4, patch_artist=True, showfliers=True,whis=3)
        
        plt.setp(box['boxes'], facecolor='none', edgecolor='white')
        plt.setp(box['whiskers'], color='orange')
        plt.setp(box['caps'], color='white')
        plt.setp(box['medians'], color='orange')
        ax1.plot(i+1, mean,marker='.', color='w',markersize = fontsize-9)
        xytext = (0,0)
        ax1.annotate(str(N_), (i+1+0.3, median),textcoords="offset points", xytext=xytext, ha='left',va = 'center',fontsize = fontsize-5,color='w')

        index= np.where(ratings == np.max(ratings))[0]
        best_film = titles[index]
        
        ax1.annotate(best_film[0], xy=(i+1, np.max(ratings)+0.1), xytext=(i+1, np.max(ratings)+0.1),
             fontsize=fontsize -6, color='white', ha='center')

        index= np.where(ratings == np.min(ratings))[0]
        worst_film = titles[index]
        #print(worst_film)
        #print(np.min(ratings))
        print(file)
        print("name = {}, max = {}, min = {}".format(file,np.max(ratings),np.min(ratings)))
        ax1.annotate(worst_film[0], xy=(i+1, np.min(ratings)-0.16), xytext=(i+1, np.min(ratings)-0.16),
             fontsize=fontsize -6, color='white', ha='center')

        if i ==0:
            ax1.annotate('No of\n films', xy=(i+1+0.38, median+0.1), xytext=(i+1+0.38, median+0.6),
             fontsize=fontsize -5, color='white', ha='center')
            ax1.arrow(i+1+0.38, median+0.5, 0, -0.3, head_width=0.1, head_length=0.08, fc='white', ec='white')

            ax1.annotate('Mean', xy=(i+1+0.38, mean+0.1), xytext=(i+1+0.45, mean-0.66),
             fontsize=fontsize -5, color='white', ha='center')
            ax1.arrow(i+1+0.38, mean-0.5, -0.26, 0.37, head_width=0.1, head_length=0.08, fc='white', ec='white')

            
    ax1.set_facecolor('#2e2e2e')

    # Plot the data with modern aesthetics
 
    # Set x-ticks to match the director names
    ax1.set_xticks(range(1, len(names) + 1))
    new_names = [name.replace(" ", "\n") for name in names]
    ax1.set_xticklabels(new_names,fontsize=fontsize)
    # Customize the ticks and labels
    fontsize = 22
    ax1.tick_params(axis='x', which='major', labelsize=fontsize-3, colors='white')
    ax1.tick_params(axis='y', which='major', labelsize=fontsize, colors='white')

    # Set axis labels with a larger font size and color
    ax1.set_ylabel("Rating (/10)", fontsize=fontsize+12, labelpad=35, color='white')
    ax1.set_xlabel("Directors", fontsize=fontsize+5, labelpad=15, color='white')

    # Set the title with a larger font size and color
    ax1.set_title('Comparison of Top IMDB Directors', fontsize=fontsize+13, pad=30, color='white')
    
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

    ax1.text(-0.07,-0.1,"Source: IMDB", transform=ax1.transAxes,fontsize =fontsize  -7, color='white')
    fig1.subplots_adjust(left=0.07,
                    bottom=0.1, 
                    right=0.97, 
                    top=0.92)

    fig1.savefig("Director_comparison_box_plot.jpeg", dpi=300, facecolor=fig1.get_facecolor())

#Examples 


#director_box_plot(['Steven Spielberg',"Quentin Tarantino",'James Cameron','Stanley Kubrick','Christopher Nolan','Alfred Hitchcock',"David Fincher","Ingmar Bergman","Martin Scorsese","Ridley Scott","Akira Kurosawa","Robert Zemeckis","David Lynch",'Billy Wilder',"Darren Aronofsky"])


#plot_director_comparison_df(['Steven Spielberg','Christopher Nolan',"Quentin Tarantino",'James Cameron','Stanley Kubrick','Alfred Hitchcock','Billy Wilder','Clint Eastwood','Danny Boyle', "David Lean","David Fincher","Ingmar Bergman", "Martin Scorsese","Ridley Scott","Roman Polanski","Denis Villeneuve","Sergio Leone", "Jean Pierre Junet", "Wes Anderson", "Woody Allen", "Peter Jackson", "Francis Ford Coppola", "Hayao Miyazaki","Akira Kurosawa","Darren Aronofsky","M. Night Shyamalan","Guy Ritchie","David Lynch", "Edgar Wright", "Alex Garland", "Charlie Chaplin", "Woody Allen","Robert Zemeckis","George Lucas","Agnès Varda","Spike Lee","Kathryn Bigelow","Ang Lee","Alfonso Cuarón","Guillermo del Toro","Brian De Palma","David Cronenberg","Milos Forman","Sam Mendes","Paul Thomas Anderson","Federico Fellini","Andrei Tarkovsky","William Friedkin"],[["Stanley Kubrick","left"],["Paul Thomas Anderson",'center'],["David Fincher",'center'],["Edgar Wright",'center'],["Robert Zemeckis",'right'],["George Lucas",'left'],["Andrei Tarkovsky",'left'],['Clint Eastwood','right'],["Ingmar Bergman","right"],['Alfred Hitchcock',"right"]])


plot_director_films(['Steven Spielberg','Christopher Nolan','James Cameron','Stanley Kubrick'])

