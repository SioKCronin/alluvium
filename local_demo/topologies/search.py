# https://medium.com/@Sugeesh/connecting-python-bolt-for-apache-storm-topology-af6c2e3f2200

from streamparse import Grouping, Topology

from bolts.search import SearchBolt
from spouts.docs import DocSpout

class Search(Topology):
    docs = DocSpout.spec()
    search = SearchBolt.spec()


