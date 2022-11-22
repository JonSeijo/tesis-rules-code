# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import argparse
import re

class StringMetrics(object):
    """ Compute metrics for strings  """

    def levenshtein(s1, s2):
        """ Levenshtein or edit distance for two strings s1 and s2 """
        ls1 = len(s1)
        ls2 = len(s2)

        if ls1 == 0:
            return ls2

        if ls2 == 0:
            return ls1

        v0 = list(range(ls1+1))
        v1 = []

        for i in range(ls1+1):
            v1.append(0)

        for i in range(0, ls2):
            v1[0] = i+1
            for j in range(0, ls1):
                substitution_cost = v0[j]
                if s1[j] != s2[i]:
                    substitution_cost = substitution_cost + 1

                v1[j+1] = min(v0[j+1] + 1, v1[j] + 1, substitution_cost);

            v0 = list(v1) #Important to copy the list!!


        return v1[ls1]

