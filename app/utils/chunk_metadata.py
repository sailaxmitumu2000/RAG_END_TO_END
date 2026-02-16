from typing import List,Dict
def add_metadata_to_chunks(chunks:List[str],source:str)->List[Dict]:
    chunk_objects = []
    for idx,chunk in enumerate(chunks):
        chunk_objects.append({
            "chunk_id":idx,
            "text":chunk,
            "source": source


        })
   

    return chunk_objects