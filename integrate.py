from pprint import pprint

def parse_decision(lines):
    """Returns a list of the information neede to add lang tags:
       the word, it's language tag, and the line"""

    cases = []
    word = ""
    decision = ""
    line = 0

    for i, l in enumerate(lines):
        if l.startswith("** "):
            cases.append((word, decision, line))
            word = l[8:]
            decision = ""
            line = 0
        elif l.startswith("*** Decision"):
            decision = lines[i+1]
        elif l.startswith("*** Line"):
            line = lines[i+1]

    return cases[1:]

def add_tag(word, language, text):
    """Add a language tag around a word in a string"""

    tag_open = "<lang script=\"A\" lang=\"%s\">" % (language)
    tag_close = "</lang>"

    before, after = text.split(word)
    before += tag_open
    after = tag_close + after

    return before + word + after

# Parse decisions
with open("cases.org", "r") as f:
    lines = f.read().splitlines()
    lines_cases = lines[13:]
decisions = parse_decision(lines_cases)

# Make sure that all tags are acceptable
acceptable_tags = ['Hindustani', 'Turkish', 'Arabic', 'Persian']
unique_tags = set([d[1] for d in decisions])
for u in unique_tags:
    if u not in acceptable_tags:
        print("Warning: the tag %s is unacceptable." % (u))

# Add tags to a new copy of the dictionary
lines_to_change = [int(d[2]) for d in decisions]
with open("monier.xml", "r") as f:
    lines = f.read().splitlines()
    with open("monier_with_lang_tags.xml", "w") as w:
        for i, line in enumerate(lines):
            if i in lines_to_change:
                w.write(add_tag(d[0], d[1], lines[int(d[2])]))
            else:
                w.write(line)
# with open("monier_with_lang_tags.xml", "w") as f:
#     pass
# for d in decisions:
#     changes.append(add_tag(d[0], d[1], lines[int(d[2])]))

# print(lines_to_change)
