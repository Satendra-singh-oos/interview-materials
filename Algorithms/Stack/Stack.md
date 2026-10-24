# Stack Patterns

### Pattern Detection Signals
* **Sign 1:** The problem involves linear data structures like an **Array**, **String**, or **Linked List**.
* **Sign 2:** As you traverse from left-to-right (or right-to-left), you need to make decisions based on the **most recently visited elements** (Last-In, First-Out access).
* **Sign 3:** The problem keywords include **Next/Previous Greater Element (NGE/PGE)**, **Next/Previous Smaller Element (NSE/PSE)**, **Matching / Canceling Pairs** (e.g., valid parentheses, adjacent duplicates), or **Remove $K$ elements**.
* **Sign 4:** You need to maintain a sorted order of elements inside the stack to find nearest bounds in $O(1)$ time.

---

### TL;DR

> **Core Concept:** A stack acts like a **gun magazine** — you can only inspect, remove, or insert elements at the very top. It gives instant access to the most recent history.
>
> **3 Main Stack Variations:**
> 1. **Simple Push / Pop Stack:** Used for matching, canceling, or reversing (e.g., Parentheses, String cleaning).
> 2. **Monotonic Stack:** Maintains strictly **increasing** or **decreasing** values inside the stack to solve NGE / NSE / PGE / PSE problems in $O(N)$ time.
> 3. **Greedy Stack:** Uses custom conditions to dynamically adjust element positions for optimal output (e.g., Remove $K$ Digits).

---

### Pseudo Code

#### Monotonic / Standard Stack Template

```text
# Initialize stack (can store values or indices depending on problem)
stack = []
result = [-1] * len(arr)  # Default value if no NGE/NSE exists

for i in range(len(arr)):
    # 1. Pop elements from stack while they violate the desired property
    while stack is not empty and condition_satisfied(stack.top(), arr[i]):
        # Example condition for Next Greater Element: stack.top() < arr[i]
        popped_index = stack.pop()
        result[popped_index] = arr[i]  # Or save result as needed
        
    # 2. Check current stack state (optional based on left-to-right vs right-to-left traversal)
    if stack is not empty:
        # stack.top() now holds the Previous Greater/Smaller element
        pass
        
    # 3. Push current element (or index) onto stack
    stack.push(i)

return result
```

---

### Top 10 Practice LeetCode Problems

Here are classic LeetCode problems covering standard stack, monotonic stack, and greedy stack variations:

| # | Problem | Difficulty | Stack Type | Key Strategy & Detection |
|---|---|---|---|---|
| 1 | [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | **Medium** | **Monotonic Decreasing** | **Next Greater Element:** Use stack to store indices. Pop smaller temperatures when warmer day is found. |
| 2 | [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | **Easy** | **Monotonic Decreasing** | **NGE + HashMap:** Traversal with monotonic stack to map each element to its Next Greater Element. |
| 3 | [503. Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | **Medium** | **Monotonic + Circular** | **Circular Array NGE:** Loop through the array twice `2 * N` using index modulo `i % N` with monotonic stack. |
| 4 | [2487. Remove Nodes From Linked List](https://leetcode.com/problems/remove-nodes-from-linked-list/) | **Medium** | **Monotonic Decreasing** | **Linked List NGE:** Use stack (or reverse list) to remove nodes that have a node with a strictly greater value to their right. |
| 5 | [84. Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | **Hard** | **Monotonic Increasing** | **NSE / PSE bounds:** Use stack to find Left and Right boundaries where height stops being smaller. |
| 6 | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | **Hard** | **Monotonic Decreasing** | **Bounded Container:** Maintain decreasing heights. When a taller height arrives, calculate trapped water between left boundary, current height, and popped base. |
| 7 | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | **Easy** | **Simple Push/Pop** | **Matching Pairs:** Push open brackets, pop and match on closing brackets. Stack must be empty at the end. |
| 8 | [1047. Remove All Adjacent Duplicates In String](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) | **Easy** | **Simple Push/Pop** | **Canceling:** Pop if current character matches `stack.top()`, otherwise push. |
| 9 | [402. Remove K Digits](https://leetcode.com/problems/remove-k-digits/) | **Medium** | **Greedy Stack** | **Monotonic Increasing:** Pop larger previous digits when a smaller current digit arrives to form the smallest possible number. |
| 10 | [901. Online Stock Span](https://leetcode.com/problems/online-stock-span/) | **Medium** | **Monotonic Decreasing** | **PGE Count:** Store `(price, span)` pairs in stack. Pop smaller prices and aggregate their spans. |