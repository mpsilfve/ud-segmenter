from sys import argv, stderr, stdout
from collections import defaultdict
from random import random, shuffle, seed
from math import log
from distance import levenshtein

from split import sample_next, sample_nth, get_init_split, get_str

seed(0)

ALPHA = .1

BJC=0
BC=1
JC=2
C=3
TC=4

def gl(s):
    return "LABEL:" + s 

def get_sl_prob(s, l, alpha, params):
    assert(s != '')
    if not '=' in l:
        return .5**(levenshtein(s,l))
    bjc = params[BJC][s][gl(l)]
    bcs = params[BC][s]
    bcl = params[BC][gl(l)]

    jc = params[JC][s][gl(l)]
    cs = params[C][s]
    cl = params[C][gl(l)]

    basep = (alpha * bjc + jc)**2/((alpha*bcs + cs)*(alpha*bcl + cl))

    return basep

def entropy(params):
    tot = 0
    for s in params[JC]:
        for l in params[JC][s]:
            tot += params[JC][s][l]
    assert(tot!=0)
    
    H = 0
    for s in params[JC]:
        for l in params[JC][s]:
            if params[JC][s][l] != 0:
                H -= log(params[JC][s][l]/tot)
    return H

def update_counts(split,assignment,wf,params,incr):
    for i,s in enumerate(split):
        if i == len(split) - 1:
            break
        for l in assignment[i]:
            params[JC][get_str(i,split,wf)][gl(l)] += incr
#            params[C][get_str(i,split,wf)] += incr
            params[C][gl(l)] += incr
        params[C][get_str(i,split,wf)] += incr

        if i == 0:
            for l in assignment[i]:
                params[TC][gl('#')][gl(l if '=' in l else "STEM")] += 1
        else:
            for pl in assignment[i-1]:
                for l in assignment[i]:
                    params[TC][gl(pl if '=' in pl else "STEM")][gl(l if '=' in l else "STEM")] += 1
                    if not '=' in pl:
                        params[C]["STEM"] += 1

def get_trans_prob(pls,l,params):
    prob = 1.0
    for pl in pls:
        plabel = pl if ('=' in pl or pl == '#') else "STEM"
        label = pl if ('=' in pl or pl == '#') else "STEM"
        prob *= params[TC][gl(plabel)][gl(label)]/(params[C][pl]+1)
    assert(prob != 0)
    return prob

def get_prob(split, assignment, wf, alpha, params):
    tot = 1

    for i, s in enumerate(split):
        if i == len(split) - 1:
            continue
        for l in assignment[i]:
            tot *= get_sl_prob(get_str(i,split,wf),l,alpha,params)
            if i == 0:
                tot *= get_trans_prob(['#'],l,params)
            else:
                tot *= get_trans_prob(assignment[i-1],l,params)
            
    return tot

def sample_from(scores):
    tot = sum([x[0] for x in scores])
    r = tot * random()
    acc = 0
    for j,sl in enumerate(scores):
        score, l = sl
        if score == 0:
            continue
        acc += score
        if acc >= r:
            return l, j
    print(acc,tot)
    assert(0)

def get_assignment(split, labels, wf, alpha, params):
    assignment = [[] for i in range(len(split) - 1)]
#    assignment = [[] for i in range(len(split))]
    used_labels = [0 for l in labels]

    for i, s in enumerate(split):
        if i + 1 == len(split):
            break
        scores = [(get_sl_prob(get_str(i,split,wf),l,alpha,params) if used_labels[j] == 0 else 0,l) 
                  for j,l in enumerate(labels)]
        if i == 0:
            scores = [(get_trans_prob(['#'],l,params)*p,l) for (p,l) in scores]
        else:
            scores = [(get_trans_prob(assignment[i-1],l,params)*p,l) for (p,l) in scores]

        l, j = sample_from(scores)
        assignment[i].append(l)
        used_labels[j] = 1

    for i, l in enumerate(labels):
        if used_labels[i] == 0:
            scores = [(get_sl_prob(get_str(j,split,wf),l,alpha,params),split[j]) 
                      for j,_a in enumerate(assignment)]
            s, j = sample_from(scores)
            assignment[j].append(l)

    return assignment

def filter_labels(labels):
    return labels
#    return [l for l in labels if not l in ["pos=N","pos=V","pos=ADJ","num=SGN","mood=IND","tense=PRS","polar=POS",
#                                          "num=PLV","num=SGV","case=NOM"]]


train_fn = argv[1]
test_fn = argv[2]

train_data =  open(train_fn).read().split('\n')
shuffle(train_data)
test_data =  open(test_fn).read().split('\n')

