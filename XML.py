import csv


class Image:
    title = -1
    id = -1
    tags = []

    def __init__(self, title):
        self.title = title

class Tag:
    accuracy = 0.0
    id = ''
    tag_title = ''
    tagtags = []

    def __init__(self, id, accuracy, tag_title, tagtags):
        self.id = id
        self.accuracy = accuracy
        self.tag_title = tag_title
        self.tagtags = tagtags


#reads the caffe_output file and creates a xml for html input
def create_XML(filename):
    data = read_caffe_file(filename)
    write_XML('html_output/XML.xml', data)


#reads the caffe_output file
def read_caffe_file(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')       #create reader
        row_count = sum(1 for row in reader)

        f.seek(0)
        reader = csv.reader(f, delimiter=';')       #create reader

        image_count = row_count / 6

        #for every image
        for i in range(0,image_count):
            #get the data for the object

            #get title
            line1 = reader.next()[0]
            idx11 = 26
            idx12 = line1.find('.jpg')
            title = line1[idx11:idx12]
            title = int(title)

            #create the Image object
            image = Image(title)

            #get the tags
            idx21 = 6
            tags = []
            for j in range(0,5):
                line2 = reader.next()[0]

                #get accuracy
                accuracy = float(line2[0:idx21])

                #get tag id (e.g. n0977058)
                tag_id = line2[10:19]

                #get tags
                line2 = line2[20:len(line2) - 1]
                tag_title = line2
                split_tags = line2.split(', ')

                #create Tag object
                tag = Tag(tag_id, accuracy, tag_title, split_tags)
                tags.append(tag)

            image.tags = tags

            data.append(image)

    # To sort the list in place...
    data.sort(key=lambda x: x.title)

    #write id's after sorting
    i = 0
    for image in data:
        image.id = i
        i += 1

    return data


# creates a xml file for html input
def write_XML(filename, data):
    with open(filename, 'w') as f:
        #header
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n'
                '<images>\n\n')

        #write data for every image
        for image in data:
            f.write('<image>\n')

            f.write('\t<id>' + str(image.id) + '</id>\n')
            f.write('\t<title>' + str(image.title) + '</title>\n')

            for tag in image.tags:
                if tag.accuracy > 0.0:
                    f.write('\t<tag>\n')
                    f.write('\t\t<id>' + str(tag.id) + '</id>\n')
                    f.write('\t\t<accuracy>' + str(tag.accuracy) + '</accuracy>\n')
                    f.write('\t\t<title>' + str(tag.tag_title) + '</title>\n')

                    for tagtag in tag.tagtags:
                        f.write('\t\t<tagtag>' + tagtag + '</tagtag>\n')

                    f.write('\t</tag>\n')

            f.write('</image>\n')

        #footer
        f.write('\n</images>')
