log = open("./git_log_react.txt", "r")

file_changes_count = {}
files_adjacency_mtx = {}
file_relationships_count = {}


def update_file_changes_count(file):
    if file in file_changes_count:
        file_changes_count[file] += 1
    else:
        file_changes_count[file] = 1


def update_file_relationships_count(file):
    if file in file_relationships_count:
        file_relationships_count[file] += 1
    else:
        file_relationships_count[file] = 1


def increment_tuple_count(file1, file2):
    if (file1, file2) in files_adjacency_mtx:
        files_adjacency_mtx[(file1, file2)] += 1
    elif (file2, file1) in files_adjacency_mtx:
        files_adjacency_mtx[(file2, file1)] += 1
    else:
        files_adjacency_mtx[(file1, file2)] = 1


def update_adjacency_matrix(files):
    for file1 in files:
        update_file_changes_count(file1)
        for file2 in files:
            if file1 != file2:
                increment_tuple_count(file1, file2)
                update_file_relationships_count(file1)
                update_file_relationships_count(file2)


def read_commit_files():
    files = []
    while True:
        line = log.readline()
        if line == "\n" or line == "" or line == "###NEW_COMMIT###\n":
            break
        files.append(line)
    return files


def find_max_value_in_hash(the_hash):
    max_value = -1
    max_key = None
    for key in the_hash.keys():
        if max_value < the_hash[key]:
            max_value = the_hash[key]
            max_key = key
    return max_key, max_value


for line in log:
    if line == "###NEW_COMMIT###\n":
        files = read_commit_files()
        update_adjacency_matrix(files)


print("Files that changed most together:",
      find_max_value_in_hash(files_adjacency_mtx))
print("File with more relationships:",
      find_max_value_in_hash(file_relationships_count))

file_score = {}
for file in file_changes_count.keys():
    multiplier = 1
    if file in file_relationships_count:
        multiplier = file_relationships_count[file]
    file_score[file] = file_changes_count[file] * multiplier

print("Most important file:", find_max_value_in_hash(file_score))
