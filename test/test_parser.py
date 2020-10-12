#!/usr/bin/env python
# -*- coding: utf-8 -*-


from http_parse import HttpParser


def tests_parser(http_request_log_sample):
    http_parser = HttpParser(http_request_log_sample)

    assert http_parser.get_distinct_ip_address() == 11
    assert http_parser.get_top3_active_ip_address() == [
        "168.41.191.40",
        "177.71.128.21",
        "50.112.00.11",
    ]
    assert http_parser.get_top3_visited_url() == [
        "168.41.191.40",
        "177.71.128.21",
        "50.112.00.11",
    ]
