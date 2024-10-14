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
prob_random_ciphertext = 0.1
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

def decrypt_mono(ciphertext, key, prob_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    t = len(key)
    dec_pt = []
    L = len(ciphertext)
    while ciphertext_pointer <L:
        dec_pt.append(keyspace[key.index(keyspace.index(ciphertext[ciphertext_pointer]))])
        ciphertext_pointer += 1
    return ''.join(dec_pt)

def return_highest_vals(freq_list):
    temp_list = freq_list.copy()
    temp_list.sort()
    top_vals = temp_list[-max_number_to_return:][::-1]
    bottom_vals = temp_list[:max_number_to_return]
    return top_vals, bottom_vals

def return_frequencies(input_string):
    # Get the frequency of each character in input_string
    frequencies = Counter(input_string)
    # Return the counts in the order of keyspace
    to_return = [frequencies.get(char, 0) for char in keyspace]
    return to_return

def count_double_char(text):
    count = 0
    # Loop through the text, check consecutive characters
    for i in range(len(text) - 1):  # len(text) - 1 to avoid out of range
        if text[i] == text[i + 1]:
            count += 1
    return count

# Frequency analysis by itself only works for 0.05 random ciphertext
# 1 candidate at 0.05, 2 at 0.1, 3 at 0.15, 4 at 0.2, 5 at 0.25+
def isCandidate(PT_freq, CT_freq):
    for i in range(len(keyspace)):
        if PT_freq[i] > CT_freq[i]:
            return False
    return True

def guess(PT_guess):
    print("My plaintext guess:")
    print(PT_guess)

def print_frequencies(PT_max_freq, PT_min_freq, PT_frequencies, CT_freq):
    CT_highest,CT_lowest = return_highest_vals(CT_freq)
    CT_freq.sort()
    for x in range(0,len(PT)):
        count_iter = 0
        print("PT Frequencies: ")
        print(keyspace)
        for freq_iter in range(0,len(PT_frequencies)):
            count_iter+=1
            print(PT_frequencies[freq_iter])
        print("")
        # observed that space and letter e are highest frequency of all strings
        print("PT:", x)
        print("CT Highest:", CT_highest)
        print("Highest:", PT_max_freq[x])
        print("CT Lowest: ", CT_lowest)
        print("Lowest: ", PT_min_freq[x])
        PT_frequencies[x].sort()
        print("CT Freq:", CT_freq)
        print("PT Freq:", PT_frequencies[x])

def main():
    idx = 0
    test_key = [5,4,1,2,9,3,0,6,17,8,10,11,16,13,14,15,12,7,18,20,19,21,22,23,24,25,26]
    CT = encrypt_mono(idx,test_key,prob_random_ciphertext)
    print("-------------------------------")
    print("Plaintext:")
    print(PT[idx],"\n")
    # print("-------------------------------")
    # print("Ciphertext:")
    # print(CT,"\n")
    #CT_len = len(CT)
    #print("CT_len:",CT_len,"\n")
    #CT_decrypt = decrypt_mono(CT,test_key, prob_random_ciphertext)
    #print("Decrypted Ciphertext:")
    #print(CT_decrypt)
    #print("------------------------------- \n")

    CT_freq = return_frequencies(CT)
    CT_freq.sort()
    PT_frequencies = []
    PT_candidates = []
    PT_max_freq = []
    PT_min_freq = []
    for plaintext in PT:
        PT_freq = return_frequencies(plaintext)
        PT_freq.sort()
        candidate = isCandidate(PT_freq, CT_freq)
        PT_frequencies.append(PT_freq)
        if candidate:
            PT_candidates.append(plaintext)
        pt_highest,pt_lowest = return_highest_vals(PT_freq)
        PT_max_freq.append(pt_highest)
        PT_min_freq.append(pt_lowest)
    print("-------------------------------")
    print("Candidates:")
    for candidate in PT_candidates:
        print(candidate, "\n")
    print("-------------------------------")
    if len(PT_candidates) == 1:
        guess(PT_candidates[0])
    else:
        guess_idx = random.randint(0, len(PT_candidates)-1)
        guess(PT_candidates[guess_idx])
    
    # CT_freq = return_frequencies(CT)
    #print_frequencies(PT_max_freq, PT_min_freq, PT_frequencies, CT_freq)
    
    

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    # Calculate total time in seconds
    elapsed_time = end_time - start_time
    print(f"Raw elapsed time: {elapsed_time:.8f} seconds")

    # Convert to minutes and seconds
    minutes, seconds = divmod(elapsed_time, 60)

    # Print result in minutes and seconds
    print(f"Process time: {int(minutes)} minutes and {seconds:.2f} seconds")