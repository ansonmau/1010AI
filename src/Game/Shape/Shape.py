from random import randrange
class Shape:
        NAMES = [ 'NULLPIECE',
                 'single',
                 'small TR corner',
                 'small TL corner',
                 'small BL corner',
                 'small BR corner',
                 'large TR corner',
                 'large TL corner',
                 'large BL corner',
                 'large BR corner',
                 'small square',
                 'large square',
                 '2 horizontal',
                 '3 horizontal',
                 '4 horizontal',
                 '5 horizontal',
                 '2 vertical',
                 '3 vertical',
                 '4 vertical',
                 '5 vertical' ]

        PATTERNS = { 0: '0000000000000000000000000',
                    1: '1000000000000000000000000',
                    2: '1100001000000000000000000',
                    3: '1100010000000000000000000',
                    4: '1000011000000000000000000',
                    5: '0100011000000000000000000',
                    6: '1110000100001000000000000',
                    7: '1110010000100000000000000',
                    8: '1000010000111000000000000',
                    9: '0010000100111000000000000',
                    10: '1100011000000000000000000',
                    11: '1110011100111000000000000',
                    12: '1100000000000000000000000',
                    13: '1110000000000000000000000',
                    14: '1111000000000000000000000',
                    15: '1111100000000000000000000',
                    16: '1000010000000000000000000',
                    17: '1000010000100000000000000',
                    18: '1000010000100001000000000',
                    19: '1000010000100001000010000'
                    }

        def __init__(self, id):
            self._id      = id
            self._name    = Shape.NAMES[id]
            self._pattern = Shape.PATTERNS[id]
            self._offsets = Shape._get_offsets_from_id(id)
            self._dims    = self.__calc_dims_from_offsets()

            # self._dims = Shape._get_dims_from_id(id)
        
        # ╭────────────────────────────────────────────────╮
        # │                      API                       │
        # ╰────────────────────────────────────────────────╯

        def get_offsets(self):
            return self._offsets

        def get_dimensions(self):
            return self._dims

        def get_id(self):
            return self._id

        def get_pattern(self):
            return self._pattern

        def get_arr_repr(self):
            arr = []
            for i in range(5):
                row = []
                for j in range(5):
                    row.append(int(self._pattern[i+j]))
                arr.append(row)

            return arr

        def clone(self):
            return Shape(self._id)
                
        def __str__(self):
            return self._name

        def __calc_dims_from_offsets(self):
            """
            quicker method to calculate dims but requires offsets to be
            calculated already. better to use this and use the staticmethod
            for external one-time use
            """
            if self._id == 0:
                return (0,0)

            height = max([x[0] for x in self._offsets])
            width = max([x[1] for x in self._offsets])

            return (height+1, width+1)


        @staticmethod
        def from_name(name):
            id = Shape.NAMES.index(name)
            return Shape(id)

        @staticmethod
        def get_random_shape():
            return Shape(randrange(1, len(Shape.PATTERNS)))
        
        @staticmethod
        def get_null_shape():
            return Shape(0)

        @staticmethod
        def get_all_shapes(ignore=[]):
            def trim(l1, l2):
                """
                removes elements from list
                """
                return [x for x in l1 if x not in l2]

            all_s = [Shape(s) for s in Shape.PATTERNS.keys()]
            return trim(all_s, ignore) 

        @staticmethod
        def _get_offsets_from_id(shapeID):
            offsets = []
            pattern = Shape.PATTERNS[shapeID]
            for rowCount in range(5):
                    for colCount in range(5):
                            ind = rowCount*5 + colCount
                            if pattern[ind] == '1':
                                    offsets.append((rowCount, colCount))
        
            return offsets

        @staticmethod
        def _get_dims_from_id(shapeID):
            # assumes offsets are already generated
            spriteHeight = 5
            spriteWidth = 5

            width = 0
            height = 0

            pattern = Shape.PATTERNS[shapeID]

            for row in range(spriteHeight):
                for col in range(spriteWidth):
                    ind = row*5 + col
                    if pattern[ind] == '1':
                        height = row
                        if col > width:
                            width = col
                                        
            return (height+1, width+1)


