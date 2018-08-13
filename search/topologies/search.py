"""
Search topology
"""

from streamparse import Grouping, Topology
from spouts.docs import DocsSpout
from bolts.search import SearchBolt


class Search(Topology):
    docs_spout = DocsSpout.spec()
    search_bolt = SearchBolt.spec(inputs=[docs_spout])
