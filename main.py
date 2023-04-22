# Angel Higueros - 20460
# Laboratorio D

from yalex.yalex import Yalex
from tools.graph import display_expression_tree
from tools.tools import infix_postfix
from tree.tree import get_tree

from yalex.analizador import analizar

import sys

# Utilidades
yalex_config = "config/y0.yal"
txt_test = "test/test0.txt"


# analyzw_yalex = Yalex(sys.argv[1])
# regex = analyzw_yalex.get_regex()
analizar(txt_test, yalex_config)
# display_expression_tree(get_tree(infix_postfix(regex)), regex)




