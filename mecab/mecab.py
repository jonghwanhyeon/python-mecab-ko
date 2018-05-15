import _mecab

def _create_lattice(sentence):
    lattice = _mecab.Lattice()
    lattice.add_request_type(_mecab.MECAB_ALLOCATE_SENTENCE) # Essential
    lattice.set_sentence(sentence)

    return lattice

def _node_iter(node):
    current_node = node
    while current_node:
        is_sentinel = current_node.stat in { _mecab.MECAB_BOS_NODE, _mecab.MECAB_EOS_NODE }
        if not is_sentinel:
            yield current_node

        current_node = current_node.next


def _extract_tag(node):
    # Reference: https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
    # feature = <tag>,<semantic>,<has_jongseong>,<reading>,<type>,<first_tag>,<last_tag>,<representation>
    pos, _ = node.feature.split(',', 1)
    return pos

class MeCabError(Exception):
    pass

class MeCab: # APIs are inspried by KoNLPy
    def __init__(self):
        self.tagger = _mecab.Tagger('')

    def pos(self, sentence):
        lattice = _create_lattice(sentence)
        if not self.tagger.parse(lattice):
            raise MeCabError(self.tagger.what())

        return [
            (node.surface, _extract_tag(node))
            for node in _node_iter(lattice.bos_node())
        ]

    def morphs(self, sentence):
        return [ morpheme for morpheme, _ in self.pos(sentence) ]

    def nouns(self, sentence):
        return [
            morpheme for morpheme, pos in self.pos(sentence)
            if pos.startswith('N')
        ]
