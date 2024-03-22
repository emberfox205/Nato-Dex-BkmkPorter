from os import path
import pandas as pd


def write_data(data: dict):
    append_df = pd.DataFrame(data)
    if path.isfile(".\\bookmark_db.csv"):
        prev_df = pd.read_csv("bookmark_db.csv", encoding="utf-8")
        combined_df = pd.concat(
            [prev_df, append_df], ignore_index=True
        ).drop_duplicates(subset="title",keep="last")
    else:
        combined_df = append_df
    combined_df.to_csv(path_or_buf="bookmark_db.csv", index=False)
    print(f"Database updated")


def retrieve_data():
    retrieve_df = pd.read_csv("bookmark_db.csv", encoding="utf-8", usecols=["title", "manganato", "mangadex"])
    titles = []
    titles = retrieve_df.to_dict()
    return titles

if __name__ == "__main__":
    retrieve_data()