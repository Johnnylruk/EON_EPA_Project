from removing_labels import save_transformed_file
import os

base_path = 'labels\\transformed_files'

transformed_dir_list = os.listdir(base_path)
keep_classl_list = ['0','7','5']

for file_name in transformed_dir_list:
    file_path = os.path.join(base_path, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            read_file = file.read()
    if read_file == '':
        print(file_name)
        
            

  