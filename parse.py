# bulk collection path
from utilities.parsers import npl_doc_parser, npl_q_r_parser

npl_docs_path = "./experiments/collections/Unparsed/NPL/doc-text"
#experiments/collections/Unparsed/NPL/dest/docs

npl_docs_dest_path = "./experiments/collections/Unparsed/NPL/dest/docs"

npl_q_r_path = "./experiments/collections/Unparsed/NPL/dest"

#test = npl_doc_parser(npl_docs_path, npl_docs_dest_path)

npl_q_path = "./experiments/collections/Unparsed/NPL/query-text"
npl_r_path = "./experiments/collections/Unparsed/NPL/rlv-ass"
test1 = npl_q_r_parser(npl_q_r_dest_path = npl_q_r_path,npl_r_path=npl_r_path)
