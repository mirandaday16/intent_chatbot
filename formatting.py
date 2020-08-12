

# Capitalizes the first letter of every word in a string, e.g. for city names
# Parameters: a place name (string) entered by the user
def cap_first_letters(phrase):
    phrase_list = [word[0].upper() + word[1:] for word in phrase.split()]
    cap_phrase = " ".join(phrase_list)
    return cap_phrase