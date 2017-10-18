from pyrr import Vector3
from material_mesh import MaterialMesh, Face

class MtlParser:

    def __init__(self):
        self.words = []
        self.cur_line = 0
        self.cur_word = 0
        self.mtl_map = {}
        self.cur_mtl = None

    def parse_string(self, content):
        lines = content.split('\n')

        for line in lines:
            self.cur_line += 1
            self.words = line.split(' ')

            # Handle comments
            if len(self.words) > 0 and len(self.words[0]) > 0 and self.words[0][0] == '#':
                continue

            self.cur_word = 0
            while self.cur_word < len(self.words):
                self.parse_word(self.words[self.cur_word])
                self.cur_word += 1

    def parse_word(self, word):
        if word == 'newmtl':
            mtl_name = self.seek_next_word()
            self.cur_mtl = MaterialMesh()
            self.mtl_map[mtl_name] = self.cur_mtl
        elif word == 'Ns':
            self.cur_mtl.mtl.specular_exponent = self.read_float() / 1000.0
        elif word == 'd':
            self.cur_mtl.mtl.alpha = 1.0 - self.read_float()
        elif word == 'Ka':
            self.cur_mtl.mtl.ambient_color = self.read_color()
        elif word == 'Kd':
            self.cur_mtl.mtl.diffuse_color = self.read_color()
        elif word == 'Ks':
            self.cur_mtl.mtl.specular_color = self.read_color()
        elif word == 'Ke':
            self.cur_mtl.mtl.emissive_color = self.read_color()
    
    def seek_next_word(self):
        self.cur_word += 1
        if self.cur_word >= len(self.words):
            raise Exception('Error in parsing material file: missing token (line {})'.format(self.cur_line))
            return None
        return self.words[self.cur_word]

    def read_float(self):
        word = self.seek_next_word()
        try:
            ret = float(word)
            return ret
        except:
            raise Exception('Error in parsing material file: invalid float value (line {})'.format(self.cur_line))
            return None

    def read_color(self):
        return Vector3([self.read_float(), self.read_float(), self.read_float()])

class ObjParser:

    def __init__(self):
        self.words = []
        self.cur_line = 0
        self.cur_word = 0
        self.mtl_map = {}
        self.cur_mtl = None
        self.vertices = []
        self.texcoords = []
        self.normals = []

    def parse_string(self, mtl_map, content):
        self.mtl_map = mtl_map
        lines = content.split('\n')

        for line in lines:
            self.cur_line += 1
            self.words = line.split(' ')

            # Handle comments
            if len(self.words) > 0 and len(self.words[0]) > 0 and self.words[0][0] == '#':
                continue

            self.cur_word = 0
            while self.cur_word < len(self.words):
                self.parse_word(self.words[self.cur_word])
                self.cur_word += 1

    def parse_word(self, word):
        if word == 'usemtl':
            mtl_name = self.seek_next_word()
            self.cur_mtl = self.mtl_map[mtl_name]
            if self.cur_mtl is None:
                raise Exception('Error in parsing object file: missing material definition (line {})'.format(self.cur_line))
            else:
                self.cur_mtl.mesh.vertices = self.vertices
                self.cur_mtl.mesh.texcoords = self.texcoords
                self.cur_mtl.mesh.normals = self.normals
        elif word == 'v':
            self.vertices.append(self.read_vector_3D())
        elif word == 'vn':
            self.normals.append(self.read_vector_3D())
        elif word == 'vt':
            self.texcoords.append(self.read_vector_2D())
        elif word == 'f':
            self.cur_mtl.mesh.faces.append(self.read_face())

    def seek_next_word(self):
        self.cur_word += 1
        if self.cur_word >= len(self.words):
            raise Exception('Error in parsing object file: missing token (line {})'.format(self.cur_line))
            return None
        return self.words[self.cur_word]

    def read_float(self):
        word = self.seek_next_word()
        try:
            ret = float(word)
            return ret
        except:
            raise Exception('Error in parsing object file: invalid float value (line {})'.format(self.cur_line))
            return None

    def read_vector_3D(self):
        return [self.read_float(), self.read_float(), self.read_float()]

    def read_vector_2D(self):
        return [self.read_float(), self.read_float()]

    def read_face(self):
        face = Face()

        for i in range(0, 3):
            indices = self.seek_next_word().split('/')
            face.vertices.append(self.get_int(indices[0]) - 1)
            if len(indices) > 1 and indices[1] != '':
                face.texcoords.append(self.get_int(indices[1]) - 1)
            if len(indices) > 2:
                face.normals.append(self.get_int(indices[2]) - 1)
        
        return face

    def get_int(self, string):
        try:
            ret = int(string)
            return ret
        except:
            raise Exception('Error in parsing object file: invalid int value (line {})'.format(self.cur_line))
            return None
