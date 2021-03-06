# -*- coding: utf8 -*-

from constants import PREFIX_DECLARATION_TYPE_INTEGER
from constants import PREFIX_DECLARATION_TYPE_REAL
from constants import PREFIX_DECLARATION_TYPE_CHARACTER
from constants import PREFIX_DECLARATION_TYPE_LOGICAL
from constants import PREFIX_CONTEXT_TYPE_LOCAL
from constants import PREFIX_CONTEXT_TYPE_ARGUMENT
from constants import PREFIX_CONTEXT_TYPE_MODULE
from constants import PREFIX_CONTEXT_TYPE_OBJECT
from constants import PREFIX_CONTEXT_TYPE_GLOBAL
from extractors import *
from graph import Digraph
import re
import os

# ...
class Block(object):
    """

    """
    def __init__(self, keyword, \
                 TAG="", source=None, \
                 verbose=0, \
                 ancestor=None, \
                 color=None, \
                 prefix=None, \
                 prefix_lib=None, \
                 filename=None):

        self._keyword     = keyword
        self._TAG         = TAG
        self._text        = None
        self._source      = source
        self._variables   = None
        self._name        = TAG
        self._label       = None
        self._description = None
        self._verbose     = verbose
        self._dict_call   = {}
        self._dict_decl  = {}
        self._ancestor    = ancestor
        self._color       = color
        self._prefix      = prefix
        self._prefix_lib  = prefix_lib
        self._contains    = None
        self._is_valid    = False
        self._filename    = filename
        self._signature   = None

        if color is None:
            self.set_color()

        if prefix is None:
            self._prefix = ""

        if prefix_lib is None:
            self._prefix_lib = ""

        self._re_block     = extract_blocks(self._keyword, TAG)

    @property
    def keyword(self):
        return self._keyword

    @property
    def signature(self):
        return self._signature

    @property
    def filename(self):
        return self._filename

    @property
    def label(self):
        if self._label is None:
            self._label = self.name
        return self._label

    @property
    def prefix(self):
        return self._prefix

    @property
    def prefix_lib(self):
        return self._prefix_lib

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def text(self):
        return self._text

    @property
    def source(self):
        return self._source

    @property
    def variables(self):
        if self._variables is None:
            self.parse_variables()

        return self._variables

    @property
    def variables_arguments(self):
        return [var for var in self.variables if var.name in self._arguments]

    @property
    def variables_local(self):
        return [var for var in self.variables if var.name not in self._arguments]

    @property
    def verbose(self):
        return self._verbose

    @property
    def dict_call(self):
        return self._dict_call

    @property
    def dict_decl(self):
        return self._dict_decl

    @property
    def ancestor(self):
        return self._ancestor

    @property
    def color(self):
        if self._color is None:
            self.set_color()
        return self._color

    @property
    def contains(self):
        if self._contains is None:
            _re = extract_contains()
            self._contains = (len(_re.findall(self.text, re.I)) > 0)
        return self._contains

    @property
    def is_valid(self):
        return self._is_valid

    def set_source(self, source):
        self._source = source

    def get_code(self):
        if self.text is None:
            if self.source is not None:
                n = len(self._re_block.split(self.source))
                if n > 1:
                    self._is_valid = True

                if self.is_valid:
                    try:
                        self._text = self._re_block.findall(self.source, re.I)[0]
                    except:
                        print ("Cannot parse the source code")
                        raise()
            else:
                print ("you must provide the source code before parsing")
                raise()

        return self.text

    def get_signature(self):
        if self.text is None:
            self.get_code()

        try:
            t = get_signature_from_text(self.text)
        except:
            t = None

        self._signature = t

        return t

    def get_arguments(self):
        if self.text is None:
            self.get_code()
        _text = self.get_signature()
        if self.verbose > 0:
            print (">>> signature:", _text)
        self._arguments = get_arguments_from_text(_text)
        return self._arguments

    def get_decl_call(self):
        """
        """
        self._dict_decl, self._dict_call = get_declarations_calls(self.text)

    def parse_variables(self, constructor_variable=None):
        if constructor_variable is None:
            print ("parse_variables: a constructor must be provided. Received None")
            raise()
        self._variables = []
        for keyword in list_keywords_decs:
            _re = dict_keywords_re[keyword]
            _vars_name = _re.findall(self.text, re.I)
            for _vars in _vars_name:
                for var_name in _vars.split(','):
                    var = constructor_variable(name=var_name.strip(), dtype=keyword)
                    self._variables.append(var)

    def replace_variable(self, var, inline=True):
        """
        """
        print ("replace_variable: not yet implemented for the generic class")
        raise()

    def update_source(self):
        print ("update_source: not yet implemented for the generic class")
        raise()

    def update_variables(self):
        for var in self.variables:
            var.construct_prefix()
        for var in self.variables:
            self.replace_variable(var)

    def set_color(self):
        if self.keyword == "module":
            self._color = "red"
        if self.keyword == "subroutine":
            self._color = "blue"
        if self.keyword == "function":
            self._color = "green"

    def update_label(self, root):
        if not self.contains:
            return
        else:
            for key, values in self.dict_decl.items():
                keyword = key

                for name in values:
                    other = root.get_block_by_filename_name(self.filename, name)
                    if other is not None:
                        try:
