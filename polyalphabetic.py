import random
import Levenshtein

# List of plaintexts
PT = ["unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
      "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
      "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
      "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
      "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
      ]

# Keyspace
keyspace = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
prob_random_ciphertext = 0.05

def encrypt(pt_number, key, prob_of_random_ciphertext):
    ciphertext_pointer = 0
    message_pointer = 0
    num_rand_characters = 0
    t = len(key)
    c = [] 
    m = PT[pt_number] 
    L = len(m)  # Length of the message
    while (ciphertext_pointer < (L + num_rand_characters)):
        coin_value = random.uniform(0,1)  # coin generation return value [0,1]
        # Case 1: Encrypt and return ciphertext
        if (prob_of_random_ciphertext <= coin_value <= 1):
            j = (message_pointer % t) + 1  # Shift value
            key_shift = key[j % t]
            message_char_pos = keyspace.index(m[message_pointer])
            shifted_char = keyspace[(message_char_pos + key_shift) % len(keyspace)]  # Shift the message char 
            c.append(shifted_char) 
            message_pointer += 1
        else:  # Case 2: Insert random value
            rand_char = keyspace[random.randint(0,26)]
            c.append(rand_char)
            num_rand_characters += 1
        ciphertext_pointer += 1
    return ''.join(c)

def match_ciphertext(CT, PT):
    min_distance = float('inf')
    matched_plaintext = None
    for plaintext in PT:
        distance = Levenshtein.distance(CT, plaintext)
        print(f"Levenshtein distance to plaintext: {distance}")
        if distance < min_distance:
            min_distance = distance
            matched_plaintext = plaintext
    return matched_plaintext

def main():
    test_key = [random.randint(0,26) for _ in range(10)]  # Random key of length 10
    CT = encrypt(1, test_key, prob_random_ciphertext)  # Encrypt the second plaintext
    print("Ciphertext:")
    print(CT)
    print("\nMatching plaintext...")
    matched_plaintext = match_ciphertext(CT, PT)
    print("\nMost likely plaintext:")
    print(matched_plaintext)

if __name__ == "__main__":
    main()