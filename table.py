# coding=utf-8

# Copyright (c) 2012, Eser Aygün
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#   disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy
import csv

__version__ = "0.0.4"

class Table(object):
    """
    Provides a two-dimensional matrix with named rows and columns.
    """

    def __init__(self, rowNames, columnNames, matrix=None):
        """
        Creates a table with given row names and column names.
        Both row names and column names should be unique.
        The optional matrix argument can be used to initialize the matrix.
        If provided, the size of the matrix argument should be equal to len(rowNames) * len(columnNames).
        """
        self.rowNames = list(rowNames)
        self.columnNames = list(columnNames)
        self.rowIndices = dict([(n, i) for i, n in enumerate(self.rowNames)])
        self.columnIndices = dict([(n, i) for i, n in enumerate(self.columnNames)])
        self.matrix = numpy.zeros((len(rowNames), len(columnNames)))
        if matrix is not None:
            self.matrix[:] = matrix

    def cell(self, rowName, columnName):
        """
        Returns the value of the cell on the given row and column.
        """
        return self.matrix[self.rowIndices[rowName], self.columnIndices[columnName]]

    def row(self, rowName):
        """
        Returns the given row as an array.
        """
        return self.matrix[self.rowIndices[rowName], :]

    def column(self, columnName):
        """
        Returns the given column as an array.
        """
        return self.matrix[:, self.columnIndices[columnName]]

    def __getRowIndex(self, rowName):
        if rowName is None:
            return None
        else:
            return self.rowIndices[rowName]

    def __getColumnIndex(self, columnName):
        if columnName is None:
            return None
        else:
            return self.columnIndices[columnName]

    def __getRowSlice(self, rowName):
        if rowName is None:
            return None
        elif isinstance(rowName, slice):
            return slice(
                self.__getRowIndex(rowName.start),
                self.__getRowIndex(rowName.stop),
                rowName.step
            )
        else:
            return self.__getRowIndex(rowName)

    def __getColumnSlice(self, columnName):
        if columnName is None:
            return None
        elif isinstance(columnName, slice):
            return slice(
                self.__getColumnIndex(columnName.start),
                self.__getColumnIndex(columnName.stop),
                columnName.step
            )
        else:
            return self.__getColumnIndex(columnName)

    def __getitem__(self, item):
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("2-tuple expected")

        return self.matrix[self.__getRowSlice(item[0]), self.__getColumnSlice(item[1])]

    def __setitem__(self, item, value):
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("2-tuple expected")

        self.matrix[self.__getRowSlice(item[0]), self.__getColumnSlice(item[1])] = value

    def __repr__(self):
        return "Table(%s)" % self.matrix

    def __str__(self):
        return str(self.matrix)

    def __unicode__(self):
        return unicode(self.matrix)

def readTableFromDelimited(f, separator="\t"):
    """
    Reads a table object from given plain delimited file.
    """
    rowNames = []
    columnNames = []
    matrix = []

    first = True
    for line in f.readlines():
        line = line.rstrip()
        if len(line) == 0:
            continue

        row = line.split(separator)
        if first:
            columnNames = row[1:]
            first = False
        else:
            rowNames.append(row[0])
            matrix.append([float(c) for c in row[1:]])

    return Table(rowNames, columnNames, matrix)

def readTableFromCSV(f, dialect="excel"):
    """
    Reads a table object from given CSV file.
    """
    rowNames = []
    columnNames = []
    matrix = []

    first = True
    for row in csv.reader(f, dialect):
        if first:
            columnNames = row[1:]
            first = False
        else:
            rowNames.append(row[0])
            matrix.append([float(c) for c in row[1:]])

    return Table(rowNames, columnNames, matrix)
