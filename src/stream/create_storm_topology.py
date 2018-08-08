# https://medium.com/@Sugeesh/connecting-python-bolt-for-apache-storm-topology-af6c2e3f2200

import storm

class SplitBoltPython(storm.BasicBolt):

    def initialize(self, conf, context):
        self._conf = conf;
        self._context = context;

    def process(self, tuple):
        word = tuple.values[0]
               # do your processing here
        storm.emit([word])  # return list object

SplitBoltPython().run()
