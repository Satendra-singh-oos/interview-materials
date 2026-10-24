# Merge Intervals Pattern

### Pattern Detection Signals
* **Sign 1:** Input is given as a 2D array of ranges/pairs `[[start_1, end_1], [start_2, end_2], ...]`.
* **Sign 2:** The problem asks to identify **overlap, conflict, merge, free time, meeting room usage, CPU load, or scheduling simulation**.
* **Sign 3:** Input looks like `[[1,4], [2,10]]`, hinting at overlapping intervals that need merging or comparison.

---

### TL;DR

> **Core Concept:** Sort intervals by `start` time first. Once sorted, adjacent intervals only overlap if `end1 >= start2`.
>
> **Key Strategy:**
> * **Overlap Condition:** `prev_end >= curr_start`
> * **Merged Interval:** `[prev_start, max(prev_end, curr_end)]`
> * **Time Complexity:** $O(N \log N)$ (due to sorting)
> * **Space Complexity:** $O(N)$ (for output array) or $O(1)$ auxiliary space

---

### Pseudo Code

```text
# Step 1: Sort intervals based on starting times
intervals.sort(key = start_time)

result = [intervals[0]]

# Step 2: Iterate through remaining intervals and check overlaps
for i from 1 to len(intervals) - 1:
    curr_start, curr_end = intervals[i]
    prev_start, prev_end = result.last()

    if prev_end >= curr_start:
        # Overlap detected! Merge by updating end time to max(prev_end, curr_end)
        result.last().end = max(prev_end, curr_end)
    else:
        # No overlap, push as a new interval
        result.append([curr_start, curr_end])

return result
```

---

### Top 10 Practice LeetCode Problems

Here are classic LeetCode problems covering standard Merge Intervals and its variations:

| # | Problem | Difficulty | Variation Type | Key Strategy & Detection |
|---|---|---|---|---|
| 1 | [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/) | **Medium** | **Standard Merge** | Sort by start time. Merge overlapping intervals where `prev_end >= curr_start` with `max(prev_end, curr_end)`. |
| 2 | [57. Insert Interval](https://leetcode.com/problems/insert-interval/) | **Medium** | **Insertion** | Add all intervals before newInterval, merge all overlapping intervals into newInterval, then add remaining intervals. |
| 3 | [252. Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) | **Easy** | **Conflict Detection** | Sort intervals by start time. Check if any adjacent meetings overlap (`prev_end > curr_start`). Return boolean. |
| 4 | [253. Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | **Medium** | **Min Heap / Chronological** | Sort start times and end times separately (or use a Min-Heap for active end times) to track minimum required rooms. |
| 5 | [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | **Medium** | **Greedy Removal** | Sort by **end time**. Keep track of last non-overlapping end time to minimize removals. |
| 6 | [452. Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | **Medium** | **Interval Intersection** | Sort by end coordinate. Shoot an arrow at the end of the first balloon to burst all overlapping balloons. |
| 7 | [986. Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | **Medium** | **Two Pointers** | Compare pairs from two sorted lists. Overlap is `[max(start1, start2), min(end1, end2)]`. Advance the pointer with smaller end time. |
| 8 | [1272. Remove Interval](https://leetcode.com/problems/remove-interval/) | **Medium** | **Interval Splitting** | Compare each interval against `toBeRemoved`. Split intervals that overlap with `toBeRemoved`. |
| 9 | [759. Employee Free Time](https://leetcode.com/problems/employee-free-time/) | **Hard** | **Merged Free Time** | Merge all employee working schedules using a Min-Heap or Sorting, then identify gaps between merged intervals. |
| 10 | [218. The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | **Hard** | **Sweep Line / Priority Queue** | Convert buildings into critical start/end events. Use a Max-Heap / Multiset to track active maximum height at each point. |