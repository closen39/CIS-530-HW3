def reformat():
    f = open("fileList2")
    out = open("fileList2Out", "w")
    for line in f:
        out.write('/home1/c/cis530/hw3/data/testing/all_files/' + line.rstrip() + "\n")
    out.close()

def main():
    reformat()

if __name__ == '__main__':
    main()

