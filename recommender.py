import logging
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd
import config
import os
import errno

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("="*50)
logger.info("Starting recommender")
logger.info("="*50)
logger.info("\n")

torch.device("cpu")


logger.info("Start: Loading Dataset")
try:
    dataset_df = pd.read_csv(config.DATASET)
except OSError as e:
    if e.errno == errno.ENOENT:
        logger.info(f"Dataset \"{config.DATASET}\" couldn't be found. Exiting.")
        os._exit()
    else:
        raise
logger.info("End: Loading Dataset")

logger.info("Start: Loading embedder")
embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
logger.info("End: Loading embedder")


logger.info("Start: Creating product name embeddings")
try:
    pn_embeddings = torch.load("pn_cache.pkl")
except OSError as e:
    if e.errno == errno.ENOENT:
        logger.info(f"Name cache not found. Creating new ones.")
        pn_embeddings = embedder.encode(dataset_df.product_name.fillna(""), convert_to_tensor=True)
    else:
        raise
logger.info("End: Creating product name embeddings")


logger.info("Start: Creating product description embeddings")
try:
    pd_embeddings = torch.load("pd_cache.pkl")
except OSError as e:
    if e.errno == errno.ENOENT:
        logger.info(f"Description cache not found. Creating new ones.")
        pd_embeddings = embedder.encode(dataset_df.description.fillna(""), convert_to_tensor=True)
    else:
        raise
logger.info("End: Creating product description embeddings")

logger.info("="*50)
logger.info("Recommender ready to go!!")
logger.info("="*50)


def get_recommendation(uniq_id):
    """
    Make k (config) recommendations of items similar to the one past as param.

    params:
        - uniq_id: Id of the item.

    returns:
        - message: Json-like answer with the recommendations
        - status_code: status code of the answer
    """

    # Filtering
    query_df = dataset_df[dataset_df.uniq_id == uniq_id]
    if not len(query_df):
        return {"message": f"Unable to retrieve item {uniq_id}"}, 404

    p_name = query_df.iloc[0].product_name
    p_desc = query_df.iloc[0].description

    # Name query
    pn_query_embedding = embedder.encode(p_name, convert_to_tensor=True, show_progress_bar=False)
    pn_cos_scores = util.pytorch_cos_sim(pn_query_embedding, pn_embeddings)[0]
    pn_cos_scores = pn_cos_scores.cpu()
    
    # Description query
    pd_query_embedding = embedder.encode(p_desc, convert_to_tensor=True, show_progress_bar=False)
    pd_cos_scores = util.pytorch_cos_sim(pd_query_embedding, pd_embeddings)[0]
    pd_cos_scores = pd_cos_scores.cpu()
    
    # Weighted sum of scores
    total_cos_scores = config.NAME_VALUE * pn_cos_scores + config.DESCRIPTION_VALUE * pd_cos_scores
    
    # Extracting K top scores
    top_results = torch.topk(total_cos_scores, k=config.TOP_K + 1) 
    
    # Skipping first element (identity)
    indices = top_results.indices[1:].tolist()
    values = top_results.values[1:].tolist()
    
    return {"values": dataset_df.iloc[indices].to_dict(orient="records"), "scores": values}, 200


