#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pandas import DataFrame
import re
from typing import List, Dict


class HttpParser(object):
    def __init__(self, raw_string: str):
        self.raw_string = raw_string
        # Load parsed structure data into pandas DataFrame
        self._http_request_df = pd.DataFrame(self.text_to_dict)

    @property
    def text_to_dict(self) -> List[Dict[str, str]]:
        """Parse unstructured raw string into structure data.

        :return: A list of fetched contents by parsing request log.
        """
        dict_array = []
        found_items = re.findall(
            "(?m)^((?:[\d]{1,3}\.){3}[\d]{1,3})[\S\ ]*?\[([\S\ "
            ']*?)\][\S\ ]*?"([A-Z]+)[\S\ ]*?(/(?=[\s]+)|/[\s]*[\S]+)[\S\ ]*?('
            'HTTP[\S]*?)"[\S\ ]*?([\d]{3}(?=\s|$))',
            self.raw_string,
        )
        for i in range(len(found_items)):
            try:
                dict = {
                    "remote_host": found_items[i][0],
                    "datetime": found_items[i][1],
                    "method": found_items[i][2],
                    "path": found_items[i][3],
                    "http_version": found_items[i][4],
                    "response_code": found_items[i][5],
                }
                dict_array.append(dict)
            except:
                print(f"Failed to extract contents from: {found_items[i]}")
        return dict_array

    @property
    def get_parsed_data(self):
        return self._http_request_df

    @staticmethod
    def select_topn_categories_by_freq(
        df: DataFrame, groupby_col: str, topn: int
    ) -> List[str]:
        """Extract top frequent categories based on their counts.

        :param df: input dataframe.
        :param groupby_col: string column to be grouped by.
        :param topn: number of top records.
        :return: a list of top frequent categories.
        """
        freq_count = df.groupby(groupby_col).size().reset_index(name="counts")
        # Sort by descending order of freqency count
        freq_count_desc = freq_count.sort_values(by="counts", ascending=False)
        # Select topn rows
        topn_records = freq_count_desc.head(topn)
        return topn_records[groupby_col].tolist()

    def get_distinct_ip_address(self) -> int:
        return self.get_parsed_data["remote_host"].nunique()

    def get_top3_visited_url(self) -> List[str]:
        return self.select_topn_categories_by_freq(df=self.get_parsed_data,
                                                   groupby_col="remote_host",
                                                   topn=3)

    def get_top3_active_ip_address(self) -> List[str]:
        success_request = self.get_parsed_data[
            self.get_parsed_data["response_code"] == "200"
        ]
        return self.select_topn_categories_by_freq(df=success_request,
                                                   groupby_col="remote_host",
                                                   topn=3)
