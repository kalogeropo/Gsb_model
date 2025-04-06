#dont forget to pip instal beir

import csv
import time
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval import models
from beir.retrieval.models import SPLADE
from beir.retrieval.models import SPARTA
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES
from beir.retrieval.evaluation import EvaluateRetrieval
import os
import json

import logging
import pathlib

#utill functions
def convert_folder_to_beir_corpus(folder_path, output_path="CF_corpus.jsonl"):
    corpus = []
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Skip non-file entries
        if not os.path.isfile(file_path):
            continue

        doc_id = os.path.splitext(filename)[0]  # remove file extension

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                continue  # skip empty files

            title = "doc_" + doc_id  # or use the first line as title
            text = " ".join([line.strip() for line in lines[0:]])

            doc = {
                "_id": doc_id,
                "title": title,
                "text": text
            }
            corpus.append(doc)

    # Write to corpus.jsonl
    with open(output_path, "w", encoding="utf-8") as out_f:
        for doc in corpus:
            out_f.write(json.dumps(doc) + "\n")

    print(f"Converted {len(corpus)} documents to {output_path}")
    return corpus

def convert_queries(input_txt, output_jsonl="queries.jsonl"):
    with open(input_txt, "r", encoding="utf-8") as f:
        queries = [line.strip() for line in f if line.strip()]

    with open(output_jsonl, "w", encoding="utf-8") as out_f:
        for idx, query in enumerate(queries):
            obj = {
                "_id": f"q{idx+1}",
                "text": query
            }
            out_f.write(json.dumps(obj) + "\n")

    print(f"Converted {len(queries)} queries to {output_jsonl}")

def convert_relevance_file(relevant_file, output_file="qrels_test.tsv"):
    with open(relevant_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("query-id\tdoc-id\tlabel\n")
        for i, line in enumerate(lines):
            query_id = f"q{i+1}"
            
            doc_ids = line.split()
            for doc_id in doc_ids:
                out.write(f"{query_id}\t{doc_id.zfill(5)}\t1\n")

    print(f"Parsed {len(lines)} queries to {output_file}")
if __name__ == "__main__":

    #folder_path = r"experiments\collections\CF"
    # folder_path = r"experiments\collections\CRAN"
    # convert_folder_to_beir_corpus(folder_path+"\docs")
    # convert_relevance_file(folder_path+"\Relevant.txt")
    # convert_queries(folder_path+"\Queries.txt")
    
    ### Setup logging
    logging.basicConfig(level=logging.INFO)
    dataset_path = "CRAN"

    #### Load dataset
    corpus, queries, qrels = GenericDataLoader(dataset_path).load(split="qrels_test")
    print(f"Loaded {len(corpus)} documents, {len(queries)} queries, and {len(qrels)} relevance labels.")
    
    #### Load model (you can change this to other SBERT models)
    dense_models = {
    # Reliable classics
    "multi-qa-MiniLM": "sentence-transformers/multi-qa-MiniLM-L6-cos-v1",
    "multi-qa-mpnet-base": "sentence-transformers/multi-qa-mpnet-base-dot-v1",
    "msmarco-distilbert-base-v3": "sentence-transformers/msmarco-distilbert-base-v3",


    # Modern lightweight or mid-range (RAM friendly)
    "bge-base-en-v1.5": "BAAI/bge-base-en-v1.5",
    "gte-base": "thenlper/gte-base",
    "e5-base-v2": "intfloat/e5-base-v2",
    }
    # Loop through each model and evaluate
    results_csv = "CRAN_beir_model_results_k1209.csv"

    # Initialize CSV with headers
    with open(results_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "model_name",
            "map@1209", "precision@1209", "recall@1209",
            "retrieval_time_s", "evaluation_time_s", "total_time_s"
        ])

    # Loop through each model and evaluate
    for model_name, model_path in dense_models.items():
        print(f"\n--- Running model: {model_name} ---")

        start_model = time.time()
        beir_model = DRES(models.SentenceBERT(model_path), batch_size=32)
        retriever = EvaluateRetrieval(beir_model, score_function="dot")

        # Retrieval
        start_retrieve = time.time()
        results = retriever.retrieve(corpus, queries)
        end_retrieve = time.time()

        # Evaluation
        start_eval = time.time()
        scores = retriever.evaluate(qrels, results, k_values=[1209])
        print(type(scores))  # Should show <class 'dict'>
        print(scores)
        end_eval = time.time()

        total_time = time.time() - start_model
        retrieval_time = end_retrieve - start_retrieve
        evaluation_time = end_eval - start_eval

        # Log results
        print(f"Results for {model_name}:\n{scores}")
        print(f"⏱ Retrieval time: {retrieval_time:.2f}s")
        print(f"⏱ Evaluation time: {evaluation_time:.2f}s")
        print(f"⏱ Total time: {total_time:.2f}s")

        # Extract metrics
        map_ = scores[1].values()
        precision = scores[-1].values()
        recall = scores[2].values()

        # Write to CSV
        with open(results_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                model_name,
                map_, precision, recall,
                f"{retrieval_time:.2f}",
                f"{evaluation_time:.2f}",
                f"{total_time:.2f}"
            ])
    

    splade_encoder = SPLADE("naver/splade-cocondenser-ensembledistil")
    splade_model = DRES(splade_encoder)  # <- this is critical
    retriever = EvaluateRetrieval(splade_model, score_function="dot")  # "cos_sim" also valid
    results = retriever.retrieve(corpus, queries)
    scores = retriever.evaluate(qrels, results, k_values=[10, 100, 1209])
    print("splade")
    print(scores)

    # model_path = 
    # start_model = time.time()
    # beir_model = DRES(models.SentenceBERT(model_path), batch_size=32)
    # retriever = EvaluateRetrieval(beir_model, score_function="dot")

    # # Retrieval
    # start_retrieve = time.time()
    # results = retriever.retrieve(corpus, queries)
    # end_retrieve = time.time()

    # # Evaluation
    # start_eval = time.time()
    # scores = retriever.evaluate(qrels, results, k_values=[1209])
    # print(type(scores))  # Should show <class 'dict'>
    # print(scores)
    # end_eval = time.time()

    # total_time = time.time() - start_model
    # retrieval_time = end_retrieve - start_retrieve
    # evaluation_time = end_eval - start_eval

    # # Log results
    # print(f"Results for {model_name}:\n{scores}")
    # print(f"⏱ Retrieval time: {retrieval_time:.2f}s")
    # print(f"⏱ Evaluation time: {evaluation_time:.2f}s")
    # print(f"⏱ Total time: {total_time:.2f}s")

    # # Extract metrics
    # map_ = scores[1].values()
    # precision = scores[-1].values()
    # recall = scores[2].values()
