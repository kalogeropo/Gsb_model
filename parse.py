# bulk collection path
from utilities.parsers import group_queries_and_relevance, npl_doc_parser, npl_q_r_parser,parse_cran_file, parse_cranqrel, parse_cranqry

import pandas as pd

# NPL PARSER

# npl_docs_path = "./experiments/collections/Unparsed/NPL/doc-text" 
# #experiments/collections/Unparsed/NPL/dest/docs

# npl_docs_dest_path = "./experiments/collections/Unparsed/NPL/dest/docs"

# npl_q_r_path = "./experiments/collections/Unparsed/NPL/dest"

# test = npl_doc_parser(npl_docs_path, npl_docs_dest_path)

# npl_q_path = "./experiments/collections/Unparsed/NPL/query-text"
# npl_r_path = "./experiments/collections/Unparsed/NPL/rlv-ass"
# test1 = npl_q_r_parser(npl_q_r_dest_path = npl_q_r_path,npl_r_path=npl_r_path)




# Fixing file path with raw string
cran_file_path = r"experiments\raw_collections\cran\cran.all.1400"
qry_file_path = r"experiments\raw_collections\cran\cranqry"
qrel_file_path = r"experiments\raw_collections\cran\cranqrel"

# Call the parser function
document_list = parse_cran_file(cran_file_path,True)

# for doc in document_list:
#     print(doc["id"],"\n",doc["abstract"])

# Display a sample of parsed documents
sample_df = pd.DataFrame(document_list[:5])
#print(sample_df)



queries = parse_cranqry(qry_file_path)
relevance_judgments = group_queries_and_relevance(queries,parse_cranqrel(qrel_file_path))
#print(queries,relevance_judgments)
