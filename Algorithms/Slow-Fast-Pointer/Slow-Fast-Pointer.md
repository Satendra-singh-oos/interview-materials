# Fast & Slow Pointer Pattern (Floyd's Cycle Detection)

* **Scope:** Most commonly used in **Linked Lists**, but also applies to **Arrays**, **Strings**, and **Number-based** problems (e.g., Happy Number,Find the Duplicate Number).

---

### Pattern Detection Signals

* **Sign 1:** The problem explicitly or implicitly asks to **detect a cycle**.
* **Sign 2:** The problem asks to find the **starting point (entrance) of a cycle**.
* **Sign 3:** The problem asks to find the **middle element** of a Linked List.

---

### TL;DR

> **Core Concept:** Move `slow` by 1 step and `fast` by 2 steps.
> * **Cycle Detection:** If `slow == fast`, a cycle exists.
> * **Middle Element:** When `fast` reaches the end, `slow` will be at the middle.

---

### Pseudo Codes

#### 1. Detect Cycle & Find Cycle Entry Point

```text
slow = start  # head (Linked List), arr[0] (Array), or n (Number)
fast = start

while fast is not at end:
    slow = move 1 step (e.g., slow.next, arr[slow], or sum_of_squares(n))
    fast = move 2 steps (e.g., fast.next.next, arr[arr[fast]], or sum_of_squares(sum_of_squares(n)))
    
    if slow == fast:
        # Option A: Just detect cycle
        return True 
        
        # Option B: Find the starting point of the cycle
        slow = start
        while slow != fast:
            slow = move 1 step
            fast = move 1 step
        return slow  # 'slow' is now at the entrance of the cycle
        
return False
```

#### 2. Find Middle Element of Linked List

```text
slow = head
fast = head

while fast != null and fast.next != null:
    slow = slow.next
    fast = fast.next.next

return slow  # 'slow' points to the middle node
```

---

### Top 10 Practice LeetCode Problems

Here are classic LeetCode problems categorized by Fast & Slow Pointer application types:

| # | Problem | Difficulty | Application Type | Key Strategy |
|---|---|---|---|---|
| 1 | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | **Easy** | **Cycle Detection** | Standard cycle detection in Linked List. Fast moves 2 steps, slow moves 1 step. |
| 2 | [142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | **Medium** | **Cycle Entrance** | Detect cycle, then reset `slow` to `head` and step both 1 node at a time to find the start node. |
| 3 | [876. Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | **Easy** | **Find Middle** | Standard two-pointer middle search. Stops when `fast == null` or `fast.next == null`. |
| 4 | [202. Happy Number](https://leetcode.com/problems/happy-number/) | **Easy** | **Number-based Cycle** | Treat sum-of-squared-digits function as `.next`. Use fast/slow to detect infinite loops. |
| 5 | [287. Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | **Medium** | **Array Cycle Entrance** | Treat array indices as implicit pointers (`arr[i]`). Duplicate value acts as cycle entrance. |
| 6 | [234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | **Easy** | **Find Middle + Reverse** | Use fast & slow pointers to find middle node, reverse second half, and compare with first half. |
| 7 | [143. Reorder List](https://leetcode.com/problems/reorder-list/) | **Medium** | **Find Middle + Interleave** | Find middle node using fast/slow, reverse second half, then interleave nodes from both halves. |
| 8 | [19. Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | **Medium** | **Pointer Gap (N steps)** | Advance `fast` pointer $N$ steps ahead, then move `slow` and `fast` together at same speed. |
| 9 | [2130. Maximum Twin Sum of a Linked List](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/) | **Medium** | **Find Middle + Twin Sum** | Locate middle with fast/slow pointers, reverse second half, and calculate max pair sums. |
| 10 | [457. Circular Array Loop](https://leetcode.com/problems/circular-array-loop/) | **Medium** | **Array Cycle Detection** | Apply fast/slow pointers on array transitions considering direction consistency and loop length > 1. |