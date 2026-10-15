"""Degree-level tagger.

Many postings name the degree they're for right in the title ("Software
Engineering PhD Intern", "2027 Summer Intern, BS/MS, ...", "Intern,
Bachelor's"). detect_degrees() pulls those out so the site can filter on them.

Returns a list drawn from ("BS", "MS", "PhD"), in that order, or [] when the
title doesn't say — which usually means the role is open to any level.

"Graduate" (as in Intel's "Intern, Graduate" vs "Intern, Bachelor's") means a
graduate student, so it maps to both MS and PhD; "Undergraduate" maps to BS.
"""
import re


def _rx(pattern):
    return re.compile(pattern, re.IGNORECASE)


_GRAD = r"(?<!under)\bgrad(uate)?\b|\bpostgrad"

DEGREE_PATTERNS = [
    ("BS", _rx(r"\bbachelor|\bb\.?sc?\b|\bb\.s\.|\bb\.?eng\b|\bundergrad")),
    ("MS", _rx(r"\bmaster(?!\s*data)|\bm\.?sc?\b|\bm\.s\.|\bm\.?eng\b|" + _GRAD)),
    ("PhD", _rx(r"\bph\.?\s?d\b|\bdoctor|\bdoktor|" + _GRAD)),
]


def detect_degrees(title):
    return [name for name, pattern in DEGREE_PATTERNS if pattern.search(title or "")]
