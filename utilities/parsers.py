# NPL collection


def write_file(filename, list_to_write):
    print(filename)
    with open(filename, "w") as fd:
        for word in list_to_write:
            fd.write("%s\n" % word)
    return 0


def npl_q_r_parser(npl_q_r_dest_path, npl_q_path=None, npl_r_path=None):
    # Handling queries
    temp = []
    relevant = []
    queries = []
    if npl_q_path:
        with open(npl_q_path, "r") as fd:
            with open(npl_q_path, 'r') as fd:
                line = fd.readline()
                sline = line.split()
                print(line,sline)
                while line and line != "END":
                    line = fd.readline()
                    queries.append(line)
                    fd.readline()
                    fd.readline()
            qs = []
            for sub in queries:
                qs.append(sub.replace("\n", ""))
            print(qs)
            res = write_file("/".join([npl_q_r_dest_path,"queries.txt"]),qs)

    # Handling relevant
    if npl_r_path:
        with open(npl_r_path, "r") as fd:
            line = fd.readline()
            sline = line.split()
            #print(line, sline)
            while sline[0] != "END":
                while sline[0] != "/":
                    line = fd.readline()
                    sline = line.split()
                    temp += sline
                    #print(temp)
                line = fd.readline()
                sline = line.split()
                # print(sline)
                relevant.append(temp)
                temp = []
                if len(sline) == 0 or sline[0] == "END":
                    break
        rel_to_write = []
        for list in relevant:
            del list[-1]
            rel_to_write.append(list)
        print(rel_to_write)
        with open("/".join([npl_q_r_dest_path,"relevant.txt"]),"w") as fd:
            for item in rel_to_write:
                item.append("\n")
                fd.write(" ".join(item))
    return 0


def npl_doc_parser(npl_docs_path, npl_docs_dest_path):
    fd = open(npl_docs_path, "rt")
    line = fd.readline()
    text_as_list = line.split()
    file = text_as_list[0]
    count = 0
    while line != "END":
        if count == 0:
            temp_text_list = text_as_list
        else:
            line = fd.readline()
            text_as_list = line.split()
            temp_text_list = []
        if len(text_as_list) > 0:
            try:
                while text_as_list[0] != "/":
                    temp_text_list.extend(text_as_list)
                    line = fd.readline()
                    text_as_list = line.split()
            except IndexError:
                break
        filename = "/".join([npl_docs_dest_path, temp_text_list[0]])
        text = temp_text_list[1:len(temp_text_list)]
        print(text)
        count += 1
        print(temp_text_list[0])
        wrt = write_file(filename, text)
    fd.close()
    return 0
