import json
import random
from collections import defaultdict
from sys import argv

DELIM = ' '

# Builds the Markov model
def build_model(infile):
  chain = defaultdict(list)
  with open(infile, 'r') as markov_file:
    lines = markov_file.readlines()
  for line in lines:
    line = line.rstrip('\n').lower().strip()
    words = line.split(' ')
    pairs = zip(words, words[1:])

    for first, second in pairs:
      chain[first].append(second)

    chain[words[-1]].append(DELIM)
    chain[DELIM].append(words[0])
  return chain

# Writes the Markov model to a json file
def write_model(infile, markov):
  chain = build_model(infile)
  with open(markov, 'w') as outfile:
    json.dump(chain, outfile)

# Generates a line of rap
def generate_line(model):
  line = []
  current = DELIM
  while not (current == DELIM and line):
    current = random.choice(model[current])
    line.append(current)

  verse = ' '.join(line).strip()
  return verse

# Gets a good verse for a rap
def get_good_verse(model):
  verse = generate_line(model)
  while len(verse.split(' ')) != 8:
    verse = generate_line(model)
  return verse

# Chooses a rhyme
def choose_rhymes(first_word, second_word, r_dict_a, r_dict_b):
  # No rhymes exist for either words
  if len(r_dict_a) < 2 and len(r_dict_b) < 2:
    return first_word, second_word

  # No rhyme exists for first word
  if len(r_dict_a) < 2:
    return random.choice(r_dict_b), second_word

  # No rhyme exists for second word
  if len(r_dict_b) < 2:
    return first_word, random.choice(r_dict_a)

  if len(first_word) < len(second_word):
    return random.choice(r_dict_b), second_word

  return first_word, random.choice(r_dict_a)

# Makes a rhyming scheme
def rhymify(model, lines):
  sonnet = []
  for i in range(int(lines)):
    sonnet.append(get_good_verse(model))

  from rhyme import get_syllables, rhymes
  syllables = get_syllables(sonnet)

  rhyme_dict = [rhymes(s) for s in syllables]

  index = 0

  fixed = []
  while(index < len(sonnet)):
    first = sonnet[index].split(' ')
    second = sonnet[index+1].split(' ')

    first[-1], second[-1] = choose_rhymes(first[-1],
                                          second[-1],
                                          rhyme_dict[index],
                                          rhyme_dict[index+1])

    fixed.append(' '.join(first))
    fixed.append(' '.join(second))
    index += 2

  final_rhyme = ''
  for line in fixed:
    final_rhyme += line + ', '
  return final_rhyme[:-2]

def get_rhyme(chain, lines):
  return rhymify(chain, lines).replace("?", "'").replace("imma", "ima").replace("im", "i'm")

def get_model(markov):
  with open(markov) as file:
    chain = defaultdict(list)
    chain.update(json.load(file))
  return chain
