"""
Search topology
"""

from streamparse import Grouping, Topology
from src.spouts.docs import DocsSpout
from src.bolts.search import SearchBolt


class Search(Topology):
    docs_spout = DocsSpout.spec()
    search_bolt = SearchBolt.spec(inputs=[docs_spout])
