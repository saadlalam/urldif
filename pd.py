
# -*- coding:utf-8 -*-
import random
import sys
import inspect
import os
BETRAY = True
SILENT = False

class Alg:
    def play(self, my_history, their_history):
        """ @param my_history List of own last choices
            @param their_history List of last choices of the other
            @return decision {BETRAY, SILENT}
        """
        raise NotImplementedError
    def __repr__(self):
        return "{}()".format(type(self).__name__)

def score(A_choice, B_choice):
    if A_choice == B_choice:
        if A_choice == BETRAY:
            return (1, 1)
        return (3, 3)
    if A_choice == BETRAY:
        return (5, 0)
    return (0, 5)

def play(A, B, *, rounds=200):
    A_choices = []
    A_score = 0
    B_choices = []
    B_score = 0
    for i in range(rounds):
        A_choice = A.play(A_choices, B_choices)
        B_choice = B.play(B_choices, A_choices)
        A_score_, B_score_ = score(A_choice, B_choice)
        A_score += A_score_
        B_score += B_score_
        A_choices.append(A_choice)
        B_choices.append(B_choice)
    #print("A={!r}\nB={!r}".format(A_choices, B_choices))
    return (A_score, B_score)

def simulate(algs, *, seed=42, rounds=200):
    random.seed(seed)
    score = [[0] * len(algs) for i in range(len(algs))]

    for idx_A, A in enumerate(algs):
        for idx_B, B in enumerate(algs):
            if idx_B > idx_A:
                break
            A_score, B_score = play(A, B, rounds=rounds)
            score[idx_A][idx_B] = A_score
            score[idx_B][idx_A] = B_score

    for line in range(len(algs)):
        s = sum(score[line])/len(algs)
        score[line].insert(0, "{:.2f}".format(s))
        score[line].insert(0, "{!r}".format(algs[line]))
    score.sort(key=lambda l: l[1], reverse=True)
    #os.path.expandvars(unicode("↓", 'UTF-8'))
    score.insert(0, ["{!r}".format(a) for a in [u"AD BR", "total"] + algs])
    print_mat(score)

def print_mat(matrix):
    # https://stackoverflow.com/a/13214945
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

def inst_all():
    cls = Alg.__subclasses__()
    inst = []
    for cl in cls:
        inst.append(cl())
    return inst

################################################################################
class Tim(Alg):
    def __init__(self, p_silent=0.5):
        self.p_silent = p_silent
    def play(self, my_history, their_history):
        if random.random() < self.p_silent:
            return SILENT
        return BETRAY
    def __repr__(self):
        return "{}(p_silent={!r})".format(type(self).__name__, self.p_silent)
class Betray(Alg):
    def play(self, my_history, their_history):
        return BETRAY
class Silent(Alg):
    def play(self, my_history, their_history):
        return SILENT
class Tit4Tat(Alg):
    def play(self, my_history, their_history):
        if len(their_history) == 0:
            return SILENT
        return their_history[-1]
class GenerousTit4Tat(Alg):
    def play(self, my_history, their_history):
        if len(their_history) == 0:
            return SILENT
        if their_history[-1] == SILENT:
            return SILENT
        if random.random() < 0.5:
            return SILENT
        return BETRAY
class Tit42Tat(Alg):
    def play(self, my_history, their_history):
        if len(their_history) <= 1:
            return SILENT
        if their_history[-1] == BETRAY and their_history[-2] == BETRAY:
            return BETRAY
        return SILENT
class PerKind(Alg):
    def play(self, my_history, their_history):
        m = len(their_history) % 3
        if m == 0 or m == 1:
            return SILENT
        return BETRAY
class PerNasty(Alg):
    def play(self, my_history, their_history):
        m = len(their_history) % 3
        if m == 0 or m == 1:
            return BETRAY
        return SILENT


class Max(Alg):
    def play(self, my_history, their_history):
        if random.random() < 0.667:
            return SILENT
        return BETRAY
class Susann(Alg):
    def play(self, my_history, their_history):
        mod = len(their_history) % 6
        if mod < 4:
            return SILENT
        return BETRAY
# aka Friedman
class Robert(Alg):
    def play(self, my_history, their_history):
        if BETRAY in their_history:
            return BETRAY
        return SILENT
class ThiLa(Alg):
    def play(self, my_history, their_history):
        if len(their_history) < 3:
            return BETRAY
        return SILENT
class RandomNasty(Alg):
    def play(self, my_history, their_history):
        if random.random() < 0.667:
            return BETRAY
        return SILENT
class Theresa(Alg):
    def play(self, my_history, their_history):
        if len(their_history) == 0:
            return BETRAY
        if len(their_history) == 1:
            if their_history[-1] == BETRAY:
                return SILENT
            return BETRAY
        if their_history[-1] == BETRAY or their_history[-2] == BETRAY:
            return SILENT
        return BETRAY
class Dirk(Alg):
    def play(self, my_history, their_history):
        cnt_betray = len([x for x in their_history if x == BETRAY])
        if cnt_betray > 0.5 * len(their_history):
            return BETRAY
        return SILENT
class WinStayLoseShift(Alg):
    def play(self, my_history, their_history):
        if len(their_history) == 0:
            return SILENT
        if my_history[-1] == SILENT and their_history[-1] == SILENT:
            return SILENT
        if my_history[-1] == SILENT and their_history[-1] == BETRAY:
            return BETRAY
        if my_history[-1] == BETRAY and their_history[-1] == SILENT:
            return BETRAY
        return SILENT

####################################################################################################
### main
if __name__ == '__main__':
    algs = inst_all()
    simulate(algs, seed=42, rounds=200)