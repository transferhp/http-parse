#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope="module")
def http_request_log_sample():
    with open("data/programming-task-example-data.log", "r") as f:
        test_input = f.read()
    return test_input
