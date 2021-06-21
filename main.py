import sys
import numpy as np
import dataparser
import bayes
import best_question as bq

dicQ = {
        "Europe"                :   "Do you want to study in Europe",
        "Alumni employment"     :   "Are you interested in finding work there",
        "Quality of education"  :   "Do you require it to have a good position in quality rankings",
        "influence"             :   "Is the reputation important for you",
        "tfg"                   :   "Do you want to do the Bachelor's Thesis there",
        "English"               :   "Do you want to go to an English-speaking country",
        "Whole year"            :   "Do you want to go a whole year",
        "Residence"             :   "Are you looking for a residence enrolled with the university",
        "Climate"               :   "Are you looking for hot weather",
        "Hackathon"             :   "Do you want to do hackathons there",
        "Clubs"                 :   "Are you interested in joining clubs",
        "party"                 :   "Do you value the amount of parties held",
        "previous alumni"       :   "Do you care about the amount of students that have gone there previously",
        "minimum grade"         :   "Should your destination require good grades",
        "calendar"              :   "Do you care about the calandar being compatible with UPC's",
        "presenciality"         :   "Do you want to go to face-to-face classes",
        "sea"                   :   "Would you rather go to a seaside city",
        "capital"               :   "Would you rather go to a capital city"
        }


# Computes total variation distance between arrays a and b. a and b add up to 1
def tvd(a, b):
  return sum(abs(a-b))/2


# given an answer in [0, 4] returns its corresponding float value in [0, 1]
def answer_to_01(answer):
    return np.interp(answer, (0, 4), (0, 1))


# Returns True if the calculated posteriors are already good enough
def finished(posterior, usedQ):
    return not np.any(usedQ[1:]) or np.any(posterior >= 0.8) or tvd(posterior, get_uniform(posterior.shape[0])) > 0.9 \
                                 or (usedQ.shape[0]) - np.count_nonzero(usedQ) > 7


# Returns the names of the 'num' universities with the highest posterior
def best_options(data, posteriors, num=5):
    df = data.copy()
    df['posteriors'] = posteriors
    df = df.sort_values(by='posteriors', ascending=False)
    m = min(df.shape[0], num)
    return writeRes(np.array(df['university'])[list(range(0, m))],data)


# Returns the specified column of data 
def get_probs(data, Q):
    VU = np.array(data.iloc[:,[Q]])
    return VU[:, None].squeeze()


# Returns questions in natural language
def get_question(data, Q):
    return dicQ[data.columns[Q]]
    #return questions[Q]


# Returns the next question to ask
def next_question(data, usedQ, posteriors):
    next_Q = bq.bestQ(usedQ, data, posteriors)
    usedQ[next_Q] = 0
    return next_Q, usedQ


# Update posteriors based on Q and A
# Q: question (represents the index in data), int
# A: answer, int or float
def update_posteriors(data, posterior, Q, A):
    if A == 2:
        return posterior  # corresponds to 'I don't care' option so don't update probabilities
    A = answer_to_01(A)
    return bayes.posteriors(posterior, data.iloc[:,Q], A)


# Initilizes the array that keeps track of already-asked questions
def init_usedQ(data):
    usedQ = np.ones(len(data.columns))
    usedQ[0] = 0
    return usedQ


# Returns an array with a uniform distribution
def get_uniform(size):
    return np.ones(size) / size


# Initializes the prior of each university
def init_priors(data):
    size = data.shape[0]
    return get_uniform(size)  # uniform distribution


# Loads the necessary data
def init_data():
    return dataparser.parse_csv('dataSmall.csv')


# Pretty format for the results
def writeRes(bestOpt, data):
    lis=[]
    for uni in bestOpt:
        s="*"+uni+"*\n\[Country]\n\[Website]"
        lis.append(s)
    return lis 


def main():
    data = init_data()
    posterior = init_priors(data)
    usedQ = init_usedQ(data)
    while not finished(posterior, usedQ):
        next_Q, usedQ = next_question(data, usedQ, posterior)
        A = float(input())
        posterior = update_posteriors(data, posterior, next_Q, A)

if __name__ == '__main__':
    main()