#                            label_s = self.label
                            label_s = self.name
                        except:
                            label_s = ""

                        try:
                            label_o = other.label
                        except:
                            label_o = ""

                        other._label = label_s + " % "+ label_o

    def update_graph_decl(self, root):
        if not self.contains:
            return

        # ... add current block if it is a subroutine or a function
        graph = root.graph_decl
        subgraph   = Digraph(name=self.name)

        attributs = {}
#        attributs["constraint"] = "true"
        attributs["constraint"] = "false"
        attributs["style"]      = "solid"
        attributs["label"]      = self.label

        # ... add edges / nodes for functions/subroutines declarations
        for key, values in self.dict_decl.items():
            keyword = key

            for name in values:
                other = root.get_block_by_filename_name(self.filename, name)

                attributs = {}
#                attributs["constraint"] = "true"
                attributs["style"]      = "dashed"

                if other is not None:
                    subgraph.edge(self, other, attributs=attributs)
        # ...

        # ... update root graph with subgraph
        graph.add_subgraph(subgraph)
        # ...

    def update_graph_call(self, root):
        # ... add current block if it is a subroutine or a function
        graph = root.graph_call

        dict_call = self.dict_call
        no_call = False
        if self.keyword == "module":
            condition_sub = True
            try:
                condition_sub = (len(self.dict_call["subroutine"]) == 0)
            except:
                pass

            condition_fun = True
            try:
                condition_fun = (len(self.dict_call["function"]) == 0)
            except:
                pass

            no_call = condition_sub and condition_fun

            if no_call:
                dict_call = self.dict_decl

        attributs = {}
#        attributs["constraint"] = "true"
        attributs["constraint"] = "false"
        attributs["style"]      = "solid"
        attributs["label"]      = self.label

        # ... add edges / nodes for functions/subroutines calls
        for key, values in dict_call.items():
            keyword = key

            for name in values:
                if root.dict_attribut['internal_graph_call']:
                    other = root.get_block_by_filename_name(self.filename, name)
                    others = []
                    if other is not None:
                        others = [other]
                else:
                    others = root.get_blocks_by_name(name)

                for other in others:
                    attributs = {}
#                    attributs["constraint"] = "true"
                    attributs["style"]      = "solid"
                    if no_call and (self.keyword == "module"):
                        attributs["style"]      = "dashed"

                    graph.edge(self, other, attributs=attributs)
        # ...
# ...

# ...
class SubroutineBlock(Block):
    def __init__(self, TAG="", source=None):
        Block.__init__(self, "subroutine", TAG=TAG, source=source)
# ...

# ...
class FunctionBlock(Block):
    def __init__(self, TAG="", source=None):
        Block.__init__(self, "function", TAG=TAG, source=source)
# ...

# ...
class ModuleBlock(Block):
    def __init__(self, TAG="", source=None):
        Block.__init__(self, "module", TAG=TAG, source=source)
# ...

