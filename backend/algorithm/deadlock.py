# backend/algorithms/deadlock.py
def bankers_algorithm(allocation, max_need, available):
    """
    allocation: list of lists (n x m)
    max_need: list of lists (n x m)
    available: list (m)
    returns dict with safe sequence if exists
    """
    n = len(allocation)
    m = len(available)
    alloc = [row[:] for row in allocation]
    maxn = [row[:] for row in max_need]
    need = [[maxn[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    work = available[:]
    finish = [False]*n
    safe_seq = []
    changed = True
    while len(safe_seq) < n and changed:
        changed = False
        for i in range(n):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(m)):
                    # can allocate
                    for j in range(m):
                        work[j] += alloc[i][j]
                    finish[i] = True
                    safe_seq.append(i)
                    changed = True
    is_safe = all(finish)
    return {"is_safe": is_safe, "safe_sequence": safe_seq if is_safe else [], "need": need, "work_end": work}
