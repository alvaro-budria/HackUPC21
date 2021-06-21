import numpy as np
import pandas as pd


# Returns the index of the next best question. The question that maximizes separability is chosen.
# usedQ indicates already-used question (are not considered)
# df contains the data
# props contains the current estimate of the probability for each university
def bestQ(usedQ, df, props):
    punt = np.zeros(len(usedQ))
    mat = df.to_numpy()

    # Decide which question is the best based on its variance
    # Take into account current distribution to be more accurate
    for quest in np.argwhere(usedQ):
        # Compute weighted mean
        pondAvg = np.dot(props, mat[:,quest])

        # Compute weighted variance
        punt[quest] = np.dot(props, np.square(pondAvg - mat[:,quest]))
    return np.argmax(punt)
