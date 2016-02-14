import os
from markov import write_model

os.chdir("../songs/clean")
for file in os.listdir("."):
    print file
    write_model(file, "../../models/%s.json" % file)
