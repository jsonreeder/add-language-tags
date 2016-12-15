"""Combine

Integrates the modified lines (now containing etymologies) into the original
dictionary.
"""


def check_line_match(ori_line, mod_line):
    """Check to make sure that the lines match up"""

    if ori_line[10] == mod_line[10]:
        return True
    else:
        print(
            "ERROR: These were expected to match:\nOriginal:\n{}\nModified:\n{}\n".format(
                ori_line, mod_line))
        return False


def test_check_line_match_fail():
    """Make sure that different lines do not match up"""

    ori_line = '<H1B><h><hc3>110</hc3><key1>ara</key1><hc1>1</hc1><key2>ara</key2></h><body> <lex>n.</lex> <c>the_spoke_of_a_wheel</c> <ls>L.</ls> </body><tail><pc>86,2</pc> <L>15012</L></tail></H1B> '
    mod_line = '<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ <lang script="A" lang="Hindustani">ارهٿ</lang></p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3> '

    assert check_line_match(ori_line, mod_line) is False


def test_check_line_match_pass():
    """Make sure that similar lines do match up"""

    ori_line = '<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ ارهٿ</p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3> '
    mod_line = '<H3><h><hc3>110</hc3><key1>araGawwa</key1><hc1>3</hc1><key2>ara--Gawwa</key2></h><body> <lex>m.</lex> <c>a_wheel_or_machine_for_raising_water_from_a_well_<p><ab>Hind.</ab>_ <lang script="A" lang="Hindustani">ارهٿ</lang></p></c> <ls>Pan5cat.</ls> </body><tail><pc>86,2</pc> <L>15014</L></tail></H3> '

    assert check_line_match(ori_line, mod_line)
