"""Software-engineering role classifier.

The tracker only lists engineering internships: AI/ML, Data, Mobile, Frontend,
Backend/Infra, general Software, QA, Security. categorize() returns the
category for a title, or None for out-of-scope roles (sales, HR, finance,
legal, marketing, hardware ops, ...) which are then dropped.

Order matters: first matching category wins, so the more specific ones
(Security, QA, Mobile, ...) come before the catch-alls.
"""
import re


def _rx(pattern):
    return re.compile(pattern, re.IGNORECASE)


# Unambiguous engineering-role signals. When one of these is in the title the
# exclusions below are skipped — they often appear as team names appended to
# real SWE roles ("Software Dev Engineer Intern, Manufacturing&Ops",
# "Applied Scientist Intern, University Talent Acquisition").
HARD_INCLUDE_RE = _rx(
    r"software|machine learning|deep learning|computer vision|"
    r"applied scien|research scien|data scien|data engineer|data analy|"
    r"full[- ]?stack|front[- ]?end|back[- ]?end|\bios\b|android|\bsdet\b|"
    r"security engineer|cybersecurity|\bnlp\b|\bllm\b|compiler|kernel")

# Roles that pattern-match an engineering keyword but aren't software work.
EXCLUDE_RE = _rx(
    r"technician|data cent(er|re)|solutions? engineer|sales|account manag|"
    r"customer success|field engineer|facilities|construction|mechanical|"
    r"civil engineer|electrical engineer|manufacturing|supply chain|"
    r"process engineer|industrial engineer|recruiter|talent|marketing")

CATEGORIES = [
    ("Security", _rx(r"security|cyber|infosec|appsec|threat|penetration|red team|"
                     r"vulnerab|crypto(graph|log)")),
    ("QA", _rx(r"\bqa\b|quality (assurance|engineer)|test(ing)? engineer|"
               r"software test|\bsdet\b|validation")),
    ("AI/ML", _rx(r"\bai\b|artificial intelligence|machine learning|\bml\b|"
                  r"deep learning|computer vision|\bnlp\b|\bllm\b|gen ?ai|"
                  r"generative|applied scien|research scien|research engineer|"
                  r"student researcher|robotics|autonom|perception|recommender")),
    ("Data", _rx(r"\bdata\b|analytics|business intelligence")),
    ("Mobile", _rx(r"mobile|\bios\b|android|flutter|react native")),
    ("Frontend", _rx(r"front[- ]?end|web develop|web engineer|\bui engineer\b|"
                     r"javascript|typescript|\breact\b")),
    ("Backend/Infra", _rx(r"back[- ]?end|distributed|infrastructure|platform|"
                          r"cloud|devops|site reliability|\bsre\b|\bapi\b|"
                          r"database|storage|network|linux|kernel|embedded|"
                          r"firmware|compiler|operating system|virtualization")),
    ("Software", _rx(r"software|\bswe\b|developer|full[- ]?stack|programmer|"
                     r"application develop|computer science|solution develop|"
                     r"game develop|\bdev\b|\bjava\b|\bpython\b|c\+\+|"
                     r"\bgolang\b|\brust\b")),
]


def categorize(title):
    if not HARD_INCLUDE_RE.search(title) and EXCLUDE_RE.search(title):
        return None
    for name, pattern in CATEGORIES:
        if pattern.search(title):
            return name
    return None
