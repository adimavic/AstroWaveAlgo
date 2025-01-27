import pandas as pd
import numpy as np
def xl_parse(price,xl_path): #no
    
    global astro_level
    df = pd.read_excel(xl_path, header=None)

    # Flatten the data into a single list of numbers
    data = np.concatenate(df.values).ravel().tolist()

    # Remove any non-numeric or NaN values from the list
    data = [x for x in data if isinstance(x, (int, float)) and not np.isnan(x)]

    # Define the value to find
    find = float(price)

    # Find the closest number to the given value
    closest = min(data, key=lambda x: abs(x-find))

    # Get the indices of the closest number and the five numbers before and after it
    idx = data.index(closest)
    indices = [i for i in range(idx-90, idx+91) if i >= 0 and i < len(data)]
    
    # Extract the values at those indices and remove duplicates
    astro_level = (set([data[i] for i in indices]))
    astro_level = [x for x in astro_level]


    # Sort the result in ascending order
    astro_level.sort()

    # Limit the astro_level list to have a maximum of 11 elements
    if len(astro_level) > 179:
        astro_level = astro_level[:179]