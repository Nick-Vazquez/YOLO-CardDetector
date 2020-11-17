import glob
from xml.dom import minidom
from labels import get_labels


def convert_coordinates(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert(path):
    # for each file ending in .xml in the specified path
    for filename in glob.glob(path + "*.xml"):
        xml = minidom.parse(filename)

        # output filename - replace .xml with .txt
        fname_out = (filename[:-4] + '.txt')

        with open(fname_out, "w") as file:
            # get data needed for writing
            items = xml.getElementsByTagName('object')
            size = xml.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            # for each object within the image
            for item in items:
                label = "-1"
                classid = (item.getElementsByTagName('name')[0]).firstChild.data
                labels = get_labels()
                if classid in labels:
                    label = str(labels[classid])
                else:
                    print("warning: label '%s' not in look-up table" % classid)

                # get bbox coordinates
                xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data

                box_not_converted = (float(xmin), float(xmax), float(ymin), float(ymax))
                box_converted = (convert_coordinates((width, height), box_not_converted))

                # write to the file in format <object-class> <x> <y> <width> <height>
                file.write(label + " " + " ".join([("%.6f" % a) for a in box_converted]) + '\n')

    print("Wrote " + str(len(glob.glob(path + "*.xml"))) + " .txt files")


path = "assets/test_zipped/"
convert(path)
