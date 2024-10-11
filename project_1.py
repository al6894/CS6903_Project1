'''
Conditions:
1. No access to key
2. Part of the encryption scheme is hidden

Known:
1. Key is a sequence of t numbers between 0 and 26
2. Ciphertext looks like a sequence of symbols {space, a,..,z}
3. Program may be ran on different L, u, and t (ex: L=600, u=5, t between 1 and 20)
4. The encryption algorithm can choose the next character from m[i] as:
      a. random value in {space, a,...,z}
      b. ciphertext character
5. If mono, key length is 27
   If poly, key length can be <<27 (much smaller than 27)
6. Encryption algorithm uses coin generation [0,1] and compares
   the value to prob_random_character to decide random or not
7. Program should work for increasing values for 
   prob_of_random_ciphertext (e.g., 0.05, 0.10, 0.15, etc)

'''

import os
import sys
import random
import Levenshtein
from collections import Counter

# Number of plaintexts u = 5
PT = ["unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
      "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
      "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
      "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
      "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
      ]
# keyspace: {space, a,...,z}
keyspace = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
prob_random_ciphertext = 0.05

# Potential function to generate random keys, up to 10000.
# (currently not in use)
def generate_random_keys(num_keys):
    keys = []
    for _ in range(num_keys):
        # Generate a random key of 27 numbers between 0 and 26
        key = [random.randint(0, 26) for _ in range(27)]
        keys.append(key)
    return keys

# Example usage: Generate 10,000 keys
random_keys = generate_random_keys(10000)

