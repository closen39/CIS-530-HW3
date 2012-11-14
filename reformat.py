def reformat():
    f = open("fileList")
    out = open("fileListOut", "w")
    for line in f:
        out.write('/home1/c/cis530/hw3/data/training/all_files/' + line.rstrip() + "\n")
    out.close()

def main():
    reformat()

if __name__ == '__main__':
    main()

