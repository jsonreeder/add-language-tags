"""Combine

Integrates the modified lines (now containing etymologies) into the original
dictionary.

NOTE: This file contains tests, which can be run using Py Test. They will be
ignored if you simply run the script itself.
"""
from collections import defaultdict
from re import search


# Helper functions
def check_line_arabic(line):
    """Check to make sure that there is Arabic in the original line

    This is an effective way to check and make sure that the right line has
    been selected. A more detailed comparison of the lines would require
    parsing the XML, since errors can be very hard to detect due to the fact
    that adjacent lines in the dictionary share much of the same text.
    """

    return bool(search("[\u0600-ۿ]", line))


def check_multi_line_arabic(lines):
    """Check to make sure that all lines contain Arabic"""

    errors = defaultdict(list)

    for line_no, content in lines.items():
        if check_line_arabic(content) is False:
            errors[line_no] = content

    if errors:
        for line_no, content in errors.items():
            print(
                "ERROR: Line does not contain Arabic, it should not be replaced:\n{}: {}".format(
                    line_no, content))
        return False
    else:
        print("GOOD: All selected lines contain Arabic")
        return True


def parse_mod_line(i_string):
    """Parse the modified lines, as output in other script"""

    lines = i_string.splitlines()
    line_no = int(lines[0])
    content = (lines[1])

    return (line_no, content)


def parse_all_mod_lines(i_file):
    """Parse the file containing modified lines"""

    parsed_lines = defaultdict(list)

    with open(i_file, "r") as f:
        text = f.read()

    mod_lines = text.split("\n\n")

    for line in mod_lines:
        parsed_line = parse_mod_line(line)
        lno, content = parsed_line
        parsed_lines[lno] = content

    return parsed_lines


def get_line_nos_to_modify(parsed_lines):
    """Extract the line numbers to be modified from the modified lines"""

    return tuple(parsed_lines.keys())


def get_lines_to_modify(i_file, line_nos):
    """Get the lines to be modified from the original file"""

    lines = defaultdict(list)

    for lno in line_nos:
        with open(i_file, "r") as f:
            line = f.readlines()[lno]
            lines[lno] = line

    return lines


def replace_lines(i_file, o_file, lines_to_insert):
    """Insert lines into file, delete original lines in their places"""

    line_nos = get_line_nos_to_modify(lines_to_insert)
    no_lines_modified = 0

    with open(i_file, "r") as fin, open(o_file, "w") as fout:
        for idx, line in enumerate(fin):
            if idx in line_nos:
                fout.write(lines_to_insert[idx] + "\n")
                no_lines_modified += 1
            else:
                fout.write(line)

    print("Number of lines modified: {}".format(no_lines_modified))
    if len(lines_to_insert) != no_lines_modified:
        print("ERROR: {} modifications were expected.".format(
            no_lines_modified))
    else:
        print("GOOD: That's the number expected.")


# Tests
def test_check_line_arabic_fail():
    """Make sure that a given line does not contain Arabic"""

    line = '<H1B><h><hc3>110</hc3><key1>ara</key1><hc1>1</hc1><key2>ara</key2></h><body> <lex>n.</lex> <c>the_spoke_of_a_wheel</c> <ls>L.</ls> </body><tail><pc>86,2</pc> <L>15012</L></tail></H1B> '

    assert check_line_arabic(line) is False


def test_check_line_arabic_pass():
    """Make sure that a given line contains Arabic"""

    line = '<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ ارهٿ</p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3> '

    assert check_line_arabic(line)


def test_check_multi_line_arabic_fail():
    """Make sure that different lines do not match up, in multiples"""

    lines = defaultdict(list, {
        17762:
        '<H3A><h><hc3>100</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex type="inh">m.</lex> <c>a_well</c> <ls>Ra1jat.</ls> </body><tail><MW>011040</MW> <pc>86,2</pc> <L>15015</L></tail></H3A>\n',
        20012:
        '<H1><h><hc3>000</hc3><key1>allApadIna</key1><hc1>1</hc1><key2>allApadIna</key2></h><body> <lex>m.</lex> = العابدينا , <ab>N.</ab> of a king, <ls>Sa1h.</ls> (<ab>v.l.</ab>).</body><tail><pc>1316,3</pc><L supL="314380">16937.2</L></tail></H1>\n'
    })

    assert check_multi_line_arabic(lines) is False


def test_check_multi_line_match_success():
    """Make sure that different lines do not match up, in multiples"""

    lines = defaultdict(list, {
        17762:
        '<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ ارهٿ</p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3>\n',
        20012:
        '<H1><h><hc3>000</hc3><key1>allApadIna</key1><hc1>1</hc1><key2>allApadIna</key2></h><body> <lex>m.</lex> = العابدينا , <ab>N.</ab> of a king, <ls>Sa1h.</ls> (<ab>v.l.</ab>).</body><tail><pc>1316,3</pc><L supL="314380">16937.2</L></tail></H1>\n'
    })

    assert check_multi_line_arabic(lines)


