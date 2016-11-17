from utils import distance


def test_main(string1, string2):
    print distance(string1, string2)


test_main('blue', 'bule')
test_main('ocean', 'ocena')
test_main('water', 'waterr')
test_main('space', 'sapce')
test_main('coconut', 'coocntu')
test_main('fire', 'frie')
