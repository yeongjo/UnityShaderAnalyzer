import os
from imports import json_viewer

file_name = input('Typing json file name want to view(Example:syj-Uber.json): ')
json_viewer.main(file_name)
os.system('pause')
