import csv,codecs,cStringIO
import sys, Image, ImageDraw, ImageFont, os
import numpy

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

image_paths = []
with open('dataset.csv','rb') as fin:
    rank = 0
    reader = UnicodeReader(fin)
    for line in reader:
        if rank == 0:
            pass
        elif rank == 1:
            print line
            image = Image.new('RGBA', (120,120),(0,0,0))
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("simsun.ttc", 120)
            draw.text((0,0), unicode(line[0].encode("utf-8"),"UTF-8"), font=font)
            del draw
            filename = "../machine_teaching/teacher/static/teacher/images/chinese/" + str(rank) + "/" + line[2] + ".JPG"
            image_paths.append(filename)
            dir = os.path.dirname(filename)
            try:
                os.stat(dir)
            except:
                os.mkdir(dir)
            image.save(filename, "JPEG")
        rank += 1
class_names = numpy.array([str(r) for r in range(1,1001)])
class_names.tofile("chinese/class_names.npy")
numpy.ones(1000).tofile("chinese/class_num_images.npy")




