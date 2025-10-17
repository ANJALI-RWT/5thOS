# backend/algorithms/process_scheduling.py
def fcfs(processes):
    # processes: list of {name, arrival, burst}
    # returns gantt list and waiting/turnaround times
    procs = sorted(processes, key=lambda p: int(p.get('arrival',0)))
    time = 0
    gantt = []
    details = []
    for p in procs:
        arrival = int(p.get('arrival',0))
        burst = int(p.get('burst',0))
        if time < arrival:
            time = arrival
        start = time
        end = time + burst
        gantt.append({"name":p.get('name'), "start":start, "end":end})
        waiting = start - arrival
        turnaround = end - arrival
        details.append({"name":p.get('name'), "arrival":arrival, "burst":burst, "start":start, "end":end, "waiting":waiting, "turnaround":turnaround})
        time = end
    avg_wait = sum(d['waiting'] for d in details)/len(details) if details else 0
    avg_turn = sum(d['turnaround'] for d in details)/len(details) if details else 0
    return {"gantt":gantt, "details":details, "avg_wait":avg_wait, "avg_turnaround":avg_turn}

def sjf_nonpreemptive(processes):
    procs = sorted(processes, key=lambda p: (int(p.get('arrival',0)), int(p.get('burst',0))))
    completed = []
    time = 0
    gantt = []
    details = []
    ready = []
    i = 0
    n = len(procs)
    while len(completed) < n:
        # add arrived
        for j in range(i, n):
            if int(procs[j].get('arrival',0)) <= time:
                ready.append(procs[j])
                i += 1
            else:
                break
        if not ready:
            # jump to next arrival
            if i < n:
                time = int(procs[i].get('arrival',0))
                continue
            else:
                break
        # pick shortest burst
        ready.sort(key=lambda x: int(x.get('burst',0)))
        p = ready.pop(0)
        start = time
        burst = int(p.get('burst',0))
        end = start + burst
        gantt.append({"name":p.get('name'), "start":start, "end":end})
        waiting = start - int(p.get('arrival',0))
        turnaround = end - int(p.get('arrival',0))
        details.append({"name":p.get('name'), "arrival":int(p.get('arrival',0)), "burst":burst, "start":start, "end":end, "waiting":waiting, "turnaround":turnaround})
        completed.append(p)
        time = end
    avg_wait = sum(d['waiting'] for d in details)/len(details) if details else 0
    avg_turn = sum(d['turnaround'] for d in details)/len(details) if details else 0
    return {"gantt":gantt, "details":details, "avg_wait":avg_wait, "avg_turnaround":avg_turn}

def round_robin(processes, quantum):
    q = []
    for p in sorted(processes, key=lambda x:int(x.get('arrival',0))):
        q.append({"name":p.get('name'), "arrival":int(p.get('arrival',0)), "burst":int(p.get('burst',0))})
    time = 0
    ready = []
    gantt = []
    details = {}
    while q or ready:
        # move arrived from q to ready
        while q and q[0]['arrival'] <= time:
            ready.append(q.pop(0))
        if not ready:
            if q:
                time = q[0]['arrival']
                continue
            else:
                break
        p = ready.pop(0)
        run = min(quantum, p['burst'])
        start = time
        end = time + run
        gantt.append({"name":p['name'], "start":start, "end":end})
        time = end
        p['burst'] -= run
        if p['burst'] > 0:
            # new arrival time is current time
            p['arrival'] = time
            ready.append(p)
        else:
            # finished: compute waiting/turnaround quickly: not precise for RR average, but provide basic info
            details[p['name']] = {"finish":time}
    return {"gantt":gantt, "details":details}
