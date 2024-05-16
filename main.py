from src.benchmarks.get_qa_dataset import get_qa_dataset
from src.benchmarks.get_semistruct import get_semistructured_data

dataset_name = 'primekg'

qa_dataset = get_qa_dataset(dataset_name)
kb = get_semistructured_data(dataset_name, download_processed=True)


# You can see part of the knowledge base schema here
# doc_info = kb.get_doc_info(0)
# # chunk_info = kb.get_chunk_info(0, 'description')
# rel_info = kb.get_rel_info(0)

print(dir(kb))
print(kb.get_tuples()) # This is really a get_ontology

# print(kb.edge_index())

# print('******** DOC INFO ********')
# print(doc_info)

# # print('******** CHUNK INFO (description) ********')
# # print(chunk_info)

# print('******** REL INFO ********')
# print(rel_info)

# import pickle
# import json

# def safe_serialize(obj):
#   default = lambda o: str(o)
#   return json.dumps(obj, default=default, indent=2)

# with open('./data/amazon/processed/node_info.pkl', 'rb') as f:
#     data = pickle.load(f)

# print(safe_serialize(data[0]))