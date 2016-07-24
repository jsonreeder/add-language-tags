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

