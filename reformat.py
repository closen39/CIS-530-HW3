def reformat():
    f = open("named_entities.txt")
    out = open("named_entities_fixed.txt", "w")
    for line in f:
        new_line = ""
        for idx, let in enumerate(line):
            if idx < len(line) - 1 and line[idx + 1] == ":":
                new_line += str(int(line[idx]) + 1)
            else:
                new_line += str(line[idx])
        out.write(new_line)
    out.close()

def main():
    reformat()

if __name__ == '__main__':
    main()

