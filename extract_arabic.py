import re

def extract_lines_add_tags(i_file, regex, tag):
    """
    Find all words of text in a given regex.
    Surround all of those words with a given tag.
    Return a set of the original line and the new line now with tags.
    """

    ret = []


    with open(i_file, "r") as f:
        for i, line in enumerate(f):
            match = re.search(regex, line)
            if match:
                newline = line
                all_matches = re.findall(regex, line)
                for m in all_matches:
                    m_with_tags = "{0}{1}{2}".format(tag[0], m, tag[1])
                    newline = newline.replace(m, m_with_tags)
                ret.append([i, all_matches, line, newline])

    return ret

def main():
    i_file = "monier.xml"
    # A regex to match all Arabic characters
    arabic_re = "[\u0600-\u06FF]+"
    tag = ['<lang type="A">', '</lex>']
    XML = "</?[A-Za-z0-9]+/?>"

    results = extract_lines_add_tags(i_file, arabic_re, tag)
    print()
    for no, matches, line, newline in results:
        no_tags = re.sub(XML, "", line)
        no_tags = re.sub("_", " ", no_tags)

        # Check for etymologies given in text
        if "Pers" in line and "Arab" in line:
            guess = "Persian and Arabic"
        elif "Pers" in line:
            guess = "Persian"
        elif "Arab" in line:
            guess = "Arabic"
        else:
            guess = False

        if guess:
            beginning = """* TODO {0}

** Guess
{1}""".format(", ".join(matches), guess)
        else:
            beginning = "* {0}".format(", ".join(matches))

        # Print the rest
        print("""{1}

** Decision


** Line w/o XML:
{3}
** Original Line:
#+begin_example xml
{2}#+end_example

** Line:
{0}
""".format(no, beginning, line, no_tags))

main()
