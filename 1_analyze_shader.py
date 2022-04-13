import os
from imports import json_viewer, compiled_shader_to_json


shader_name = compiled_shader_to_json.main()
json_viewer.main(shader_name + '.json')
os.system('pause')
