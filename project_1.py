# Conditions:
# 1. No access to key
# 2. Part of the encryption scheme is hidden

# Known:
# 1. Key is a sequence of t numbers between 0 and 26
# 2. Ciphertext looks like a sequence of symbols {space, a,..,z}
# 3. Program will be run on different L, u, and t (ex: L=600, u=5, t between 1 and 20)
# 4. The encryption algorithm can choose the next character from m[i] as:
#       a. random value in {space, a,...,z}
#       b. ciphertext character
# 5. If mono, key length is 27
#    If poly, key length can be <<27 (much smaller than 27)
# 6. Encryption algorithm uses coin generation [0,1] and compares
#    the value to prob_random_character to decide random or not
# 7. Program should work for increasing values for 
#    prob_of_random_ciphertext (e.g., 0.05, 0.10, 0.15, etc)

import os
import sys
import random

PT = ["unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
      "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
      "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
      "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
      "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
      ]

keyspace = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
prob_random_ciphertext = 0.05

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
            print("j: ",j)
            key_shift = key[j % t]
            print("key shift: ", key_shift)
            message_char_pos = keyspace.index(m[message_pointer])
            shifted_char = keyspace[(message_char_pos + key_shift) % len(keyspace)] # Shift the message char by j pos
            c.append(shifted_char) # Append shifted message character to ciphertext list
            message_pointer += 1
        else: # Insert random value
            rand_char = keyspace[random.randint(0,26)]
            c.append(rand_char)
            num_rand_characters += 1
        ciphertext_pointer += 1
    return c

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

def similarity_score(decrypted_text, reference_text):
    # Compare the two texts and count the number of matching characters
    score = sum(1 for a, b in zip(decrypted_text, reference_text) if a == b)
    return score

def find_best_plaintext_match(decrypted_text, PT):
    best_score = -1
    best_match_index = -1
    
    for i, pt in enumerate(PT):
        score = similarity_score(decrypted_text, pt)
        print(f"Similarity score with PT[{i}]: {score}")
        if score > best_score:
            best_score = score
            best_match_index = i
    
    return best_match_index  # Return the index of the best matching plaintext
    
def main():
    pt_num = 0
    key = [5, 18, 20, 7, 12, 3, 26, 11, 15, 9, 21, 0, 8, 1, 14, 25, 4, 22, 13, 2, 10, 24, 16, 17, 23, 19, 6]
    c = encrypt(pt_num, key, prob_random_ciphertext)
    str_c = ''
    for x in c:
        str_c+=x
    print("------------------------------------")
    print("Message: ")
    print(" ")
    print(PT[pt_num])
    print("------------------------------------")
    print("Ciphertext: ")
    print(" ")
    print(str_c)
    decrypted_text = decrypt(c,key, prob_random_ciphertext)
    print("------------------------------------")
    print("Decrypted: ")
    print(" ")
    print(decrypted_text)
    print("------------------------------------")
    
    matched_PT_idx = find_best_plaintext_match(decrypted_text, PT)
    print("------------------------------------")
    print(" ")
    print("My plaintext guess is:")
    print(PT[matched_PT_idx])

if __name__ == "__main__":
    main()