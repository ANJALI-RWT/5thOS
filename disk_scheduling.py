# backend/algorithms/disk_scheduling.py
def fcfs_disk(requests, head):
    order = []
    total_seek = 0
    cur = head
    for r in requests:
        order.append(r)
        total_seek += abs(r - cur)
        cur = r
    return {"order":order, "total_seek":total_seek}

def sstf_disk(requests, head):
    reqs = requests[:]
    cur = head
    order = []
    total_seek = 0
    while reqs:
        # choose nearest
        nearest = min(reqs, key=lambda x: abs(x-cur))
        total_seek += abs(nearest - cur)
        order.append(nearest)
        cur = nearest
        reqs.remove(nearest)
    return {"order":order, "total_seek":total_seek}

def scan_disk(requests, head, direction='up', max_track=199):
    # simple SCAN (elevator)
    reqs = sorted(requests)
    order = []
    total_seek = 0
    cur = head
    if direction == 'up':
        up = [r for r in reqs if r >= cur]
        down = [r for r in reqs if r < cur][::-1]
        seq = up + [max_track] + down
    else:
        down = [r for r in reqs if r <= cur][::-1]
        up = [r for r in reqs if r > cur]
        seq = down + [0] + up
    for s in seq:
        total_seek += abs(s - cur)
        order.append(s)
        cur = s
    return {"order":order, "total_seek":total_seek}
