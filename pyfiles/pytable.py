#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Table():

    def __init__(self):
        self.matrix = []
        self.colnames = []
        self.colsizes = []
        self.extra_padding = 1
        self.d_style = {}
        self.set_theme_fancy()

    def shorten_string(self, val, length):
        return val[:length//2-1] + "..." + val[-length//2+2:]
    def fmt_string(self, val, length, fill_char=" ", justify="c", bold=False, offcolor=False):
        ret = ""
        val = str(val)
        if len(val) > length: val = self.shorten_string(val, length)
        if justify == "l": 
            ret = " "+val.ljust(length-1, fill_char)
        elif justify == "r": ret = val.rjust(length, fill_char)
        elif justify == "c":
            nl = (length-len(val))//2
            nr = (length-len(val))-(length-len(val))//2
            ret = fill_char*nl + val + fill_char*nr
        if bold:
            ret = '\033[1m' + ret + '\033[0m'
        if offcolor:
            ret = '\033[2m' + ret + '\033[0m'
        return ret

    def set_theme_fancy(self):
        self.d_style["INNER_HORIZONTAL"] = '\033(0\x71\033(B'
        self.d_style["INNER_INTERSECT"] = '\033(0\x6e\033(B'
        self.d_style["INNER_VERTICAL"] = '\033(0\x78\033(B'
        self.d_style["OUTER_LEFT_INTERSECT"] = '\033(0\x74\033(B'
        self.d_style["OUTER_LEFT_VERTICAL"] = self.d_style["INNER_VERTICAL"]
        self.d_style["OUTER_RIGHT_INTERSECT"] = '\033(0\x75\033(B'
        self.d_style["OUTER_RIGHT_VERTICAL"] = self.d_style["INNER_VERTICAL"]
        self.d_style["OUTER_BOTTOM_HORIZONTAL"] = self.d_style["INNER_HORIZONTAL"]
        self.d_style["OUTER_BOTTOM_INTERSECT"] = '\033(0\x76\033(B'
        self.d_style["OUTER_BOTTOM_LEFT"] = '\033(0\x6d\033(B'
        self.d_style["OUTER_BOTTOM_RIGHT"] = '\033(0\x6a\033(B'
        self.d_style["OUTER_TOP_HORIZONTAL"] = self.d_style["INNER_HORIZONTAL"]
        self.d_style["OUTER_TOP_INTERSECT"] = '\033(0\x77\033(B'
        self.d_style["OUTER_TOP_LEFT"] = '\033(0\x6c\033(B'
        self.d_style["OUTER_TOP_RIGHT"] = '\033(0\x6b\033(B'

    def set_theme_basic(self):
        self.d_style["INNER_HORIZONTAL"] = '-'
        self.d_style["INNER_INTERSECT"] = '+'
        self.d_style["INNER_VERTICAL"] = '|'
        self.d_style["OUTER_LEFT_INTERSECT"] = '|'
        self.d_style["OUTER_LEFT_VERTICAL"] = '|'
        self.d_style["OUTER_RIGHT_INTERSECT"] = '+'
        self.d_style["OUTER_RIGHT_VERTICAL"] = '|'
        self.d_style["OUTER_BOTTOM_HORIZONTAL"] = '-'
        self.d_style["OUTER_BOTTOM_INTERSECT"] = '+'
        self.d_style["OUTER_BOTTOM_LEFT"] = '+'
        self.d_style["OUTER_BOTTOM_RIGHT"] = '+'
        self.d_style["OUTER_TOP_HORIZONTAL"] = '-'
        self.d_style["OUTER_TOP_INTERSECT"] = '+'
        self.d_style["OUTER_TOP_LEFT"] = '+'
        self.d_style["OUTER_TOP_RIGHT"] = '+'

    def set_theme_latex(self):
        self.d_style["INNER_HORIZONTAL"] = ''
        self.d_style["INNER_INTERSECT"] = ''
        self.d_style["INNER_VERTICAL"] = ' & '
        self.d_style["OUTER_LEFT_INTERSECT"] = ''
        self.d_style["OUTER_LEFT_VERTICAL"] = ''
        self.d_style["OUTER_RIGHT_INTERSECT"] = ''
        self.d_style["OUTER_RIGHT_VERTICAL"] = '\\\\ \\hline'
        self.d_style["OUTER_BOTTOM_HORIZONTAL"] = ''
        self.d_style["OUTER_BOTTOM_INTERSECT"] = ''
        self.d_style["OUTER_BOTTOM_LEFT"] = ''
        self.d_style["OUTER_BOTTOM_RIGHT"] = ''
        self.d_style["OUTER_TOP_HORIZONTAL"] = ''
        self.d_style["OUTER_TOP_INTERSECT"] = ''
        self.d_style["OUTER_TOP_LEFT"] = ''
        self.d_style["OUTER_TOP_RIGHT"] = ''


    def set_column_names(self, cnames):
        self.colnames = cnames
        self.update()

    def add_row(self, row):
        self.matrix.append(row)

    def update(self):
        if not self.colnames:
            if self.matrix:
                self.colnames = range(1,len(self.matrix[0])+1)
        if self.matrix:
            for ic, cname in enumerate(self.colnames):
                self.colsizes.append( max(
                    max([len(str(r[ic])) for r in self.matrix])+2,
                    len(str(cname))+2
                    ) )

    def sort(self, column=None, descending=True):
        self.update()
        icol = self.colnames.index(column)
        self.matrix = sorted(self.matrix, key=lambda x: x[icol], reverse=descending)

    def print_table(self, **kwargs):
        print "".join(self.get_table_string(**kwargs))

    def get_table_string(self, bold_title=True, show_row_separators=False, show_alternating=False):
        self.update()
        nrows = len(self.matrix) + 1
        for irow,row in enumerate([self.colnames]+self.matrix):
            if irow == 0:
            # line at very top
                yield self.d_style["OUTER_TOP_LEFT"]
                for icol,col in enumerate(row):
                    yield self.d_style["OUTER_TOP_HORIZONTAL"]*(self.colsizes[icol]+self.extra_padding)
                    if icol != len(row)-1: yield self.d_style["OUTER_TOP_INTERSECT"]
                yield self.d_style["OUTER_TOP_RIGHT"]+"\n"
            # lines separating columns
            yield self.d_style["OUTER_LEFT_VERTICAL"]
            oc = False if not show_alternating else (irow%2==1 )
            bold = False if not bold_title else (irow==0)
            for icol,col in enumerate(row):
                j = "l" if icol == 0 else "c"
                yield self.fmt_string(col, self.colsizes[icol]+self.extra_padding, justify=j, bold=bold,offcolor=oc)
                if icol != len(row)-1: yield self.d_style["INNER_VERTICAL"]
            yield self.d_style["OUTER_RIGHT_VERTICAL"]+"\n"
            # lines separating rows
            if (show_row_separators and (irow < nrows-1)) or (irow == 0):
                yield self.d_style["OUTER_LEFT_INTERSECT"]
                for icol,col in enumerate(row):
                    yield self.d_style["INNER_HORIZONTAL"]*(self.colsizes[icol]+self.extra_padding)
                    if icol != len(row)-1: yield self.d_style["INNER_INTERSECT"]
                yield self.d_style["OUTER_RIGHT_INTERSECT"]+"\n"
            # line at very bottom
            if irow == nrows-1:
                yield self.d_style["OUTER_BOTTOM_LEFT"]
                for icol,col in enumerate(row):
                    yield self.d_style["OUTER_BOTTOM_HORIZONTAL"]*(self.colsizes[icol]+self.extra_padding)
                    if icol != len(row)-1: yield self.d_style["OUTER_BOTTOM_INTERSECT"]
                yield self.d_style["OUTER_BOTTOM_RIGHT"]+"\n"


if __name__ == "__main__":

    if(sys.stdin.isatty()):

        tab = Table()
        # tab.set_theme_basic()
        # tab.set_theme_latex()
        tab.set_column_names(["name", "age", "blahhhhhh"])
        for row in [
                ["Alice", 42, 4293.9923344],
                ["Bob", 1, 0.9999999],
                ["Jim", -3, 4293],
                ["Pam", 4.2, 0.9923344],
                ["David", 4.2, 0.99999923344],
                ["John", 4.2, 0.9923344],
                ["John", 4.2, 0.9923344],
                ["John", 4.2, 0.9923344],
                ]:
            tab.add_row(row)
        tab.sort(column="age", descending=True)
        tab.print_table(show_row_separators=False,show_alternating=True)

    else:

        first_row_colnames = True
        rows = []
        maxcols = -1
        for row in sys.stdin: 
            row = row.strip()
            rows.append(row)
            maxcols = max(maxcols,len(row.split()))
        rows = [r for r in rows if len(r.split()) == maxcols]
        tab = Table()
        for irow,row in enumerate(rows):
            parts = row.split()
            if first_row_colnames:
                if irow == 0: tab.set_column_names(parts)
                else: tab.add_row(parts)
            else:
                tab.add_row(parts)
        tab.print_table(show_row_separators=False,show_alternating=True)
