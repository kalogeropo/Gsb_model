# NPL collection
import re
import string


def write_file(filename, list_to_write):
    print(filename)
    
    with open(filename, "w") as fd:
        for word in list_to_write:
            if word != "":
                fd.write("%s\n" % word.upper())
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
            res = write_file("/".join([npl_q_r_dest_path,"Queries.txt"]),qs)

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
        with open("/".join([npl_q_r_dest_path,"Relevant.txt"]),"w") as fd:
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
        filename = "/".join([npl_docs_dest_path, temp_text_list[0].zfill(5)])
        text = temp_text_list[1:len(temp_text_list)]
        print(text)
        count += 1
        print(temp_text_list[0])
        wrt = write_file(filename, text)
    fd.close()
    return 0

# CRAN parser

def parse_cran_file(file_path, write=False):
    documents = []
    current_doc = None
    section = None

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Detect new document
            if line.startswith('.I'):
                if current_doc:  # Save the previous document before starting a new one
                    documents.append(current_doc)
                
                doc_id = int(line.split()[1])
                current_doc = {"id": doc_id, "title": "", "authors": "", "bibliography": "", "abstract": ""}
                section = None  # Reset section

            elif line.startswith('.T'):
                section = 'title'
            elif line.startswith('.A'):
                section = 'authors'
            elif line.startswith('.B'):
                section = 'bibliography'
            elif line.startswith('.W'):
                section = 'abstract'
            elif section and current_doc:
                # Append text to the current section
                current_doc[section] += (" " if current_doc[section] else "") + line

    # Ensure the last document is added
    if current_doc:
        documents.append(current_doc)
    if write:
        write_cran_files(documents)
    return documents

def parse_cranqry(file_path,write=False):
    queries = []
    current_query = None
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith('.I'):
                if current_query:
                    queries.append(current_query)
                query_id = int(line.split()[1])
                current_query = {"id": query_id, "text": ""}
            elif line.startswith('.W'):
                continue  # Skip section header
            elif current_query:
                current_query["text"] += (" " if current_query["text"] else "") + line
    
    if current_query:
        queries.append(current_query)
    
    return queries

def parse_cranqrel(file_path):
    relevance_judgments = []
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                query_id, doc_id, relevance = map(int, parts)
                relevance_judgments.append({
                    "query_id": query_id,
                    "doc_id": doc_id,
                    "relevance": relevance
                })
    
    return relevance_judgments

def group_queries_and_relevance(queries, relevance_judgments,write_cran_path,rel=False,query=False):
    grouped_data = []
    q_id = -1
    index = 0
    for query in queries:
        if q_id != query["id"]:
            index+=1
            q_id = query["id"]
            relevant_docs = [doc["doc_id"] for doc in relevance_judgments if doc["query_id"] == index]
            #print(q_id,relevant_docs)
            grouped_data.append(relevant_docs)
            print(q_id,relevant_docs)
            if rel:
                with open("/".join([write_cran_path,"Relevant.txt"]),"a") as fd:
                        print(q_id,relevant_docs)  
                        print(" ".join(str(rel) for rel in relevant_docs)) 
                        fd.write(" ".join(str(rel) for rel in relevant_docs))
                        fd.write("\n")
    if query:
        queries = [query["text"].translate(str.maketrans('', '',string.punctuation)) for query in queries]
        write_file("/".join([write_cran_path,"Queries.txt"]),queries)
        # query_id = query["id"]
        # print(relevance_judgments[query_id])
        #relevant_docs = relevance_judgments.get(query_id, [])
        #grouped_data.append(relevant_docs)
    return grouped_data

def write_cran_files(docs, filepath=r"experiments\collections\CRAN\docs"):
    for doc in docs:
        filename = f"{filepath}/{str(doc['id']).zfill(5)}"
        write_file(filename, doc["abstract"].translate(str.maketrans('', '',string.punctuation)).strip("\n").split(" ")) 
    return 0       