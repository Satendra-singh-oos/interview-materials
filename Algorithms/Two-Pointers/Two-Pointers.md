# Two Pointer Pattern

### Pattern Detection

* **Sign 1:** The problem involves linear data structures like an **Array**, **String**, or **Linked List**.
* **Sign 2:** The input data is **sorted**, or sorting the given data makes finding the solution easier.
* **Sign 3:** The problem asks to perform operations such as **Rearrange**, **Remove Duplicates**, **Merge**, or **Detect Cycle**.
* **Sign 4:** The problem requires finding a **Pair**, **Triplet**, or **Quadruplet**.
* **Sign 5:** Strict constraint to **not use extra space** ($O(1)$ auxiliary space complexity).

---

### TL;DR

> **Core Concept:** Both pointers must communicate with each other and move accordingly based on conditions.
>
> **Important Distinction:** `Two Pointer` $
eq$ `Sliding Window`.

---

### Top 10 Practice LeetCode Problems

Here are classic LeetCode problems categorized by the pattern detection signs listed above:

| # | Problem | Difficulty | Detection Signs Applied | Key Two-Pointer Strategy |
|---|---|---|---|---|
| 1 | [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | **Easy / Medium** | Sign 2, 4, 5 | **Opposite Direction:** Left pointer starts at `0`, right pointer at `n-1`. Move inward based on target sum comparison. |
| 2 | [15. 3Sum](https://leetcode.com/problems/3sum/) | **Medium** | Sign 2, 4, 5 | **Sorted Array + Outer Loop:** Sort array, fix one element, and use standard two pointers for the remaining pair. Skip duplicates. |
| 3 | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | **Medium** | Sign 1, 5 | **Opposite Direction:** Two pointers at extreme ends; always shrink the pointer pointing to the smaller height. |
| 4 | [26. Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | **Easy** | Sign 2, 3, 5 | **Same Direction (Fast/Slow):** Slow pointer tracks position for unique elements, fast pointer scans the array. |
| 5 | [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | **Easy** | Sign 1, 5 | **Opposite Direction:** Left and right pointers converge to center while skipping non-alphanumeric characters. |
| 6 | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | **Easy** | Sign 1, 3, 5 | **Floyd's Tortoise and Hare:** Slow pointer moves 1 step, fast pointer moves 2 steps. If they meet, cycle exists. |
| 7 | [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | **Easy** | Sign 2, 3, 5 | **Backward Pointers:** Start three pointers from the ends of the arrays to merge in-place without overwriting. |
| 8 | [18. 4Sum](https://leetcode.com/problems/4sum/) | **Medium** | Sign 2, 4, 5 | **Nested Loops + Two Pointer:** Extension of 3Sum with two outer loops and two pointers converging inward. |
| 9 | [977. Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) | **Easy** | Sign 2, 5 | **Opposite Direction:** Compare squared values from left and right ends (largest values live at extremes), populate result from right to left. |
| 10 | [75. Sort Colors](https://leetcode.com/problems/sort-colors/) | **Medium** | Sign 2, 3, 5 | **Dutch National Flag (3 Pointers):** `low` for 0s, `mid` for 1s, and `high` for 2s to partition in single pass $O(1)$ space. |