all_data = train_data + test_data
all_data = [l.split(' ') for l in all_data if l != '']

base_jcounts = defaultdict(lambda : defaultdict(lambda : 0.0))
base_counts = defaultdict(lambda : 0.0)
jcounts = defaultdict(lambda : defaultdict(lambda : 0.0))
counts = defaultdict(lambda : 0.0)
tcounts = defaultdict(lambda : defaultdict(lambda : 1.0))

params = (base_jcounts,
          base_counts,
          jcounts,
          counts,
          tcounts)
all_labels = set()
for fields in all_data:
    wf = fields[-1] + ">"
    fields = filter_labels(fields[:len(fields) - 1])
    all_labels.update(fields)
    for i in range(len(wf)):
        for j in range(i+1, len(wf) + 1):
            base_counts[wf[i:j]] += 1
            for l in fields:
                base_jcounts[wf[i:j]][gl(l)] += 1
#                base_counts[wf[i:j]] += 1
#                base_counts[gl(l)] += 1
#    for l in fields:
#        base_jcounts[""][gl(l)] += 1
#        base_counts[""] += 1
#        base_counts[gl(l)] += 1

for l in all_labels:
    base_jcounts[""][gl(l)] += 1
    base_counts[""] += 1
    base_counts[gl(l)] += 1

splits = []
assignments = []
labels = []
wfs = []

for fields in all_data:
    wf =  fields[-1] + ">"
    fields = filter_labels(fields[:len(fields) - 1])
    wfs.append(wf)
    labels.append(fields)
    s = get_init_split(wf)
    s = sample_nth(100,s,len(fields))
    assignment = get_assignment(s,fields,wf,ALPHA,params)
    splits.append(s)
    assignments.append(assignment)
    update_counts(s,assignment,wf,params,1)

N = 1000

best_splits = []
best_assignment = []
best_H = float('inf')
logfile = open("logfile",'w')
for n in range(N):
    for j, s in enumerate(splits):
        new_split = sample_next(splits[j],len(labels[j]))
        new_assignment = get_assignment(new_split, labels[j], wfs[j], ALPHA, params)
        old_prob = get_prob(splits[j], assignments[j],wfs[j],ALPHA,params)
        new_prob = get_prob(new_split, new_assignment,wfs[j],ALPHA,params)
        if (new_prob / old_prob)**2 > random():
#        if new_prob > old_prob:
            update_counts(splits[j],assignments[j],wfs[j],params,-1)
            splits[j] = new_split
            assignments[j] = new_assignment
            update_counts(splits[j],assignments[j],wfs[j],params,1)
    H = entropy(params)
    logfile.write("%.3f\n" % H)
    logfile.flush()
    if H < best_H:
        best_splits = list(splits)
        best_assignments = list(assignments)
        best_H = H
    stderr.write("%u of passes %u, %.3f\r"# '>':tense=fut %f\r"#, ssa:ine %f isi:cond %f i:pln %f \r" % 
                 % (n+1,N,entropy(params),
#                 params[JC][">"][gl("tense=fut")]/params[C][gl("tense=fut")],
#                  params[JC]["isi"][gl("mood=cnd")]/params[C][gl("mood=cnd")],
#                  params[JC]["i"][gl("number=plur")]/params[C][gl("number=plur")],)
                    ))


stderr.write('\n')
ssac = 0
inc = 0

for i,a  in enumerate(best_assignments):
    if i + 1 < len(train_data):
        continue
    best_split = best_splits[i]
    best_assign = best_assignments[i]
    best_score = get_prob(best_split, best_assign,wfs[i],ALPHA,params)

    split = best_split
    assign = best_assign

    for k in range(5000):
        old_score = get_prob(split, assign,wfs[i],ALPHA,params)
        new_split = sample_next(split,len(labels[i]) - 1)
        new_assign = get_assignment(new_split, labels[i], wfs[i], ALPHA, params)
        new_score = get_prob(new_split, new_assign,wfs[i],ALPHA,params)

        if (new_score/old_score)**2 > random():
            split = new_split
            assign = new_assign
        if new_score > best_score:
            best_split = split
            best_assign = assign
            best_score = new_score

    ss = [get_str(j,best_split,wfs[i]) for j in range(len(best_split) - 1)]
#    ss = [get_str(j,best_split,wfs[i]) for j in range(len(best_split))]
    for j, s in enumerate(ss):
        stdout.write("%s/%s"%(s,','.join(best_assign[j])))
        if j + 1 < len(ss):
            stdout.write(" ")
    print()
    stdout.flush()
