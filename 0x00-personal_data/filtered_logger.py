#!/usr/bin/env python3
"""
PII filter function implementation
"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ PII filter method """
    for obs in fields:
        message = re.sub(r'{}=.*?{}'.format(obs, separator),
                         '{}={}{}'.format(obs, redaction, separator), message)
    return message
