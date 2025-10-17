# backend/algorithms/memory_management.py
def fifo_page_replacement(pages, frames):
    """
    pages: list of ints (page numbers)
    frames: int
    returns page frames over time and page faults count
    """
    frames_list = []
    frame = []
    faults = 0
    queue = []
    for p in pages:
        if p not in frame:
            faults += 1
            if len(frame) < frames:
                frame.append(p)
                queue.append(p)
            else:
                # replace FIFO
                out = queue.pop(0)
                idx = frame.index(out)
                frame[idx] = p
                queue.append(p)
        frames_list.append(frame.copy())
    return {"frames_over_time":frames_list, "page_faults":faults}

def lru_page_replacement(pages, frames):
    frames_list = []
    frame = []
    faults = 0
    for i,p in enumerate(pages):
        if p in frame:
            # move to recent: remove and append
            frame.remove(p)
            frame.append(p)
        else:
            faults += 1
            if len(frame) < frames:
                frame.append(p)
            else:
                frame.pop(0)
                frame.append(p)
        frames_list.append(frame.copy())
    return {"frames_over_time":frames_list, "page_faults":faults}
