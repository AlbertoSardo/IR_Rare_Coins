import json
import pandas as pd
import pyterrier as pt


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


if __name__ == "__main__":
    custom_indexer = CustomIndexer()
    custom_indexer.create_custom_index()

    # 1) fare spiders (script che tirino giù dati (nome, data emissione, descrizione, valore) da sito con scrapy
    # 2) modificare indexer
    # 3) creare sito dove viene mostraro il json dell'indexer
