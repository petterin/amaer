#!/usr/bin/env python

# AMAer ("Adjacency Matrix-er") turns a CSV list into an adjacency matrix.
# Usage instructions: python amaer.py --help
#
# https://github.com/petterin/amaer
#
# Copyright (c) 2013 Petteri Noponen (Licensed under the MIT License.)

import argparse
import csv
import os
import sys
import time

def main():
  # Initialize command line arguments
  arg_parser = init_argparse()
  args = arg_parser.parse_args()
  verbose = (args.outputFile.name != '<stdout>')

  # Read the input CSV and prepare data table
  csv_reader = csv.reader(args.inputFile, delimiter=';')
  data = table_from_reader(csv_reader, args.col_offset, args.row_offset)

  # Store unique values
  uniques = find_uniques_values(data);

  # Prepare the result matrix
  size = len(uniques)
  matrix = [ [-1]*size for _ in range(size) ] # table (size x size) full of neg values

  start = time.clock()
  if verbose: print '\nCalculating... (This may take a minute.)'

  # Count connections (Goes through the table several times. Quite inefficient, but works...)
  for i in range(size):
    for j in range(size):
      if i == j:
        matrix[i][j] = ''
      else:
        matrix[i][j] = count_connections(uniques[i], uniques[j], data)

  end = time.clock()
  if verbose: print 'Calculating done in %.2g seconds.' % (end-start)

  add_table_headers(uniques, matrix)

  # Output the result CSV table
  csv_writer = csv.writer(args.outputFile, delimiter=';')
  for row in matrix:
    csv_writer.writerow(row)

  if verbose: print '\nOutput matrix saved to %s.' % args.outputFile.name

def init_argparse():
  parser = argparse.ArgumentParser(description='AMAer ("Adjacency Matrix-er") turns an Excel CSV list of nodes into an adjacency matrix.')
  parser.add_argument('-c',
                      dest='col_offset',
                      metavar='X',
                      type=int,
                      default=1,
                      help="Ignore the first X columns (default: 1)")
  parser.add_argument('-r',
                      dest='row_offset',
                      metavar='Y',
                      type=int,
                      default=0,
                      help="Ignore the first Y rows (default: 0)")
  parser.add_argument('inputFile',
                      metavar='INPUT',
                      type=argparse.FileType('rU'),
                      help='Input CSV file path')
  parser.add_argument('outputFile',
                      metavar='OUTPUT',
                      nargs='?',
                      type=argparse.FileType('w'), # writable file
                      default=sys.stdout,
                      help='Output CSV file path (if omitted, uses stdout)')

  # Without arguments displays help and exits
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  return parser

def table_from_reader(reader, start_with_column=0, start_with_row=0):
  data = list()

  # Skip specified number of rows
  if start_with_row > 0:
    for _ in range(start_with_row):
      next(reader)

  for reader_row in reader:
    data_row = list()
    # Only start with column specified as parameter
    for reader_cell in reader_row[start_with_column::1]:

      # Trim cell values and use only the non-empty ones
      value = reader_cell.strip()
      if value:
        data_row.append(value)

    data.append(data_row)
  return data

def find_uniques_values(table):
  uniques = list()
  for row in table:
    for cell in row:
      if cell not in uniques:
        uniques.append(cell)
  return uniques

def count_connections(str1, str2, table):
  count = 0
  for row in table:
    if str1 in row and str2 in row:
      count += 1
  return count

def add_table_headers(header_list, table):
  if not len(table) == len(header_list):
    raise Exception("Header list's size doesn't match result matrix's size.")

  # Table's vertical headers
  for index in range(len(table)):
    header = header_list[index]
    table[index].insert(0, header)

  # Table's horizontal headers
  header_row = header_list[:] # copy from header_list
  header_row.insert(0, '') # add empty cell to the begin of the row
  table.insert(0, header_row)

if __name__ == '__main__':
  main()