def test_parse_mod_line():
    """Make sure modified lines are parsed correctly"""

    i_line = """17762
<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ <lang script="A" lang="Hindustani">ارهٿ</lang></p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3>"""
    expected = (
        17762,
        '<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ <lang script="A" lang="Hindustani">ارهٿ</lang></p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3>'
    )

    assert parse_mod_line(i_line) == expected


def test_get_line_nos():
    """Make sure that modified line numbers extracted correctly"""

    parsed = [(
        17762,
        '<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ <lang script="A" lang="Hindustani">ارهٿ</lang></p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3>'
    ), (
        20012,
        '<H1><h><hc3>000</hc3><key1>allApadIna</key1><hc1>1</hc1><key2>allApadIna</key2></h><body> <lex>m.</lex> = <lang script="A" lang="Arabic">العابدينا</lang> , <ab>N.</ab> of a king, <ls>Sa1h.</ls> (<ab>v.l.</ab>).</body><tail><pc>1316,3</pc><L supL="314380">16937.2</L></tail></H1>'
    ), (21043,
        '<H1><h><hc3>000</hc3><key1>avaraNgasAha</key1><hc1>1</hc1><key2>avaraNga-sAha</key2></h><body> <c>=_Aurungzeb_<p><c1>a_Muhammedan_king_of_the_17th_century</c1>~;~<s>sAha</s>~<c1>=_the_Persian <lang script="A" lang="Persian">شاه</lang></c1></p>.</c> </body><tail><mul/> <MW>013086</MW> <pc>102,3</pc> <L>17894</L></tail></H1>'
        )]
    expected = (17762, 20012, 21043)

    assert get_line_nos_to_modify(parsed) == expected


def test_get_lines_ingle():
    """Make sure that single lines to be modified are extracted correctly"""

    lines = get_lines_to_modify("monier.xml", [10])

    expected = defaultdict(list, {
        10:
        '<H1A><h><hc3>000</hc3><key1>a</key1><hc1>1</hc1><key2>a</key2></h><body>  <c>rarely_prefixed_to_<ab>Inf.</ab></c> <p><s>a-svaptum</s>~<c>not_to_sleep</c>~<ls>Ta1n2d2yaBr.</ls></p> <c>and_even_to_forms_of_the_finite_verb</c> <p><s>a-spfhayanti</s>~<c>they_do_not_desire</c>~<ls>BhP.</ls>~<ls>S3is3.</ls></p> <c>and_to_pronouns</c> <p><s>a-saH</s>~<c>not_he</c>~<ls>S3is3.</ls>~;~<s>a-tad</s>~<c>not_that</c>~<ls>BhP.</ls></p>  </body><tail><mul/>  <pc>1,1</pc> <L>4.1</L></tail></H1A>\n'
    })
    assert lines == expected


def test_get_lines_multiple():
    """Make sure that multiple lines to be modified are extracted correctly"""

    lines = get_lines_to_modify("monier.xml", [10, 11, 12])

    expected = defaultdict(list, {
        10:
        '<H1A><h><hc3>000</hc3><key1>a</key1><hc1>1</hc1><key2>a</key2></h><body>  <c>rarely_prefixed_to_<ab>Inf.</ab></c> <p><s>a-svaptum</s>~<c>not_to_sleep</c>~<ls>Ta1n2d2yaBr.</ls></p> <c>and_even_to_forms_of_the_finite_verb</c> <p><s>a-spfhayanti</s>~<c>they_do_not_desire</c>~<ls>BhP.</ls>~<ls>S3is3.</ls></p> <c>and_to_pronouns</c> <p><s>a-saH</s>~<c>not_he</c>~<ls>S3is3.</ls>~;~<s>a-tad</s>~<c>not_that</c>~<ls>BhP.</ls></p>  </body><tail><mul/>  <pc>1,1</pc> <L>4.1</L></tail></H1A>\n',
        11:
        '<H1A><h><hc3>000</hc3><key1>a</key1><hc1>1</hc1><key2>a</key2></h><body>  <c>occasionally_denoting_comparison</c> <p><s>a-brAhmaRa</s>~<c>like_a_<as0>Brahman</as0><as1><s>brahman</s></as1></c>~<ls>T.</ls></p>  </body><tail><mul/>  <pc>1,1</pc> <L>4.2</L></tail></H1A>\n',
        12:
        '<H1A><h><hc3>000</hc3><key1>a</key1><hc1>1</hc1><key2>a</key2></h><body>  <c>sometimes_disparagement</c> <p><s>a-yajYa</s>~<c>a_miserable_sacrifice</c></p>  </body><tail><mul/>  <pc>1,1</pc> <L>4.3</L></tail></H1A>\n'
    })
    assert lines == expected


# Implementation
def main():
    """Implement helper functions"""

    # Get data
    print("Getting data")
    lines_to_insert = parse_all_mod_lines("monier_lines_with_tags.xml")
    line_nos_to_modify = get_line_nos_to_modify(lines_to_insert)
    lines_to_modify = get_lines_to_modify("monier.xml", line_nos_to_modify)

    # Validate data
    print("Validating data")
    check_multi_line_arabic(lines_to_modify)

    # Make the changes
    print("Making the changes")
    replace_lines("monier.xml", "monier_with_tags.xml", lines_to_insert)
    print("Complete")


main()
