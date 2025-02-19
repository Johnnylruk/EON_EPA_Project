import os
# read the file content
# transform the file content
# then rewrite it the way i want 

base_path = 'labels'
dir_list = os.listdir(base_path)

keep_classl_list = ['0','7','5']

def read_file(file_to_read: str, base_file_path: str):
    file_path = os.path.join(base_file_path, file_to_read)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            read_file_name = file.read()
    return read_file_name

def split_file(file_to_split: str, list_of_label_classes: list) -> list:
    split_file = file_to_split.split('\n')
    new_file = []
    for line in split_file:
        split_line = line.split()
        if split_line and split_line[0] in list_of_label_classes:
            new_file.append(line)
    return new_file

def save_transformed_file(file_to_save: list, path_to_save: str, directory_name_to_save: str, file_to_save_name: str):
     
    file_to_be_saved = ''

    for st in file_to_save:
        file_to_be_saved += st + '\n'

    directory = os.path.join(path_to_save, directory_name_to_save)
    if not os.path.exists(directory):
        os.makedirs(directory)
    save_location = os.path.join(directory, f'{file_to_save_name}')
    with open(save_location, 'w') as file:
        file.write(file_to_be_saved)
    return file_to_be_saved

def save_all_transformed_files(files_to_be_saved: list, base_path: str):
    
    for file in files_to_be_saved:
        get_file = read_file(file, base_path)
        splited_file = split_file(get_file, keep_classl_list)
        save_transformed_file(splited_file, base_path, 'transformed_files', file)
    
save_all_transformed_files(dir_list, base_path)