# Function to test decryption
def encrypt(pt_number, key, prob_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    num_rand_characters = 0
    t = len(key)
    c = [] 
    m = PT[pt_number] 
    L = len(m) # Length of the message
    while (ciphertext_pointer < (L + num_rand_characters)):
        coin_value = random.uniform(0,1) # coin generation return value [0,1]
        # Case where we encrypt and return ciphertext
        if (prob_of_random_ciphertext <= coin_value <= 1):
            j = (message_pointer % t) + 1 # Shift value
            key_shift = key[j % t]
            message_char_pos = keyspace.index(m[message_pointer])
            shifted_char = keyspace[(message_char_pos + key_shift) % len(keyspace)] # Shift the message char by j pos
            c.append(shifted_char) # Append shifted message character to ciphertext list
            message_pointer += 1
        else: # Insert random value
            rand_char = keyspace[random.randint(0,26)]
            c.append(rand_char)
            num_rand_characters += 1
        ciphertext_pointer += 1
    return ''.join(c)

# Todo: Make decryption try more combinations of keys that we generate.
# Todo: Generate "x" random key combinations and run "y" amount of times. 
# Establish a value such as 70 or 80 percent match for a guess to be "valid". 
# We do not know the key used for encryption so our program needs to try many 
# different keys and see if we can get a good match for the plaintext.
# Key must be length 27 for monoalphabetic substitution
# key = [5, 18, 20, 7, 12, 3, 26, 11, 15, 9, 21, 0, 8, 1, 14, 25, 4, 22, 13, 2, 10, 24, 16, 17, 23, 19, 6]
def decrypt(ciphertext, key, prob_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    t = len(key)
    pt = []
    L = len(ciphertext)
    while ciphertext_pointer < L:
        j = (ciphertext_pointer % t) + 1 # Shift value
        c_val = keyspace.index(ciphertext[ciphertext_pointer])
        key_shift = key[j % t]
        plain_val = keyspace[(c_val - key_shift) % len(keyspace)] # Reverse the shift
        pt.append(plain_val)
        message_pointer += 1
        ciphertext_pointer += 1
    return ''.join(pt)

# Detect random characters based on frequency analysis. If a character appears infrequently,
# maybe it is a random character and its position is recorded.
def detect_random_characters(decrypted_text, threshold=0.01):
    letter_freqs = Counter(decrypted_text)
    total_chars = len(decrypted_text)
    # Estimate the frequency of each character
    char_probabilities = {char: count / total_chars for char, count in letter_freqs.items()}
    # Identify characters with very low frequency as "random"
    random_indices = [i for i, char in enumerate(decrypted_text) if char_probabilities.get(char, 0) < threshold]
    return random_indices

# Removes characters deemed random from the decrypted text
def filter_random_chars(decrypted_text, random_indices):
    return ''.join([char for i, char in enumerate(decrypted_text) if i not in random_indices])

def n_grams(text, n=2):
    return Counter([text[i:i+n] for i in range(len(text)-n+1)])

def get_ngram_probability(model, ngram):
    prefix, next_char = ngram[:-1], ngram[-1]
    prefix_count = sum(model[prefix].values())
    next_char_count = model[prefix][next_char]
    return next_char_count / prefix_count if prefix_count > 0 else 0

def ngram_similarity(decrypted_text, plaintext, n=3):
    decrypted_ngrams = n_grams(decrypted_text, n)
    reference_ngrams = n_grams(plaintext, n)
    
    intersection = sum((decrypted_ngrams & reference_ngrams).values())
    total = sum((decrypted_ngrams | reference_ngrams).values())
    
    return (intersection / total) * 100  # Return similarity as a percentage

def detect_random_characters_with_confidence(decrypted_text, model, n=3):
    random_char_confidence = []
    for i in range(len(decrypted_text) - n + 1):
        ngram = decrypted_text[i:i+n]
        prob = get_ngram_probability(model, ngram)
        random_char_confidence.append(prob)
    return random_char_confidence

def filter_low_confidence_chars(decrypted_text, confidence_scores, threshold=0.1):
    return ''.join([char for i, char in enumerate(decrypted_text) if confidence_scores[i] > threshold])

# Compares the similarity of words.
def word_similarity(decrypted_text, plaintext):
    decrypted_words = set(decrypted_text.split())
    reference_words = set(plaintext.split())
    intersection = len(decrypted_words & reference_words)
    union = len(decrypted_words | reference_words)
    return (intersection / union) * 100 

# Sums up the matching characters of decrypted text and plaintext to generate
# a score.
# After 10 runs of 1000 iterations, the average score was 58.44% with prob_random_ciphertext = 0.1 (worst)
def similarity_score(decrypted_text, plaintext):
    # Compare the two texts and count the number of matching characters
    score = sum(1 for a, b in zip(decrypted_text, plaintext) if a == b)
    return score

# Similar to similarity_score but is more flexible when there are mismatches
# After 10 runs of 1000 iterations, the average score was 85.20% with prob_random_ciphertext = 0.1
def levenshtein_similarity(decrypted_text, plaintext):
    distance = Levenshtein.distance(decrypted_text, plaintext)
    max_len = max(len(decrypted_text), len(plaintext))
    return (1 - (distance / max_len)) * 100  

# Combines Levenshtein Distance similarity approach with word similarity approach.
# After 10 runs of 1000 iterations, the average score was 85.50% at weights 0.9, 0.1 with prob_random_ciphertext = 0.1
# After 10 runs of 1000 iterations, the average score was 85.40% at weights 0.8, 0.2 with prob_random_ciphertext = 0.1
# After 10 runs of 1000 iterations, the average score was 85.70% at weights 0.7, 0.3 with prob_random_ciphertext = 0.1
# After 10 runs of 1000 iterations, the average score was 86.07% at weights 0.6, 0.4 with prob_random_ciphertext = 0.1 (highest)
# After 10 runs of 1000 iterations, the average score was 85.84% at weights 0.5, 0.5 with prob_random_ciphertext = 0.1
def hybrid_similarity(decrypted_text, plaintext):
    levenshtein_score = levenshtein_similarity(decrypted_text, plaintext)
    word_score = word_similarity(decrypted_text, plaintext)
    return (0.5 * levenshtein_score + 0.5 * word_score)

# Combines Levenshtein Distance similarity approach with word similarity approach and random character detection.
# After 10 runs of 1000 iterations, the average score was 85.80% at weights 0.9, 0.1 with prob_random_ciphertext = 0.1
# After 10 runs of 1000 iterations, the average score was 85.57% at weights 0.8, 0.2 with prob_random_ciphertext = 0.1
# After 10 runs of 1000 iterations, the average score was 84.87% at weights 0.7, 0.3 with prob_random_ciphertext = 0.1
# After 10 runs of 1000 iterations, the average score was 86.41% at weights 0.6, 0.4 with prob_random_ciphertext = 0.1 (highest)
# After 10 runs of 1000 iterations, the average score was 85.08% at weights 0.5, 0.5 with prob_random_ciphertext = 0.1
def hybrid_similarity_with_random_detection(decrypted_text, plaintext):
    random_indices = detect_random_characters(decrypted_text, threshold=0.01)
    filtered_decrypted = filter_random_chars(decrypted_text, random_indices)
    filtered_reference = filter_random_chars(plaintext, random_indices)
    
    # Use Levenshtein and other similarity measures on filtered texts
    levenshtein_score = levenshtein_similarity(filtered_decrypted, filtered_reference)
    word_score = word_similarity(filtered_decrypted, filtered_reference)
    return (0.5 * levenshtein_score + 0.5 * word_score)

# After 10 runs of 1000 iterations, the average score was 27.69% with prob_random_ciphertext = 0.75
# After 10 runs of 1000 iterations, the average score was 30.35% with prob_random_ciphertext = 0.70
# After 10 runs of 1000 iterations, the average score was 33.37% with prob_random_ciphertext = 0.65
# After 10 runs of 1000 iterations, the average score was 36.70% with prob_random_ciphertext = 0.60
# After 10 runs of 1000 iterations, the average score was 41.29% with prob_random_ciphertext = 0.55
# After 10 runs of 1000 iterations, the average score was 48.28% with prob_random_ciphertext = 0.50
# After 10 runs of 1000 iterations, the average score was 54.84% with prob_random_ciphertext = 0.45
# After 10 runs of 1000 iterations, the average score was 61.78% with prob_random_ciphertext = 0.40
# After 10 runs of 1000 iterations, the average score was 67.11% with prob_random_ciphertext = 0.35
# After 10 runs of 1000 iterations, the average score was 71.23% with prob_random_ciphertext = 0.30
# After 10 runs of 1000 iterations, the average score was 77.85% with prob_random_ciphertext = 0.25
# After 10 runs of 1000 iterations, the average score was 81.31% with prob_random_ciphertext = 0.20
# After 10 runs of 1000 iterations, the average score was 85.27% with prob_random_ciphertext = 0.15
# After 10 runs of 1000 iterations, the average score was 88.44% with prob_random_ciphertext = 0.1
# After 10 runs of 1000 iterations, the average score was 92.57% with prob_random_ciphertext = 0.05
def dynamic_hybrid_similarity(decrypted_text, plaintext, prob_random_ciphertext):
    levenshtein_score = levenshtein_similarity(decrypted_text, plaintext)
    ngram_score = ngram_similarity(decrypted_text, plaintext, n=4)
    word_score = word_similarity(decrypted_text, plaintext)
    # Dynamically adjust weights based on the random character probability
    if prob_random_ciphertext > 0.1:
        return (0.6 * levenshtein_score + 0.4 * ngram_score)
    else:
        return (0.4 * levenshtein_score + 0.3 * ngram_score + 0.3 * word_score)

def find_best_plaintext_match(decrypted_text, PT):
    best_score = -1
    matched_PT_idx = -1
    for i, pt in enumerate(PT):
        #score = similarity_score(decrypted_text, pt)
        #score = levenshtein_similarity(decrypted_text, pt)
        #score = hybrid_similarity(decrypted_text, pt)
        #score = hybrid_similarity_with_random_detection(decrypted_text, pt)
        score = dynamic_hybrid_similarity(decrypted_text, pt, prob_random_ciphertext)
        #print(f"Similarity score with PT[{i}]: {score:.2f}")
        if score > best_score:
            best_score = score
            matched_PT_idx = i
    return matched_PT_idx 
    
def main():
    pt_num = 0
    # Key must be length 27 for monoalphabetic substitution
    key = [5, 18, 20, 7, 12, 3, 26, 11, 15, 9, 21, 0, 8, 1, 14, 25, 4, 22, 13, 2, 10, 24, 16, 17, 23, 19, 6]
    iters = 1
    wrong = 0
    runs = 0
    total_score = 0
    while runs < 10:
        wrong = 0
        iters = 1
        while iters < 1001:
            print("-----------------------------------------------------")
            print("Iter:", iters)
            #print("Message: ")
            #print(' ')
            #print(PT[pt_num])
            #print("Ciphertext: ")
            #print(' ')
            encrypted_text = encrypt(pt_num, key, prob_random_ciphertext)
            #print(encrypted_text)
            #print("Decrypted: ")
            #print(' ')
            decrypted_text = decrypt(encrypted_text, key, prob_random_ciphertext)
            #print(decrypted_text)
            print("My plaintext guess is:")
            matched_PT_idx = find_best_plaintext_match(decrypted_text, PT)
            if PT[matched_PT_idx] != PT[pt_num]:
                wrong += 1
            print(PT[matched_PT_idx])
            iters += 1
        score = ((iters - wrong)/iters) * 100
        total_score += score
        runs += 1
    print(f"After {runs} runs, the average score was {(total_score/runs):.2f}%")

if __name__ == "__main__":
    main()