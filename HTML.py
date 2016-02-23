import FileIO


def html_stuff(stitched_shots, all_shots, outstitched_shots, ground_truth_file, filename1, filename2, output):
    data_prefix = 0
    data_vars1 = 'var jumpoffs = ['
    data_vars2 = 'var all_scenes = ['
    data_vars3 = 'var jo = ['
    data_suffix = 0

    #read ground truth for shot boundaries
    ground_truth_data = FileIO.read_shots_from_csv(ground_truth_file)

    #get start- and end-frames
    last_element = stitched_shots[len(stitched_shots)-1]
    for i in stitched_shots:
        a,b = ground_truth_data[i[0]]
        if i is not last_element:
            data_vars1 += str(a) + ', '
        else:
            data_vars1 += str(a) + '];\n'

    last_element = all_shots[len(all_shots)-1]
    for shot in all_shots:
        a,b = shot
        if shot is not last_element:
            data_vars2 += str(a) + ', '
        else:
            data_vars2 += str(a) + '];\n'

    #get start- and end-frames
    last_element = outstitched_shots[len(outstitched_shots)-1]
    for i in outstitched_shots:
        a,b = ground_truth_data[i]
        if i is not last_element:
            data_vars3 += str(a) + ', '
        else:
            data_vars3 += str(a) + '];\n'

    #read prefix and suffix (html and javascript code)
    with open(filename1, 'r') as f1:
        data_prefix = f1.read()
    f1.close()
    with open(filename2, 'r') as f2:
        data_suffix = f2.read()
    f2.close()

    string = data_prefix + data_vars1 + data_vars2 + data_vars3 + data_suffix

    with open(output, 'w') as f:
        f.write(string)
    f.close()
