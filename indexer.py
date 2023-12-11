import json
import pandas as pd
import pyterrier as pt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class CustomIndexer:
    def __init__(self):
        if not pt.started():
            pt.init()

        self.index_path = "./money-index"
        self.data_path = "./data/data.csv"
        self.indexer = pt.DFIndexer(
            index_path=self.index_path, overwrite=True, verbose=True
        )
        self.indexref = None

    def create_custom_index(self):
        """Create and populate index."""

        print("Bulk Indexing Data:")

        Numismaticatrionfale_df = pd.read_json("./data/numismatica.json")
        delcampe_df = pd.read_json("./data/delcampe.json")
        cavaliere_df = pd.read_json("./data/cavalierenumismatica.json")

        data_df = pd.concat(
            [Numismaticatrionfale_df, delcampe_df, cavaliere_df], ignore_index=True
        )

        data_df["docno"] = [str(i + 1) for i in range(len(data_df))]

        self.indexref = self.indexer.index(
            data_df["Title"],
            data_df["docno"],
        )

        data_df.to_csv(self.data_path)

    def get_custom_index_ref(self):
        return pt.IndexFactory.of(f"{self.index_path}/data.properties")

    def custom_document_search(self, q=None):
        query = [[str(i + 1), e] for i, e in enumerate(q.split(" "))]
        print(query)

        topics = pd.DataFrame(query, columns=["qid", "query"])

        self.indexref = self.indexref or self.get_custom_index_ref()

        search_result_df = pt.BatchRetrieve(self.indexref).transform(topics)
        search_result_df["docno"] = search_result_df["docno"].astype(int)

        data_df = pd.read_csv(self.data_path)

        result_df = data_df[data_df["docno"].isin(search_result_df["docno"])]

        result_df = result_df[["Title", "Price", "Image"]]

        return json.loads(result_df.to_json(orient="records"))

    def get_custom_index_ref(self):
        return pt.IndexFactory.of(f"{self.index_path}/data.properties")

    def get_similar_coins(self, q=None):
        query = q
        input_csv = pd.read_csv(self.data_path)

        documents = input_csv["Title"].values.tolist()

        documents = [str(doc) for doc in documents]

        vectorizer = TfidfVectorizer(
            min_df=0.005, lowercase=True, max_df=0.8, max_features=1000
        )

        matrix_df = vectorizer.fit_transform(documents).toarray()

        query_df = vectorizer.transform([query]).toarray()

        diz = {}

        for i in range(matrix_df.shape[0]):
            diz[i] = cosine_similarity([query_df.reshape(-1), matrix_df[i, :]])[0][1]

        idx_sort = sorted(diz.items(), key=lambda x: x[1], reverse=True)

        sorted_dict = dict(idx_sort)

        sorted_dict_json = json.dumps(sorted_dict)

        with open("./data/sorted_coins.json", "w") as json_file:
            json.dump(sorted_dict_json, json_file)

        return sorted_dict_json


if __name__ == "__main__":
    custom_indexer = CustomIndexer()
    custom_indexer.create_custom_index()