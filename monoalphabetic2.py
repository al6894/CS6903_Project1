import os
import sys
import time
import random
from collections import Counter
import numpy as np

# Number of plaintexts u = 5
PT = ["unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
      "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
      "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
      "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
      "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
      ]
# keyspace: {space, a,...,z}
keyspace = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
max_number_to_return = 6

def encrypt_mono(pt_idx, key, prob_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    num_rand_characters = 0
    c = []
    m = PT[pt_idx] # message
    L = len(m)
    while(ciphertext_pointer < (L+num_rand_characters)):
        coin_value = random.uniform(0,1)
        if(prob_of_random_ciphertext <= coin_value <=1):
            current_char = keyspace.index(m[message_pointer]) # find index of char in keyspace
            replacement_char = keyspace[key[current_char]] # index into the key to find replacement in keyspace
            c.append(replacement_char) # append substituted char to build ciphertext
            message_pointer +=1
        else:
            rand_char = keyspace[random.randint(0,26)]
            c.append(rand_char)
            num_rand_characters += 1
        ciphertext_pointer += 1
    return ''.join(c)

# Get the text's character frequency (not in use)
def get_frequency(plaintext):
    frequencies = Counter(plaintext)
    to_return = [frequencies.get(char, 0) for char in keyspace]
    return to_return

# Check if candidate is viable
def isCandidate(PT_freq, CT_freq):
    # print(PT_freq)
    # print(CT_freq)
    for i in range(len(keyspace)):
        if PT_freq[i] > CT_freq[i]:
            return False
    return True

#Approach 1: Check if letter frequencies are valid for a match
def compare_frequencies(PT_frequencies, PT_candidates, CT_freq):
    for i in range(len(PT)):
        PT_freq = get_frequency(PT[i])
        PT_freq.sort()
        # print(PT_freq)
        # print(CT_freq)
        candidate = isCandidate(PT_freq, CT_freq)
        if candidate:
            PT_frequencies[i] = PT_freq
            PT_candidates[i] = PT[i]

# Approach 2: Use ngrams (more specifically a trigram in this case)
def get_char_ngrams(text, n=4):
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    return Counter(ngrams)
# Function to compare trigram frequencies
def compare_ngrams(pt_ngrams, ct_ngrams):
    # Find common n-grams between ciphertext and plaintext
    common_ngrams = set(pt_ngrams.keys()) & set(ct_ngrams.keys())
    score = 0
    # Sum up the minimum count for each common trigram (how often it appears in both)
    for ngram in common_ngrams:
        score += min(pt_ngrams[ngram], ct_ngrams[ngram])
    return score

# Approach 3: Improves on previous frequency analysis, uses relative
# frequency, adjusts frequency based on random ciphertext chance.

# Get the text's character relative
def get_relative_freq(text):
    freq = Counter(text)
    total_count = sum(freq.values())
    relative_freq = np.array([freq.get(char, 0) / total_count for char in keyspace])
    return relative_freq

# Adjust frequencies for random insertions
def adjust_freq(pt_freq, prob_random_ciphertext):
    # Assumes the random characters are uniformly distributed over the keyspace
    uniform_freq = np.full(len(keyspace), 1/len(keyspace))
    adjusted_freq = (1 - prob_random_ciphertext) * pt_freq + prob_random_ciphertext * uniform_freq
    return adjusted_freq

# Compare sorted frequency distributions
def compare_frequency_profiles(ct_freq, pt_freq):
    ct_freq_sorted = np.sort(ct_freq)[::-1]
    pt_freq_sorted = np.sort(pt_freq)[::-1]
    # Compute Euclidean distance between frequency profiles
    distance = np.linalg.norm(ct_freq_sorted - pt_freq_sorted)
    return distance

def guess(PT_guess):
    print("My plaintext guess:")
    print(PT_guess)
    
def main():
    runs = 0
    freq_right = 0
    prob_random_ciphertext = 0.75  # Increase the probability to test robustness
    while runs < 100:
        test_key = random.sample(range(len(keyspace)), len(keyspace))
        pt_idx = random.randint(0, len(PT)-1)
        CT = encrypt_mono(pt_idx, test_key, prob_random_ciphertext)
        ct_freq = get_relative_freq(CT)

        # Store distances for each plaintext
        distances = []
        for i in range(len(PT)):
            pt_text = PT[i]
            pt_freq = get_relative_freq(pt_text)
            # Adjust for random insertions
            adjusted_pt_freq = adjust_freq(pt_freq, prob_random_ciphertext)
            distance = compare_frequency_profiles(ct_freq, adjusted_pt_freq)
            distances.append((i, distance))

        distances.sort(key=lambda x: x[1])
        best_match_idx, best_distance = distances[0]

        if best_match_idx == pt_idx:
            freq_right += 1

        runs += 1

    print(f"Accuracy over {runs} runs with random ciphertext probability {prob_random_ciphertext}:")
    print(f"Correct guesses: {freq_right}")
    print(f"Accuracy: {freq_right / runs * 100:.2f}%")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Raw elapsed time: {elapsed_time:.8f} seconds")
    minutes, seconds = divmod(elapsed_time, 60)