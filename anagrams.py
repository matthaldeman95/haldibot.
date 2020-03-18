import boto3
from os import path

# This whole thing is UGLY and INEFFICIENT and thats OK

if not path.exists("anagrams.txt"):
    s3 = boto3.client('s3')
    s3.download_file('haldibot-assets', 'anagrams.txt', 'anagrams.txt')

with open('anagrams.txt') as infile:
    words = infile.read().split('\n')


def is_perfect_anagram(word1, word2):
    if len(word1) != len(word2):
        return False
    word2 = list(word2)
    for letter in word1:
        if letter not in word2:
            return False
        else:
            word2.remove(letter)
    return True

def remainder_if_contains(smallerWord, largerWord):
    largerWord = list(largerWord)
    for letter in smallerWord:
        if letter not in largerWord:
            return None
        else:
            largerWord.remove(letter)
    return "".join(largerWord)


def recursiveAnagrams(word, level=0):
    if level >= 4:
        return None
    solutions = []
    intro_string = "\t" * level
    # print(f"{intro_string}Solving word {word}")
    # if(level >= 1):
    #     sys.exit(0)
    for x in words:
        if len(x) > len(word):
            continue
        if len(x) == len(word):
            if is_perfect_anagram(x, word):
                solutions.append(x)
            continue
        else:
            remainder = remainder_if_contains(x, word)
            if remainder and len(remainder) >= 2:
                # print(f"Partial match:  {x}")
                remainder_anagram = recursiveAnagrams(remainder, level=level+1)
                if remainder_anagram:
                    for result in remainder_anagram:
                        solutions.append(x + " " + result)
    if len(solutions) >= 1:
        if (level == 0):
            print(f"Found anagrams for word {word}:  {str(solutions)}")
        return solutions
    else:
        # print(f"{intro_string}Nothing found...")
        return None
