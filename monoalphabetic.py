import os
import sys
import time
import random
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
max_number_to_return = 6

def encrypt_mono(pt_number, key, prob_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    num_rand_characters = 0
    c = []
    m = PT[pt_number] #message
    L = len(m) #message length
    while(ciphertext_pointer < (L+num_rand_characters)):
        coin_value = random.uniform(0,1)
        if(prob_of_random_ciphertext <= coin_value <=1):
            current_char = keyspace.index(m[message_pointer]) #find index of char in keyspace
            replacement_char = keyspace[key[current_char]] #index into the key to find replacement in keyspace
            c.append(replacement_char) #append substituted char to build ciphertext
            message_pointer +=1
        else:
            rand_char = keyspace[random.randint(0,26)]
            c.append(rand_char)
            num_rand_characters += 1
        ciphertext_pointer += 1
    return ''.join(c)

#Get the text's character frequency
def get_frequency(plaintext):
    frequencies = Counter(plaintext)
    to_return = [frequencies.get(char, 0) for char in keyspace]
    return to_return

#Check if candidate is viable
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

def guess(PT_guess):
    print("My plaintext guess:")
    print(PT_guess)
    
prob_random_ciphertext = 0.05
def main():
    runs = 0
    ngram_right = 0
    freq_right = 0
    while runs < 100:
        test_key = [5,4,1,2,9,3,0,6,17,8,10,11,16,13,14,15,12,7,18,20,19,21,22,23,24,25,26]
        PT_frequencies = {}
        PT_candidates = {}
        CT = encrypt_mono(1,test_key,prob_random_ciphertext)
        CT_freq = get_frequency(CT)
        CT_freq.sort()
        compare_frequencies(PT_frequencies, PT_candidates, CT_freq)
            
        #CHAR NGRAMS 
        pt_ngrams = [get_char_ngrams(text) for text in PT]
        ct_ngrams = get_char_ngrams(CT)
        char_ngram_scores = []
        for i, pt_ngram in enumerate(pt_ngrams):
            score = compare_ngrams(pt_ngram, ct_ngrams)
            char_ngram_scores.append((i, score))  # Keep track of the score and corresponding plaintext index
        char_ngram_scores.sort(key=lambda x: x[1], reverse=True)
        best_match_idx, best_score = char_ngram_scores[0]
        print(f"Best matching plaintext using char ngram is PT[{best_match_idx}] with a score of {best_score} \n")
        print("Candidates:")
        for candidate in PT_candidates:
            print(PT_candidates[candidate], "\n")
        
        if len(PT_candidates) == 1 and next(iter(PT_candidates.values())) == PT[1]:
            freq_right += 1
        if best_match_idx == 1:
            ngram_right += 1

        runs += 1
    print("freq_right", freq_right)
    print("ngram_right", ngram_right)
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Raw elapsed time: {elapsed_time:.8f} seconds")
    minutes, seconds = divmod(elapsed_time, 60)