# Director Film Ratings Analysis

This Python project analyzes and visualizes the film ratings of directors using data from IMDb. The project consists of several functions that extract, process, and plot movie ratings for specified directors. The project uses the `imdb`, `pandas`, `numpy`, and `matplotlib` libraries.

## Requirements

- Python 3.x
- `numpy`
- `pandas`
- `matplotlib`
- `imdbpy`

You can install the required libraries using:

```bash
pip install -r requirements.txt



Example Script

import numpy as np
import os
import matplotlib.pyplot as plt
import imdb
import pandas as pd

# Extract movie data for a list of directors
extract_movie_data("Quentin Tarantino")
extract_movie_data("Steven Spielberg")

# Plot the film ratings over time for the specified directors
plot_director_films(["Quentin Tarantino", "Steven Spielberg"])

# Plot a comparison of mean film ratings for the specified directors
plot_director_comparison(["Quentin Tarantino", "Steven Spielberg"])

