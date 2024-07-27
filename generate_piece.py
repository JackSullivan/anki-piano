# coding: utf-8
range(1,33)
ms = list(range(1,33))
ms
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
chunks(ms,2)
list(chunks(ms,2))
list(chunks(ms,4))
list(chunks(ms,8))
def fandl(i):
    return (i[0], i[-1])
    
map(fandl, chunks(ms,8))
list(map(fandl, chunks(ms,8)))
for sz in [2,4,8]:
    pass
    
l = ms
for sz in [2,4,8]:
    l += map(fandl, chunks(ms, sz))
l
list(map(fandl, chunks(ms, 8)))
list(chunks(ms, 8))
ms
ms = list(range(1,33))
list(chunks(ms, 8))
l
l = ms
l = []
for sz in [2,4,8]:
    l += map(fandl, chunks(ms, sz))
    
l
l = []
l += ms
for sz in [2,4,8]:
    l += map(fandl, chunks(ms, sz))
    
l
for itm in l:
    if type(itm) == int:
        print("Minuet in G,Johan Sebastian Bach,{}".format(itm))
    else:
        print("Minuet in G,Johan Sebastian Bach,{}-{}".format(itm[0], itm[1]))
        
ms = list(range(1,17))
l = []
l += ms
for sz in [2,4,8]:
    l += map(fandl, chunks(ms, sz))
    
for itm in l:
    if type(itm) == int:
        print("Nutcracker March,Tchaikovsky,{}".format(itm))
    else:
        print("Nutcracker March,Tchaikovsky,{}-{}".format(itm[0], itm[1]))
        
