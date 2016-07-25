from collections import defaultdict

# Helper functions
def parse_decision(lines):
    """Return a list of the information neede to add lang tags:
       the word, it's language tag, and the line"""

    cases = []
    word = ""
    decision = ""
    line = 0

    for i, l in enumerate(lines):
        if l.startswith("** "):
            cases.append((word, decision, int(line)))
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

# Run functions
def parse_decisions_doc():
    """Run function parse_decisions() on input file"""

    global decisions

    with open("cases.org", "r") as f:
        lines = f.read().splitlines()
        lines_cases = lines[19:]
    decisions = parse_decision(lines_cases)

def test_tags():
    """Make sure that all tags are acceptable"""

    acceptable_tags = ['Hindustani', 'Turkish', 'Arabic', 'Persian']
    unique_tags = set([d[1] for d in decisions])

    for u in unique_tags:
        if u not in acceptable_tags:
            print("Warning: the tag %s is unacceptable." % (u))

def create_output_file():
    """Add tags to a special output file"""

    changes = defaultdict(list)

    # Prepare dictionary of changes
    with open("monier.xml", "r") as f:
        lines = f.read().splitlines()
        for d in decisions:
            if d[2] in changes:
                changes[d[2]] = add_tag(d[0], d[1], changes[d[2]])
            else:
                changes[d[2]] = add_tag(d[0], d[1], lines[d[2]])

    # Output to file
    with open("monier_lines_with_tags.xml", "w") as f:
        for k,v in sorted(changes.items()):
            f.write(str(k) + "\n")
            f.write("".join(v) + "\n\n")

def run():
    parse_decisions_doc()
    test_tags()
    create_output_file()

run()
