# Implements the Bayes theorem to calculate posterior probabilites
# Returns the updated probabilities for each university given:
#   - PU -> P(uni): Prior probabilities of each university (ordered)
#   - VU: Value for each univeristy to the given question (ordered)
#   - A: Value given as answer by the user
#   - l: lambda smoothing value

# P(uni|ans) = ( P(ans|uni) * P(uni) ) / P(ans)


import numpy as np

def posteriors(PU, VU, A, l=0.01):

    
    # Compute P(ans|uni)
    PAU = 1 - abs(A - VU)

    # Compute P(ans|uni) * P(uni)
    post = np.multiply(PAU, PU)

    # Normalize so it sums up to 1
    # P(ans) can be ignored bc it is a constant
    post = post/post.sum()

    # Smooth by a factor lambda so that values don't get to 0
    post = l/len(post) + (1-l)*post

    return post
