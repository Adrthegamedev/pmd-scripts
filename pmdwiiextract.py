import os
import sys

filepath = sys.argv[1] or input("Input filepath:")
try:
    fileout = sys.argv[2]
    if fileout[-1] != "/":
        fileout = fileout + "/"
except:
    fileout = ""


chunkcount = 0
file = open(filepath, "rb")
entirefile = file.read()
file.seek(0, os.SEEK_SET)
def fixbyte(bytee):
    if len(bytee) != 8:
        return ("0"*(8-len(bytee))) + bytee
    else:
        return bytee
    
def extractfiles(stream):
    count = 0
    exit = False
    while (count < (len(stream)) and not exit):
        datalocoffset = int("0b" + fixbyte(bin(stream[count])[2:]) + fixbyte(bin(stream[count+1])[2:]) + fixbyte(bin(stream[count+2])[2:]) + fixbyte(bin(stream[count+3])[2:]), 2)
        count = count + 4
        if(count >= (len(stream))):
            continue
        #print("datalocoffset",datalocoffset)
        #print(count)
        filesize = int("0b" + fixbyte(bin(stream[count])[2:]) + fixbyte(bin(stream[count+1])[2:]) + fixbyte(bin(stream[count+2])[2:]) + fixbyte(bin(stream[count+3])[2:]), 2)
        count = count + 4
        if(count >= (len(stream))):
            continue
        if datalocoffset == 0:
            exit = True
            continue
        #print("filesize",filesize)
        #print(count)
        hitzero = False
        filename = ""
        for i in range(20):
            if(count >= (len(stream))):
                continue
            if stream[count] == 0:
                hitzero = True
            if not hitzero:
                filename = filename + chr(stream[count])
            #print(stream[count])
            count = count + 1
            if(count >= (len(stream))):
                continue
        print("extracting filename",filename)
        with open(fileout + filename, "wb") as writefile:
            writefile.write(stream[datalocoffset:datalocoffset+filesize])
        #print(count)

def parsedecodeddata(stream, type):
    global chunkcount
    binfile = "pmdbin.bin"
    with open(fileout + binfile, "ab") as writefile:
        writefile.write(stream)
    print("wrote chunk", chunkcount, "type", type)
    chunkcount = chunkcount + 1
    writefile.close()

def decodestream(stream, tell, entirefile):
    global chunkcount
    count = 0
    decodedarray = bytearray()
    #print("streamlen: ", len(stream))
    while (count < (len(stream))):
        flag = fixbyte(bin(stream[count])[2:])
        for i in flag:
            if i == "1":
                count = count + 1
                if(count >= (len(stream))):
                    continue
                decodedarray.append(stream[count])
            if i == "0":
                count = count + 1
                if(count >= (len(stream))):
                    continue
                codeupper = fixbyte(bin(stream[count])[2:])
                count = count + 1
                if(count >= (len(stream))):
                    continue
                codelower = fixbyte(bin(stream[count])[2:])
                code = codeupper + codelower
                codenybble = int("0b" +code[:4], 2)
                coderest = int("0b" +code[4:], 2)
                #print("codenybble", codenybble)
                #print("coderestbfr", coderest)
                #print("coderestaft", (4096-coderest))
                for j in range(codenybble+3):
                    decodedarray.append(decodedarray[(((len(decodedarray))-((4096-coderest))))])
        count = count+1
    count = 0
    parsedecodeddata(decodedarray, "P")
    
def readchunk(f):
    global chunkcount
    header = f.read(4)
    if header == b"AT7P":
        size = int.from_bytes(f.read(2), "little")
        tell = f.tell()
        decodestream(f.read(size-6), tell, entirefile)
    if header == b"AT7X":
        size = int.from_bytes(f.read(2), "little")
        parsedecodeddata(f.read(size), "X")
    if header == b"AT7E":
        endfile = open(fileout + "pmdbin.bin", "rb")
        endfilestream = endfile.read()
        extractfiles(endfilestream)
        print("file end reached!")
        endfile.close()
        exit()
while True:
    readchunk(file)