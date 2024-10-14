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
max_number_to_return = 6

def return_highest_vals(freq_list):
    temp_list = []
    for val in freq_list:
        temp_list.append(val)
    temp_list.sort()
    top_vals = []
    bottom_vals = []
    for x in range(0,max_number_to_return):
        bottom_vals.append(temp_list[x])
        top_vals.append(temp_list[len(keyspace)-x-1])
    return top_vals, bottom_vals
    

def return_frequencies(input_string):
    to_return = []
    #Counter(input_string) = 
    for x in range(0,len(keyspace)):
        count = 0
        for c in input_string:
            if c == keyspace[x]:
                count+=1
        to_return.append(count)
    return to_return

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

def encrypt_mono(pt_number, key, prob_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    num_rand_characters = 0
    t = len(key)
    c = []
    m = PT[pt_number] #message
    L = len(m) #message length
    while(ciphertext_pointer < (L+num_rand_characters)):
        coin_value = random.uniform(0,1)
        if(prob_of_random_ciphertext <= coin_value <=1):
            c.append(keyspace[key[keyspace.index(m[message_pointer])]])
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

def main():
    test_key = [5,4,1,2,9,3,0,6,17,8,10,11,16,13,14,15,12,7,18,20,19,21,22,23,24,25,26]
    CT = encrypt_mono(1,test_key,prob_random_ciphertext)
    CT_len = len(CT)
    print("CT_len: " + str(CT_len))
    CT_decrypt = decrypt_mono(CT,test_key, prob_random_ciphertext)
    print(CT)
    print("")
    print(CT_decrypt)

    CT_freq = return_frequencies(CT)
    
    print(" ")
    PT_frequencies = []
    PT_max_freq = []
    PT_min_freq = []
    PT_max_freq_index = []
    for pt_str in PT:
        freq_of_pt = return_frequencies(pt_str)
        PT_frequencies.append(freq_of_pt)
        pt_highest,pt_lowest = return_highest_vals(freq_of_pt)
        PT_max_freq.append(pt_highest)
        PT_min_freq.append(pt_lowest)
        
    count_iter = 0
    print("PT Frequencies: ")
    for freq_iter in range(0,len(PT_frequencies)):
        count_iter+=1
        print(PT_frequencies[freq_iter])
        
    print(" ")
    for x in range(0,len(PT_max_freq)):
        # observed that space and letter e are highest frequency of all strings
        print("PT:" + str(x))
        print("Highest:")
        print(PT_max_freq[x])
        print("Lowerst:")
        print(PT_min_freq[x])

    #CT_highest = max(CT_freq)
    CT_highest,CT_lowest = return_highest_vals(CT_freq)
    print("CT Frequencies")
    print(CT_freq)
    print("CT Highest")
    print(CT_highest)
    print("CT Lowest")
    print(CT_lowest)

if __name__ == "__main__":
    main()