"""
Module containing a preprocessor that removes cells if they match
one or more regular expression.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re
from traitlets import List, Unicode
from nbconvert.preprocessors import Preprocessor

INPUT = 1
OUTPUT = 2
BOTH = 3

class MyRegexRemovePreprocessor(Preprocessor):
    all = List(Unicode(), default_value=[]).tag(config=True)
    input = List(Unicode(), default_value=[]).tag(config=True)
    output = List(Unicode(), default_value=[]).tag(config=True)
    patterns = None
    mode = 0

    def check_conditions(self, cell):
        """
        Checks that a cell matches the pattern.

        Returns: Boolean.
        True means cell should *not* be removed.
        """

        # Compile all the patterns into one: each pattern is first wrapped
        # by a non-capturing group to ensure the correct order of precedence
        # and the patterns are joined with a logical or
        pattern = re.compile('|'.join('(?:%s)' % pattern
                             for pattern in self.patterns))

        # Filter out cells that meet the pattern and have no outputs
        return not pattern.match(cell.source)

    def cell_modify(self, cell):
        if not self.check_conditions(cell):
            if self.mode == BOTH:
                return None
            if self.mode == INPUT:
                cell.transient = {'remove_source': True}
            if self.mode == OUTPUT:
                cell.outputs = []
        return cell

    def preprocess(self, nb, resources):
        """
        Preprocessing to apply to each notebook. See base.py for details.
        """
        if self.all:
            self.patterns = self.all
            self.mode = BOTH
        if self.input:
            self.patterns = self.input
            self.mode = INPUT
        if self.output:
            self.patterns = self.output
            self.mode = OUTPUT
        
        # Skip preprocessing if the list of patterns is empty
        if not self.patterns:
            return nb, resources

        print(self.mode, self.patterns)

        # Filter out cells that meet the conditions
        # nb.cells = [cell for cell in nb.cells if self.check_conditions(cell)]
        nb.cells = [self.cell_modify(cell) for cell in nb.cells]
        nb.cells = [cell for cell in nb.cells if cell]

 
        return nb, resources
