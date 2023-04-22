# Angel Higueros - 20460
# Laboratorio D

from yalex.yalex import Yalex
from tools.graph import display_expression_tree
from tools.tools import infix_postfix
from tree.tree import get_tree

from yalex.analizador import analizar

import sys

# Utilidades
yalex_config = "config/y1.yal"
txt_test = "test/t1.txt"


analyzw_yalex = Yalex(sys.argv[1])
regex = analyzw_yalex.get_regex()
analizar(sys.argv[1], sys.argv[2] )
display_expression_tree(get_tree(infix_postfix(regex)), regex)




