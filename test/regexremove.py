import re
from traitlets import List, Unicode
from nbconvert.preprocessors import Preprocessor

class MyRegexRemovePreprocessor(Preprocessor):
    all = List(Unicode(), default_value=[]).tag(config=True)
    input = List(Unicode(), default_value=[]).tag(config=True)
    output = List(Unicode(), default_value=[]).tag(config=True)

    def compile(self, patterns):
        if not patterns:
            return None
        return re.compile('|'.join('(?:%s)' % pattern
                              for pattern in patterns), re.M)

    def check_conditions(self, cell, pat):
        if not pat:
            return False
        return pat.search(cell.source)

    def cell_modify(self, cell):
        in_match = self.check_conditions(cell, self.input_pat)
        out_match = self.check_conditions(cell, self.output_pat)
        all_match = self.check_conditions(cell, self.all_pat)

        print(not all_match, not in_match, not out_match)
        if all_match or (in_match and out_match):
            return None
        if in_match:
            cell.transient = {'remove_source': True}
        if out_match:
            cell.outputs = []
        return cell

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply to each notebook. See base.py for details.
        """
        self.all_pat = self.compile(self.all)
        self.input_pat = self.compile(self.input)
        self.output_pat = self.compile(self.output)
        
        print(self.all, self.input, self.output)
        nb.cells = [self.cell_modify(cell) for cell in nb.cells]
        nb.cells = [cell for cell in nb.cells if cell]
 
        return nb, resources
