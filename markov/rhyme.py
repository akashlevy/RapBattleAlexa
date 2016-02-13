from nltk.corpus import cmudict
from nltk.tokenize import wordpunct_tokenize

# Get cmudict
cmu_dict = cmudict.dict()

# Gets the syllables in a word
def get_syllables(sonnet):
  tokens = [wordpunct_tokenize(s) for s in sonnet]
  punct = set(['.', ',', '!', ':', ';'])
  filtered = [[w for w in sentence if w not in punct ] for sentence in tokens]
  last = [sentence[len(sentence) - 1] for sentence in filtered]
  syllables = [[(word, len(pron), pron) for (word, pron) in cmu_dict.items() if word == w] for w in last]
  return syllables

# Make a rhyme with s line
def rhymes(s):
  try:
    (w, l, p) = s[0]
    try:
      filtered = [wt for (wt, pt) in cmu_dict.items()
                  if l == len(pt)
                  and p[-2:] == pt[-2:]]
      return filtered
    except:
      return [w]
  except:
    return []

# Get the number of syllables in a word
def nsyl(word):
  return [len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]][0]
