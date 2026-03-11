import os
import sys

filepath = sys.argv[1] or input("Input filepath:")
try:
    fileout = sys.argv[2]
except:
    fileout = "out.smd"

endianness = None
#chunkcount = 0
file = open(filepath, "rb")
entirefile = file.read()
file.seek(0, os.SEEK_SET)
def fixbyte(bytee):
    if len(bytee) != 8:
        return ("0"*(8-len(bytee))) + bytee
    else:
        return bytee
def header(f):
    global endianness
    newstream = bytearray()
    header = bytearray(f.read(4))
    unk7 = bytearray(f.read(4))
    flen = bytearray(f.read(4))
    version = bytearray(f.read(2))
    unk1 = bytearray(f.read(1))
    unk2 = bytearray(f.read(1))
    unk3 = bytearray(f.read(4))
    unk4 = bytearray(f.read(4))
    year = bytearray(f.read(2))
    month = bytearray(f.read(1))
    day = bytearray(f.read(1))
    hour = bytearray(f.read(1))
    minute = bytearray(f.read(1))
    second = bytearray(f.read(1))
    centisecond = bytearray(f.read(1))
    fname = bytearray(f.read(16))
    unk5one = bytearray(f.read(2))
    unk5two = bytearray(f.read(2))
    unk6 = bytearray(f.read(4))
    unk8 = bytearray(f.read(4))
    unk9 = bytearray(f.read(4))
    
    flen.reverse()
    version.reverse()
    year.reverse()
    unk5one.reverse()

    if header == bytearray(b"smdb"):
        endianness = "little"
        newstream.extend(bytearray(b"smdl"))
    else:
        endianness = "big"
        newstream.extend(bytearray(b"smdb"))
    newstream.extend(unk7)
    newstream.extend(flen)
    newstream.extend(version)
    newstream.extend(unk1)
    newstream.extend(unk2)
    newstream.extend(unk3)
    newstream.extend(unk4)
    newstream.extend(year)
    newstream.extend(month)
    newstream.extend(day)
    newstream.extend(hour)
    newstream.extend(minute)
    newstream.extend(second)
    newstream.extend(centisecond)
    newstream.extend(fname)
    newstream.extend(unk5one)
    newstream.extend(unk5two)
    newstream.extend(unk6)
    newstream.extend(unk8)
    newstream.extend(unk9)
    
    with open(fileout, "ab") as writefile:
        writefile.write(newstream)
    writefile.close()
def song(f):
    newstream = bytearray()
    header = bytearray(f.read(4))
    unk1one = bytearray(f.read(2))
    unk1two = bytearray(f.read(2))
    unk2 = bytearray(f.read(4))
    unk3 = bytearray(f.read(4))
    unk4 = bytearray(f.read(2))
    tpqn = bytearray(f.read(2))
    unk5 = bytearray(f.read(2))
    nbtrks = bytearray(f.read(1))
    nbchans = bytearray(f.read(1))
    unk6 = bytearray(f.read(4))
    unk7 = bytearray(f.read(4))
    unk8one = bytearray(f.read(2))
    unk8two = bytearray(f.read(2))
    unk9one = bytearray(f.read(2))
    unk9two = bytearray(f.read(2))
    unk10 = bytearray(f.read(2))
    unk11 = bytearray(f.read(2))
    unk12 = bytearray(f.read(4))
    unkpad = bytearray(f.read(16))
    
    unk1two.reverse()
    unk3.reverse()
    unk4.reverse()
    tpqn.reverse()
    unk8two.reverse()
    unk9one.reverse()
    unk9two.reverse()

    newstream.extend(header)
    newstream.extend(unk1one)
    newstream.extend(unk1two)
    newstream.extend(unk2)
    newstream.extend(unk3)
    newstream.extend(unk4)
    newstream.extend(tpqn)
    newstream.extend(unk5)
    newstream.extend(nbtrks)
    newstream.extend(nbchans)
    newstream.extend(unk6)
    newstream.extend(unk7)
    newstream.extend(unk8one)
    newstream.extend(unk8two)
    newstream.extend(unk9one)
    newstream.extend(unk9two)
    newstream.extend(unk10)
    newstream.extend(unk11)
    newstream.extend(unk12)
    newstream.extend(unkpad)

    for i in range(int.from_bytes(nbtrks, endianness)):
        trk_label = bytearray(f.read(4))
        trk_param1one = bytearray(f.read(2))
        trk_param1two = bytearray(f.read(2))
        trk_param2 = bytearray(f.read(4))
        trk_chunklen = bytearray(f.read(4))

        trk_param1two.reverse()
        trk_chunklen.reverse()

        newstream.extend(trk_label)
        newstream.extend(trk_param1one)
        newstream.extend(trk_param1two)
        newstream.extend(trk_param2)
        newstream.extend(trk_chunklen)
        for i in range(int.from_bytes(trk_chunklen, endianness)):
            newstream.extend(f.read(1))
        for i in range(3 - ((f.tell()+3) % 4)):
            newstream.extend(f.read(1))

    eoc_label = bytearray(f.read(4))
    eoc_param1one = bytearray(f.read(2))
    eoc_param1two = bytearray(f.read(2))
    eoc_param2 = bytearray(f.read(4))
    eoc_chunklen = bytearray(f.read(4))

    eoc_param1two.reverse()
    eoc_chunklen.reverse()

    newstream.extend(eoc_label)
    newstream.extend(eoc_param1one)
    newstream.extend(eoc_param1two)
    newstream.extend(eoc_param2)
    newstream.extend(eoc_chunklen)
    
    with open(fileout, "ab") as writefile:
        writefile.write(newstream)
    writefile.close()
def examine(f):
    header(f)
    song(f)
examine(file)
file.close()