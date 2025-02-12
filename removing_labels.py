# read the file content
# transform the file content
# then rewrite it the way i want 

file_path = 'file_text.txt'
keep_classl_list = ['2','11','8','1']

# This is for reading file
with open(file_path, 'r') as file:
    read_file = file.read()

#This for transforming the file
split_file = read_file.split('\n')
new_file = []
for line in split_file:
    split_line = line.split()
    if split_line and split_line[0] in keep_classl_list:
        new_file.append(line)

string_empty = ''

for st in new_file:
    string_empty += st + '\n'
    

with open('Removed_classe.txt', 'w') as file:
    file.write(string_empty)

