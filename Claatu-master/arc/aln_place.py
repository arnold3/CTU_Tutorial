#!/usr/bin/python

# Claatu::aln_place -Alignment placer 
#Copyright (C) 2015  Christopher A. Gaulke 
#author contact: gaulkec@science.oregonstate.edu
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#    
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#    
#You should have received a copy of the GNU General Public License
#along with this program (see LICENSE.txt).  If not, see 
#<http://www.gnu.org/licenses/>


####################
#   ___________    #
#  |           |   #
#  | |==(*)==| |   #
#   |         |    #
#    |_______|     #
#                  #
####################  


##################
#  aln_place.py  #
##################

''' This module contains functions to make external calls to infernal, taxtastic, and pplacer.
For now this module will only support working with the reference tree we provide
but in the future I will write extensions that will do this for custom built packages as well'''

#Requirements

'''

infernal (I used v1.1.1 June 2012), 
pplacer (v1.1.alpha13r2-0-g79a8847), 
taxit v0.5.3,
FastTree (version 2.1.3 SSE3)

'''

import argparse
import subprocess
import os

wd = os.getcwd()

###################
#Command line Args#
###################

parser = argparse.ArgumentParser(description='This module contains functions to make external calls to infernal, taxtastic, and pplacer. For now this module will only support working with the reference tree we provide but in the future I will write extensions that will do this for custom built packages as well')
parser.add_argument("-i", help="Path to input query sequences", required=True, metavar='<input_seqs>')
parser.add_argument("-o", help="Full path to output directory. If this directory doesn't exist it will be created, if it does it will be overwritten", metavar='<out_dir>', required=True, default= '{0}_aln_out'.format(wd))
parser.add_argument("-t", help="Path to reference tree", required=True, metavar='<ref_tre>')
parser.add_argument("--tree_stats", help="Path to statistics from reference tree build (FastTree, RAxML)", required=True, metavar='<ref_tre_stats>')

parser.add_argument("-p", help="Path profile alignment", required=True, metavar='<profile>')
parser.add_argument("-r", help="Path reference sequnece alignment", required=True, metavar='<ref_seqs>')
parser.add_argument("--procs", help="Number of processors (default=8)", type=int, metavar='nprocs', default = 8)

args = parser.parse_args()

#make query alignments
subprocess.call(["cmalign", '--hbanded' '--sub' '--dnaout' '--outformat pfam' '-g' '--notrunc' '-o {0}/{1}_aln.sto'.format(args.o, args.i), args.p, args.i, '--cpu {0}'.format(args.procs)])

#define path to query aln 
query_aln = '{0}/{1}_aln.sto'.format(args.o, args.i)

#merge alignments
subprocess.call(['esl-alimerge', '--dna', '-o {0}/merged.sto'.format(ars.o),query_aln, args.r])

#now make ref package

# my.refpkg   gg_20_log.txt --tree-file gg97_n20.tre
subprocess.call(['taxit', 'create', '-l 16s_rRNA', '-P my.refpkg','--aln-fasta merged.sto', '--tree-stats {0}'.format(args.tree_stats), '--tree-file {0}'.format(args.t)])

#run pplacer
subprocess.call(['pplacer', '-c {0}my.refpkg/'.format(args.o), '-j {0}'.format(args.procs),'-p','{0}merged.sto'.format(args.o)])

