import os
import sys
import random

PT = ["unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
      "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
      "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
      "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
      "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
      ]

spaces = [62,60,68,63,61]

keyspace = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

test_prob_random_ciphertext = 0.35


def encrypt(pt_number, key, probability_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    num_rand_characters = 0
    t = len(key)
    j = 0
    c = []
    m = PT[pt_number]
    L = len(m)
    max_loops = 5
    loop_count = 0
    while (ciphertext_pointer < (L+num_rand_characters)):
        #loop_count+=1
        #if(loop_count > max_loops):
        #    break
        coin_value = random.uniform(0,1)
        #print(str(probability_of_random_ciphertext))
        #print(str(coin_value))
        #print(str(probability_of_random_ciphertext <= coin_value))
        if (probability_of_random_ciphertext <= coin_value <= 1):
            j = (message_pointer%t) + 1
            # print(str(j))
            shift_val = keyspace.index(key[j%t])
            m_val = keyspace.index(m[message_pointer])
            new_val = (shift_val + m_val)%len(keyspace)
            c.append(keyspace[new_val])
            message_pointer+=1
            ciphertext_pointer+=1
        else:
            rand_char_pos = random.randint(0,26)
            c.append(keyspace[rand_char_pos])
            ciphertext_pointer+=1
            num_rand_characters+=1
    return c

def decrypt(ciphertext, key, probability_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    num_rand_characters = 0
    key_pos = 0
    t = len(key)
    j = 0
    pt = []
    L = len(ciphertext)
    while ciphertext_pointer < L:
        c_val = keyspace.index(ciphertext[ciphertext_pointer])
        j = (ciphertext_pointer%t)+1
        shift_val = keyspace.index(key[j%t])
        new_val = (c_val - shift_val)%len(keyspace)
        pt.append(keyspace[new_val])
        message_pointer+=1
        ciphertext_pointer+=1
    return ''.join(pt)
    '''
    while ciphertext_pointer < L:
        coin_value = random.uniform(0,1)  # Generate a random coin flip value

        if probability_of_random_ciphertext <= coin_value <= 1:
            j = (message_pointer % t) + 1  # Same logic as the encryption function
            shift_val = keyspace.index(key[j % t])  # Find the shift value
            c_val = keyspace.index(ciphertext[ciphertext_pointer])  # Get the ciphertext value
            original_val = (c_val - shift_val) % len(keyspace)  # Reverse the shift
            pt.append(keyspace[original_val])  # Append the decrypted character to plaintext
            message_pointer += 1
        else:
            # If it's a random character, skip it (don't increase message_pointer)
            num_rand_characters += 1
        
        ciphertext_pointer += 1  # Always move the ciphertext pointer
    
    return ''.join(pt)  # Join the list into a string
    '''
def attack(ciphertext):
    
def main():
    # keyspace_length = len(keyspace)
    # print(str(keyspace_length))
    pt_num = 1
    key = 'a'
    c = encrypt(pt_num,key,test_prob_random_ciphertext)
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
    m_d = decrypt(c,key, test_prob_random_ciphertext)
    print("------------------------------------")
    print("Decrypted: ")
    print(" ")
    print(m_d)

if __name__ == "__main__":
    main()
