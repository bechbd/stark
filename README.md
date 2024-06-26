
<h1 align="left">
    STaRK: Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases
</h1>

<div align="left">

[![](https://img.shields.io/badge/paper-pink?style=plastic&logo=GitBook)](https://arxiv.org/abs/2404.13207)
[![](https://img.shields.io/badge/-github-green?style=plastic&logo=github)](https://github.com/snap-stanford/stark) 
[![](https://img.shields.io/badge/-Linkedin-blue?style=plastic&logo=Linkedin)](https://www.linkedin.com/posts/leskovec_reduce-llm-hallucinations-with-rag-over-textual-activity-7190745116339302401-da4n?utm_source=share&utm_medium=member_desktop) 
[![](https://img.shields.io/badge/-Twitter-cyan?style=plastic&logo=Twitter)](https://twitter.com/ShirleyYXWu/status/1784970920383402433) 
[![](https://img.shields.io/badge/-Medium-black?style=plastic&logo=Medium)](https://medium.com/@multiplatform.ai/researchers-from-stanford-and-amazon-unveil-stark-a-comprehensive-benchmark-for-retrieving-b9ce4da55bba#:~:text=%2D%20STARK%20is%20a%20novel%20benchmark,textual%20descriptions%20with%20relational%20queries.) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>


**Interactive interface:** [STaRK SKB Explorer](https://huggingface.co/spaces/snap-stanford/SKB-Explorer)

## NEWS
- **[May 11th 2024]** We have upgraded our Amazon knowledge base and uploaded datasets to huggingface. Now you can download the SKB data from our [huggingface repo](https://huggingface.co/snap-stanford/STaRK-Dataset)!
- **[May 9th 2024]** We released [STaRK SKB Explorer](https://huggingface.co/spaces/snap-stanford/SKB-Explorer) on Hugging Face, an interactive interface for you to explore our knowledge bases! A demo video will be out soon.
- **[May 7th 2024]** We present STaRK in the [2024 Stanford Annual Affiliates Meeting](https://forum.stanford.edu/events/2024-annual-affiliates-meeting) and [2024 Stanford Data Science Conference](https://datascience.stanford.edu/2024-stanford-data-science-conference).
- **[May 5th 2024]** STaRK was reported on [Medium](https://medium.com/@multiplatform.ai/researchers-from-stanford-and-amazon-unveil-stark-a-comprehensive-benchmark-for-retrieving-b9ce4da55bba#:~:text=%2D%20STARK%20is%20a%20novel%20benchmark,textual%20descriptions%20with%20relational%20queries.) and [Marketpost](https://www.marktechpost.com/2024/05/01/researchers-from-stanford-and-amazon-developed-stark-a-large-scale-semi-structure-retrieval-ai-benchmark-on-textual-and-relational-knowledge-bases/) and [智源社区 BAAI](https://hub.baai.ac.cn/paper/6841fd6f-1eca-41c4-a432-5f2d845ac167). Thanks for writing about our work!
- **[Apr 21st 2024]** We release the STaRK benchmark.

## What is STaRK?
STaRK is a large-scale semi-structure retrieval benchmark on Textual and Relational Knowledge Bases. Given a user query, the task is to extract nodes from the knowledge base that are relevant to the query. 


<figure class="center-figure">
    <img src="media/overview.png" width="100%">
</figure>



## Why STaRK?
- **Novel Task**: Recently, large language models have demonstrated significant potential on information retrieval tasks. Nevertheless, it remains an open
question how effectively LLMs can handle the complex interplay between textual and relational
requirements in queries.

- **Large-scale and Diverse KBs**: We provide three large-scale knowledge bases across three areas, which are constructed from public sources.

    <figure class="center-figure"> <img src="media/kb.jpg" width="100%"></figure> 

- **Natural-sounding and Practical Queries**: The queries in our benchmark are crafted to incorporate rich relational information and complex textual properties, and closely mirror questions in real-life scenarios, e.g., with flexible query formats and possibly with extra contexts.

    <figure class="center-figure"> <img src="media/questions.jpg" width="100%"></figure> 


# Access benchmark data

## 1) Env Setup
Create a conda env with python 3.8 and install required packages in `requirements.txt`.
```bash
conda create -n stark python=3.8 
conda activate stark
pip install -r requirements.txt
```

## 2) Data loading 

### Demo: See [`load_dataset.ipynb`](https://github.com/snap-stanford/stark/blob/main/load_dataset.ipynb) for more
```python
from src.benchmarks.get_qa_dataset import get_qa_dataset
from src.benchmarks.get_semistruct import get_semistructured_data

dataset_name = 'amazon'

# Load the retrieval dataset
qa_dataset = get_qa_dataset(dataset_name)
idx_split = qa_dataset.get_idx_split()

# Load the knowledge base
kb = get_semistructured_data(dataset_name, download_processed=True)
```

### Data of the Retrieval Task

Question answer pairs for the retrieval task are locally included in `data/{dataset}/stark_qa`. We provided official split in `data/{dataset}/split`.


### Data of the Knowledge Bases

There are two ways to load the knowledge base data:
- (Recommended) Instant downloading: The knowledge base data of all three benchmark will be **automatically** downloaded and loaded when setting `download_processed=True`. 
- Process data from raw: We also provided all of our preprocessing code for transparency. Therefore, you can process the raw data from scratch via setting `download_processed=False`. In this case, STaRK-PrimeKG takes around 5 minutes to download and load the processed data. STaRK-Amazon and STaRK-MAG may takes around an hour to process from the raw data.

## 3) Evaluation on benchmark
- Our evaluation requires embed the node documents into `candidate_emb_dict.pt`, which is a dictionary `node_id -> torch.Tensor`. Query embeddings will be automatically generated if not available. You can either run the following the python script to download query embeddings and document embeddings generated by `text-embedding-ada-002`. (We provide them so you can run on our benchmark right away.)
    ```bash
    python download_emb.py --dataset amazon --emb_dir emb/
    ```
    
    Or you can run the following code to generate the query or document embeddings by yourself. E.g.,
    ```bash
    python generate_emb.py --dataset amazon --mode query --emb_dir emb/ --emb_model text-embedding-ada-002
    ```
    - `dataset`: one of `amazon`, `mag` or `primekg`.
    - `mode`: the content to embed, one of `query` or `doc` (node documents).
    - `emb_dir`: the directory to store embeddings.
    - `emb_model`: the LLM name to generate embeddings, such as `text-embedding-ada-002`, `text-embedding-3-large`.
    - See `generate_emb.py` for other arguments.

- Run the python script for evaluation. E.g.,
    ```bash
    python eval.py --dataset amazon --model VSS --emb_dir emb/ --output_dir output/ --emb_model text-embedding-ada-002 --save_pred
    ```

    ```bash
    python eval.py --dataset amazon --model LLMReranker --emb_dir emb/ --output_dir output/  --emb_model text-embedding-ada-002 --llm_model gpt-4-1106-preview --save_pred
    ```

    - `dataset`: the dataset to evaluate on, one of  `amazon`, `mag` or `primekg`.
    - `model`: the model to be evaluated, one of `VSS`, `MultiVSS`, `LLMReranker`. 
        - Please specify the name of embedding model with argument `--emb_model`.
        - If you are using `LLMReranker`, please specify API keys at `config/openai_api_key.txt` or `config/claude_api_key.txt` and the LLM name with argument `--llm_model`.
    - `emb_dir`: the directory to store embeddings.
    - `output_dir`: the directory to store evaluation outputs.


## Reference 

Please cite our paper if you use our benchmark or code in your work:
```
@article{wu24stark,
    title        = {STaRK: Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases},
    author       = {
        Shirley Wu and Shiyu Zhao and 
        Michihiro Yasunaga and Kexin Huang and 
        Kaidi Cao and Qian Huang and 
        Vassilis N. Ioannidis and Karthik Subbian and 
        James Zou and Jure Leskovec
    },
    eprinttype   = {arXiv},
    eprint       = {2404.13207},
  year           = {2024}
}
```
