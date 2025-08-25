SHAPENAMES = ['single','small TR corner','small TL corner','small BL corner','small BR corner','large TR corner','large TL corner','large BL corner','large BR corner','small square','large square','2 horizontal','3 horizontal','4 horizontal','5 horizontal','2 vertical','3 vertical','4 vertical','5 vertical']

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

shape_offsets = {}
shape_dims = {}

def initialize_shape_data():
        for shape_id in SHAPE_PATTERNS:
                shape_offsets[shape_id] = getOffsetsFromID(id)
                shape_dims[shape_id] = getDimsFromID(id)

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

class Shape:
        def __init__(self, id):
                self.name = SHAPENAMES[id]
                self.id = id
                self.pattern = SHAPE_PATTERNS[self.id]
        
        @staticmethod
        def createFromName(name):
                id = SHAPENAMES.index(name)
                return Shape(id)

        def __str__(self):
                return self.name
        
        def getOffsets(self):
                return shape_offsets[self.id]

        def getDims(self):
                return shape_dims[self.id]

        def getID(self):
                return self.id

        def getPattern(self):
                return SHAPE_PATTERNS[self.id]

        def clone(self):
                return Shape(self.id)
                
        

