import pack as p
import Bots.bot_helpers as b

import hand_helpers
def test_value(name, expected_value, cards):
    hand = hand_helpers.Hand(name)
    for card in cards:
        hand.add_card(hand_helpers.Shorthand[card])
    if expected_value != hand.get_value():
        print("expected: %i" % expected_value)
        print("actual: %i" % hand.get_value())
        print(i)
        return False
    return True


def run_tests():

    test_value('pair_twos', 302, ['2h', '2c'])
    test_value('3-high', 3, ['3h', '2h'])
    test_value('4-high', 4, ['4h', '2h'])
    test_value('flush', 730, ['3h', '2h', 'Qh', '4d', '6h', '10s', '7h'])
    test_value('four-of-a-kind', 907, ['7h', '7d', '7c', '4d', '6h', '10s', '7s'])
    test_value('straight', 606, ['3h', '2h', '4c', '5d', '6d'])
    test_value('set', 503, ['3h', '2h', '3d', '4c', '3s'])

    flush_Q_7_6_3_2 = b.value_of(['3h', '2h', 'Qh', '4d', '6h', '10s', '7h'])
    flush_Q_6_4_3_2 = b.value_of(['3h', '2h', 'Qh', '4h', '6h', '10s', '7d'])
    assert flush_Q_7_6_3_2 > flush_Q_6_4_3_2
    four_value = b.value_of(['7h', '7d', '7c', '4d', '6h', '10s', '7s'])
    flush_value = b.value_of(['3h', '2h', 'Qh', '4h', '6h', '10s', '7d'])
    assert four_value > flush_value



HEART = '♥'
CLUB = '♣'
DIAMOND = '♦'
SPADE = '♠'

if __name__ == '__main__':
    run_tests()