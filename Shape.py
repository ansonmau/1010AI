SHAPE_PATTERNS = {
        0: '1000000000000000000000000',
        1: '1100001000000000000000000',
        2: '1100010000000000000000000',
        3: '1000011000000000000000000',
        4: '0100011000000000000000000',
        5: '1110000100001000000000000',
        6: '1110010000100000000000000',
        7: '1000010000111000000000000',
        8: '0010000100111000000000000',
        9: '1100011000000000000000000',
        10: '1110011100111000000000000',
        11: '1100000000000000000000000',
        12: '1110000000000000000000000',
        13: '1111000000000000000000000',
        14: '1111100000000000000000000',
        15: '1000010000000000000000000',
        16: '1000010000100000000000000',
        17: '1000010000100001000000000',
        18: '1000010000100001000010000'
}

SHAPENAMES = ['single','small TR corner','small TL corner','small BL corner','small BR corner','large TR corner','large TL corner','large BL corner','large BR corner','small square','large square','2 horizontal','3 horizontal','4 horizontal','5 horizontal','2 vertical','3 vertical','4 vertical','5 vertical']

SHAPENAME_TO_ID = {
        'single': 0,
        'small TR corner': 1,
        'small TL corner': 2,
        'small BL corner': 3,
        'small BR corner': 4,
        'large TR corner': 5,
        'large TL corner': 6,
        'large BL corner': 7,
        'large BR corner': 8,
        'small square': 9,
        'large square': 10,
        '2 horizontal': 11,
        '3 horizontal': 12,
        '4 horizontal': 13,
        '5 horizontal': 14,
        '2 vertical': 15,
        '3 vertical': 16,
        '4 vertical': 17,
        '5 vertical': 18
}

class Shape:
        def __init__(self, name):
                self.name = name
                self.id = SHAPENAME_TO_ID[name]
                self.pattern = SHAPE_PATTERNS[self.id]

                self.offsets = []
                self.dims = ()
                
                self._initDims()
                self._initOffsets()
        
        def createFromID(ID):
                shapeName = SHAPENAMES[ID]
                return Shape(shapeName)

        def __str__(self):
                return self.name
        
        def getOffsets(self):
                return self.offsets

        def getDims(self):
                return self.dims

        def getID(self):
                return self.id

        def clone(self):
                newShape = Shape(self.name)
                return newShape
        
        def getPos(self):
                return self.position
        
        def getName(self):
                return self.name
        
        def _initOffsets(self):
                self.offsets = []
                for rowCount in range(5):
                        for colCount in range(5):
                                ind = rowCount*5 + colCount
                                if self.pattern[ind] == '1':
                                        self.offsets.append((rowCount, colCount))
                
        def _initDims(self):
                spriteHeight = 5
                spriteWidth = 5

                width = 0
                height = 0

                for row in range(spriteHeight):
                        for col in range(spriteWidth):
                                ind = row*5 + col
                                if self.pattern[ind] == '1':
                                        height = row
                                        if col > width:
                                                width = col
                                        
                self.dims = (height+1, width+1)
        

        def getDimsFromID(shapeID):
                spriteHeight = 5
                spriteWidth = 5

                width = 0
                height = 0

                pattern = SHAPE_PATTERNS[shapeID]

                for row in range(spriteHeight):
                        for col in range(spriteWidth):
                                ind = row*5 + col
                                if pattern[ind] == '1':
                                        height = row
                                        if col > width:
                                                width = col
                                        
                return (height+1, width+1)

        def getOffsetsFromID(shapeID):
                offsets = []
                pattern = SHAPE_PATTERNS[shapeID]
                for rowCount in range(5):
                        for colCount in range(5):
                                ind = rowCount*5 + colCount
                                if pattern[ind] == '1':
                                        offsets.append((rowCount, colCount))
                
                return offsets