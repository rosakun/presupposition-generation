def starts_with_vowel(word):
    return str(word)[0] in ["a","e","i","o","u","A","E","I","O","U"]

def regular_plural(word):
    number = word.morph.get("Number")
    if number == []:
        return False
    else:
        if number[0] == 'Sing':
            return False
        else:
            return True