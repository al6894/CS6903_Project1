import time
import numpy as np
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

# Approach 3: Improves on previous frequency analysis, uses relative
# frequency, adjusts frequency based on random ciphertext chance.

# Get the text's character relative
def get_relative_freq(text):
    frequencies = Counter(text)
    L = sum(frequencies.values()) # length of plaintext
    relative_freq = np.array([frequencies.get(char, 0) / L for char in keyspace])
    return relative_freq

# Adjust frequencies for random insertions
def adjust_freq(pt_freq, prob_random_ciphertext):
    # Assumption: the random characters are uniformly distributed over the keyspace
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
    
def main():
    #prob_random_ciphertext = 0.05
    print("Enter the ciphertext:")
    CT = input()
    ct_freq = get_relative_freq(CT)

    avg_pt_length = sum(len(pt) for pt in PT) / len(PT)
    prob_random_ciphertext = max(0, (len(CT) - avg_pt_length) / len(CT))
    # Store distances (essentially a match score) for each plaintext
    distances = []
    # Loop through all plaintexts and calculate their relative frequencies.
    for i in range(len(PT)):
        pt_text = PT[i]
        pt_freq = get_relative_freq(pt_text)
        adjusted_pt_freq = adjust_freq(pt_freq, prob_random_ciphertext)
        distance = compare_frequency_profiles(ct_freq, adjusted_pt_freq)
        distances.append((i, distance))

    distances.sort(key=lambda x: x[1])
    best_match_idx, best_distance = distances[0]
    
    print("My plaintext guess is:")
    print(PT[best_match_idx])

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Raw elapsed time: {elapsed_time:.8f} seconds")
    minutes, seconds = divmod(elapsed_time, 60)