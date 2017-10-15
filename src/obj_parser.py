import numpy
from material_mesh import MaterialMesh

class MtlParser:

    def __init__(self):
        self.words = []
        self.cur_line = 0
        self.cur_word = 0
        self.mtl_map = {}
        self.cur_mtl = None

    def parseString(self, content):
        lines = content.split('\n')

        for line in lines:
            self.cur_line += 1
            self.words = line.split(' ')

            # Handle comments
            if len(self.words) > 0 and len(self.words[0]) > 0 and self.words[0][0] == '#':
                continue

            self.cur_word = 0
            while self.cur_word < len(self.words):
                self.parseWord(self.words[self.cur_word])
                self.cur_word += 1

    def parseWord(self, word):
        if word == 'newmtl':
            mtl_name = self.seekNextWord()
            self.cur_mtl = MaterialMesh()
            self.mtl_map[mtl_name] = self.cur_mtl
        elif word == 'Ns':
            self.cur_mtl.mtl.specularExponent = self.readNumber()
        elif word == 'd':
            self.cur_mtl.mtl.transparency = 1.0 - self.readNumber()
        elif word == 'Ka':
            self.cur_mtl.mtl.ambient = self.readColor()
        elif word == 'Kd':
            self.cur_mtl.mtl.diffuse = self.readColor()
        elif word == 'Ks':
            self.cur_mtl.mtl.specular = self.readColor()
    
    def seekNextWord(self):
        self.cur_word += 1
        if self.cur_word >= len(self.words):
            raise Exception('Error in parsing material file: missing token (line {})'.format(self.cur_line))
            return None
        return self.words[self.cur_word]

    def readNumber(self):
        word = self.seekNextWord()
        try:
            ret = float(word)
            return ret
        except:
            raise Exception('Error in parsing material file: invalid float value (line {})'.format(self.cur_line))
            return None

    def readColor(self):
        return numpy.array([self.readNumber(), self.readNumber(), self.readNumber()])
