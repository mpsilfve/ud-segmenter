from sys import argv

sysdata = open(argv[1]).read().split('\n')
golddata = open(argv[2]).read().split('\n')

sys_boundaries = set()
gold_boundaries = set()

sysboundstot = 0
goldboundstot = 0
bothbounds = 0

sysmorphs = set()
goldmorphs = set()

lsysmorphs = set()
lgoldmorphs = set()

for i, sysline in enumerate(sysdata):
    if sysline == '':
        continue
    sysline = sysline.replace(">","")
    goldline = golddata[i].replace(">","")

    syschunks = sysline.split(' ')
    goldchunks = goldline.split(' ')

    systoks = [x[:x.find('/')] for x in syschunks if '/' in x]
    goldtoks = [x[:x.find('/')] for x in goldchunks if '/' in x]
    syslabels = [x[x.find('/')+1:].split(',') for x in syschunks if '/' in x]
    goldlabels = [x[x.find('/')+1:].split(',') for x in goldchunks if '/' in x]

    assert(len(syslabels) == len(systoks))
    assert(len(goldlabels) == len(goldtoks))

    systoks = [x for x in systoks if x != '']
    goldtoks = [x for x in goldtoks if x != '']
    if ''.join(systoks) != ''.join(goldtoks):
        print(i+1)

    assert(''.join(systoks) == ''.join(goldtoks))
    if systoks.count("0") or systoks.count("1") or systoks.count("2") or systoks.count("6"):
        sysmorphs.add(''.join(systoks))
        goldmorphs.add(''.join(goldtoks))
        continue
    sysbounds = [0] + [len(x) for x in systoks]
    goldbounds = [0] + [len(x) for x in goldtoks]
    
    cumul = 0
    for j in range(len(sysbounds)):
        l = sysbounds[j]
        cumul += l
        sysbounds[j] = cumul
    cumul = 0
    for j in range(len(goldbounds)):
        l = goldbounds[j]
        cumul += l
        goldbounds[j] = cumul

    sysbounds = sysbounds
    goldbounds = goldbounds

    sysbounds = set(sysbounds)
    goldbounds = set(goldbounds)

    sysboundstot += len(sysbounds)
    goldboundstot += len(goldbounds)
    bothbounds += len(sysbounds.intersection(goldbounds))

#    if systoks != goldtoks:
#        print("SYS:",' '.join(systoks), "GOLD:", ' '.join(goldtoks))

    for k,m in enumerate(goldtoks):
        goldmorphs.add((i,m))
        for l in goldlabels[k]:
            lgoldmorphs.add((i,m,l))

    if len(goldlabels) > len(goldtoks):
        for l in goldlabels[-1]:
            lgoldmorphs.add((i,"",l))

    for k,m in enumerate(systoks):
        sysmorphs.add((i,m))
        for l in syslabels[k]:
            lsysmorphs.add((i,m,l))

    if len(syslabels) > len(systoks):
        for l in syslabels[-1]:
            lsysmorphs.add((i,"",l))

boundsr = bothbounds * 1.0 / goldboundstot
boundsp = bothbounds * 1.0 / sysboundstot
boundsf = 2 * boundsp * boundsr / (boundsp + boundsr)
print("Boundaries R:%.3f P:%.3f F%.3f"%(100*boundsr,100*boundsp,100*boundsf))

morphr = len(sysmorphs.intersection(goldmorphs)) * 1.0 / len(goldmorphs)
morphp = len(sysmorphs.intersection(goldmorphs)) * 1.0 / len(sysmorphs)
morphf = 2 * morphp * morphr / (morphp + morphr)
print("Morphemes R:%.3f P:%.3f F%.3f"%(100*morphr,100*morphp,100*morphf))

morphr = len(lsysmorphs.intersection(lgoldmorphs)) * 1.0 / len(goldmorphs)
morphp = len(lsysmorphs.intersection(lgoldmorphs)) * 1.0 / len(sysmorphs)
morphf = 2 * morphp * morphr / (morphp + morphr)
print("Labeled morphemes R:%.3f P:%.3f F%.3f"%(100*morphr,100*morphp,100*morphf))
