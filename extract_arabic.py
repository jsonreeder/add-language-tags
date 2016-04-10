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

    results = extract_lines_add_tags(i_file, arabic_re, tag)
    for no, matches, line, newline in results:
        print("Line: {0}\nMatch(es): {1}\nOriginal Line:\n{2}Line With Tags:\n{3}".format(no, matches, line, newline))

main()
