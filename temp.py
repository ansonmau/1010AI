def shapePrint(s):
        counter = 0
        for i in range(5):
                for j in range(5):
                        if s[counter] == '1':
                                print('x', end = ' ')
                        else:
                                print('.', end = ' ')
                        counter+=1
                print()

SHAPE_PATTERNS = {
        'single': '1000000000000000000000000',
        'small TR corner': '1100001000000000000000000',
        'small TL corner': '1100010000000000000000000',
        'small BL corner': '1000011000000000000000000',
        'small BR corner': '0100011000000000000000000',
        'large TR corner': '1110000100001000000000000',
        'large TL corner': '1110010000100000000000000',
        'large BL corner': '1000010000111000000000000',
        'large BR corner': '0010000100111000000000000',
        'small square': '1100011000000000000000000',
        'large square': '1110011100111000000000000',
        '2 horizontal': '1100000000000000000000000',
        '3 horizontal': '1110000000000000000000000',
        '4 horizontal': '1111000000000000000000000',
        '5 horizontal': '1111100000000000000000000',
        '2 vertical': '1000010000000000000000000',
        '3 vertical': '1000010000100000000000000',
        '4 vertical': '1000010000100001000000000',
        '5 vertical': '1000010000100001000010000',
}

c = 0
for key in SHAPE_PATTERNS:
        print("{}: '{}',".format(c, SHAPE_PATTERNS[key]))
        c+=1