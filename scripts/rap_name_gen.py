import os
with open("rapper_schema.txt", "w") as outfile:
    for infile in os.listdir("../models"):
        outfile.write("StartLike\tlike {%s|Rapper}\n" % infile[:-5])
