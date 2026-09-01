# Sliding Window Pattern

### Pattern Detection Signals

* **Sign 1:** The problem involves linear data structures like an **Array** or **String**.
* **Sign 2:** The problem explicitly asks for operations related to a **Subarray** or **Substring**.
* **Sign 3:** The problem asks to find metrics such as **Maximum**, **Minimum**, **Longest**, **Shortest**, **Sum / Count / Average**, or conditions like **At most $K$**, **At least $K$**, or **Exactly $K$**.

---

### TL;DR

> **Core Concept:** There are two main types of sliding windows:
> 1. **Fixed Window Size:** The window size $K$ remains constant.
> 2. **Variable Window Size:** The window size dynamically grows and shrinks based on problem constraints.
>
> **Key Optimization Notes:**
> * After sliding to a new window, calculate and update stored window state/information.
> * Most of the time, use a **HashMap** (for arrays) or an array of size 256 (for character frequencies in strings) to track window state.

---

### Pseudo Codes

#### 1. Fixed Size Window Pseudo Code

```text
low = 0, high = k - 1

for i in range(len(arr)):
    # Calculate initial window information (from low = 0 to high = k - 1)
    
    while high < n:
        # Save current window answer
        # Remove arr[low] from window information (e.g., sum = sum - arr[low])
        # Move low: low++
        # Edge case check: if high == n - 1, break
        # Advance high and add arr[high] to window information: high++
        
return answer
```

#### 2. Variable Size Window Pseudo Code

##### A. Maximum Window Variant
```text
low = 0, high = 0

while high < n:
    # Include current value at high into window information
    
    while information_is_wrong:
        # Remove arr[low] from window information
        # Move low pointer to shrink window until information becomes valid: low++
        
    # Window information is now valid
    # Calculate length_of_window = high - low + 1
    # Update max_length answer: ans = max(ans, length_of_window)
    
    high++
```

##### B. Minimum Window Variant
*(Most questions involve conditions like "greater than or equal to $K$")*

```text
low = 0, high = 0

while high < n:
    # Include current value at high into window information
    
    while information_is_correct:
        # Save valid window answer: length = high - low + 1; ans = min(ans, length)
        # Remove arr[low] from window information
        # Shrink window: low++
        
    high++
```

---

### Top 10 Practice LeetCode Problems

Here are classic LeetCode problems categorized by fixed vs. variable sliding window types:

| # | Problem | Difficulty | Window Type | Key Strategy & Detection |
|---|---|---|---|---|
| 1 | [643. Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | **Easy** | **Fixed** | **Fixed Size ($K$):** Track running sum over window of size $K$. Slide window by adding right element and subtracting left element. |
| 2 | [1456. Maximum Number of Vowels in a Substring of Given Length](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) | **Medium** | **Fixed** | **Fixed Size ($K$):** Maintain vowel count within a window of length $K$. |
| 3 | [438. Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | **Medium** | **Fixed** | **Fixed Size + Frequency Map:** Window size equals length of pattern string `p`. Compare frequency array of size 26. |
| 4 | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | **Medium** | **Variable (Max)** | **Max Window:** Expand `high` while using a HashMap/Set to detect duplicate characters. Shrink `low` when duplicate is found. |
| 5 | [1004. Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | **Medium** | **Variable (Max)** | **Max Window (At most $K$):** Expand `high` tracking zero count; shrink `low` when zero count exceeds $K$. |
| 6 | [904. Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | **Medium** | **Variable (Max)** | **Max Window (At most $K=2$):** Track distinct fruit types using a HashMap; shrink `low` when map size exceeds 2. |
| 7 | [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | **Medium** | **Variable (Min)** | **Min Window ($\ge K$):** Expand `high` until sum $\ge target$. While sum is valid, record minimum length and shrink `low`. |
| 8 | [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | **Hard** | **Variable (Min)** | **Min Window + Frequency Map:** Expand `high` until all target characters are satisfied, then shrink `low` to find smallest valid window. |
| 9 | [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | **Medium** | **Variable (Max)** | **Max Window:** Track max frequency character in window. Condition: `(window_length - max_freq) <= K`. |
| 10 | [992. Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) | **Hard** | **Variable (Exact)** | **Exact $K$ Strategy:** Solve using `atMost(K) - atMost(K - 1)` trick with variable sliding windows. |