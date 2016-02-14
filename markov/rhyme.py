from cmudict import cmu_dict
def get_syllables(sonnet):

  from nltk.tokenize import wordpunct_tokenize
  tokens = [wordpunct_tokenize(s) for s in sonnet]
  punct = set(['.', ',', '!', ':', ';'])
  filtered = [ [w for w in sentence if w not in punct ] for sentence in tokens]
  last = [ sentence[len(sentence) - 1] for sentence in filtered]

  syllables = [[(word, len(pron), pron) for (word, pron) in cmu_dict if word == w] for w in last]
  return syllables

def rhymes(s):
  try:
    (w, l, p) = s[0]
    try:
      filtered = [wt for (wt, pt) in cmu_dict
                  if l == len(pt)
                  and p[-2:] == pt[-2:]]
      return filtered
    except:
      return [w]
  except:
    return []