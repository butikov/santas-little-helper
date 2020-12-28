import json
import re
import pandas as pd
from collections import defaultdict


def from_reddit_file(file_name: str) -> pd.DataFrame:
    good, bad = defaultdict(list), list()
    with open(file_name, "r") as comments:
        for line in comments.readlines():
            comment = json.loads(line)
            score = comment["score"]
            if score < 0:
                bad.append(comment["body"])
            elif score > 0:
                good[score].append(comment["body"])
        data_cleaned = []
        target = []
        good = sorted(good.items(), reverse=True)
        for comment in bad:
            words = re.findall(r"\w+", comment.lower())
            if len(words) > 0:
                data_cleaned.append(' '.join(words))
                target.append(0)
        cnt = len(data_cleaned)
        good_cnt = 0
        i = 0
        while good_cnt < cnt:
            good_cnt += len(good[i][1])
            for comment in good[i][1]:
                words = re.findall(r"\w+", comment.lower())
                if len(words) > 0:
                    data_cleaned.append(' '.join(words))
                    target.append(1)
            i += 1

        df = pd.DataFrame()
        df["comment"] = data_cleaned
        df["is_good"] = target
    return df
