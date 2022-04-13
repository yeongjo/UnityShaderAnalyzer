import os
import re

import pyjsonviewer
import jsonpickle


def save_to_file(file_name, context):
    f = open(file_name, 'w')
    f.write(context)
    f.close()


def compile_shader(file_name):
    stream = os.popen('malioc -c Mali-G76 ' + file_name)  # Yes It's hardcoded..
    result = stream.read()
    return result


class Shader:
    def __init__(self):
        self.vert = ''
        self.frag = ''
        self.name = ''
        self.result_vert = ''
        self.result_frag = ''

    def __init__(self, name, vert, frag):
        self.vert = vert
        self.frag = frag
        self.name = name

    def set_shader_code_vert(self, vert):
        self.vert = vert

    def set_shader_code_frag(self, frag):
        self.frag = frag

    def set_name(self, name):
        self.name = name

    def compile_vert(self):
        save_to_file('saves/shader.vert', self.vert)
        self.result_vert = compile_shader('saves/shader.vert')

    def compile_frag(self):
        save_to_file('saves/shader.frag', self.frag)
        self.result_frag = compile_shader('saves/shader.frag')

    def compile(self):
        self.compile_vert()
        self.compile_frag()

    def compile_and_print(self):
        print('START Shader Info ============================================')
        print(self.name)
        print('START Vert Info ==============================================')
        print(self.compile_vert())
        print('START Frag Info ==============================================')
        print(self.compile_frag())
        print('END Shader Info ==============================================')


def print_every_shader_code(shader_list):
    for i in range(len(shader_list)):
        print('\n\n' + str(i) + '. Start Vert ============================================')
        print(shader_list[i].name + '\n')
        print(shader_list[i].vert)
        print('\n\n' + str(i) + '. End Vert Start Frag ============================================')
        print(shader_list[i].frag)
        print(str(i) + '. Frag End ============================================\n\n')


def print_every_shader_result(shader_list):
    for i in range(len(shader_list)):
        print(str(i) + ' ====================START===================== ' + str(i))
        shader_list[i].compile_and_print()
        print(str(i) + ' ===================END===================== ' + str(i))
        print('\n\n\n')


def compile_every_shader(shader_list):
    for shader in shader_list:
        shader.compile()
    print(str(len(shader_list)) + ' Shaders Compile Done!')


def export_to_json(shader_name, shader_list):
    with open(shader_name+'.json', 'w') as f:
        json_data = jsonpickle.encode(shader_list)
        f.write(json_data)


def main():
    save_data_file_name = 'saves/save_data.txt'
    input_question = 'Paste file path: '
    last_path = ''
    if os.path.isfile(save_data_file_name):
        save_data_txt = open(save_data_file_name, 'r')
        if save_data_txt is not None:
            last_path = save_data_txt.read()
            if last_path != '':
                input_question = input_question + '(If you want to use this path:( \''+last_path+'\') Press Enter.): '
        save_data_txt.close()

    # Get input file path
    shader_file_path = input(input_question)
    if shader_file_path == '':
        shader_file_path = last_path

    # Save last path
    save_data_txt = open(save_data_file_name, 'w')
    save_data_txt.write(shader_file_path)
    save_data_txt.close()

    f = open(shader_file_path, 'r')
    shader_code = f.read()
    f.close()
    shader_name_find_txt = 'Compiled-'
    shader_name_start_idx = shader_file_path.rfind(shader_name_find_txt)+len(shader_name_find_txt)
    shader_name_end_idx = shader_file_path.rfind('.shader')
    shader_name = shader_file_path[shader_name_start_idx:shader_name_end_idx]

    print('\nProgressing..\n')

    shader_code = re.sub('UNITY_BINDING\([\d]+\)', '', shader_code, flags=re.MULTILINE)

    splitted_shader_code = re.split('\n\n#endif\n\n\n', shader_code, flags=re.MULTILINE)

    shader_list = []

    re_keywords = re.compile('Global Keywords: [\D]+\n')
    re_vertex = re.compile('Shader Disassembly:\n#ifdef VERTEX\n')
    re_frag = re.compile('\n\n#endif\n#ifdef FRAGMENT\n')

    shader_names = re_keywords.findall(shader_code)
    for i in range(len(shader_names)):
        shader_names[i] = shader_names[i][:-1]  # Remove last \n

    for code in splitted_shader_code:
        searched_m = re_vertex.search(code)
        if searched_m is not None:
            vert_frag_code = code[searched_m.end():]
            vert_frag_split_code = re_frag.split(vert_frag_code)
            shader = Shader(shader_names[len(shader_list)], vert_frag_split_code[0], vert_frag_split_code[1])
            shader_list.append(shader)

    # print_every_shader_code(shader_list)  # For debug
    # print_every_shader_result(shader_list)
    compile_every_shader(shader_list)
    export_to_json(shader_name, shader_list)
    return shader_name


if __name__ == '__main__':
    main()
