import os
# read the file content
# transform the file content
# then rewrite it the way i want 

base_path = 'labels'
dir_list = os.listdir(base_path)

keep_classl_list = ['2','11','8','1']


for file_name in dir_list:
    file_path = os.path.join(base_path, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            read_file = file.read()

    split_file = read_file.split('\n')
    new_file = []
    for line in split_file:
        split_line = line.split()
        if split_line and split_line[0] in keep_classl_list:
            new_file.append(line)

    string_empty = ''

    for st in new_file:
        string_empty += st + '\n'

    directory = os.path.join(base_path, 'transformed_files')
    if not os.path.exists(directory):
        os.makedirs(directory)
    save_location = os.path.join(directory, f'{file_name}')
    with open(save_location, 'w') as file:
        file.write(string_empty)
    







