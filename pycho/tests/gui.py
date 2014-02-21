
def test_keys():
    from pycho.gui.interaction import KEYS
    from string import ascii_uppercase as letters


    for letter in letters:
        assert letter in KEYS
        assert KEYS[letter] == ord(letter)

    assert KEYS['Space'] == 32 

def main():
    test_keys()

if __name__ == '__main__':
    main()