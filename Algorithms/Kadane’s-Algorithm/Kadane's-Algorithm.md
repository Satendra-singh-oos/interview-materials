# Kadane's Algorithm

### Pattern Detection
- **Sign 1:** Question is related to **Array** only and strictly involves contiguous **Subarrays**.
- **Sign 2:** Question asks us to find **maximum, minimum sum, product, or frequency** in a subarray.
- **Sign 3:** Sometimes we have twisted conditions (e.g., absolute value, delete at most one element, circular arrays, etc.).



---

### Core Intuition & Logic

1. At any index `i`, you must know the **best continuous result possible up to index `i-1`**.
2. At index `i`, you face **2 choices**:
   * **Extend:** Include `a[i]` in the existing running subarray (`best_ending + a[i]`).
   * **Restart:** Start a fresh subarray starting at `a[i]`.
3. Update the global `result` at every step.

---

### TL;DR
- **Core Logic:** At index `i`, decide whether to **extend** the previous subarray's answer or **start a new subarray** from index `i`.
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

---

### Pseudo Code

```text
result = a[0]
best_answer = a[0]

for i in range(1, len(a)):
    # 2 choices at i: extend previous subarray OR start a new one with a[i]
    best_answer = max(best_answer + a[i], a[i])
    result = max(result, best_answer)

return result
```

> **Note:** Most of the time, twisted conditions modify `best_answer` (e.g., tracking `one_deletion` or tracking both `min_prod` & `max_prod` for product variants).

---

### Top 10 Practice LeetCode Problems

Here are classic LeetCode problems covering standard Kadane's algorithm and its variations:

| # | Problem | Difficulty | Variation Type | Key Strategy |
|---|---|---|---|---|
| 1 | [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | **Easy / Medium** | **Standard** | Standard Kadane's algorithm. `best = max(best + nums[i], nums[i])`. |
| 2 | [152. Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | **Medium** | **Product Variant** | Track both `max_prod` and `min_prod` because a negative number multiplied by a negative becomes positive. |
| 3 | [918. Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) | **Medium** | **Circular Array** | Calculate `max_subarray` using Kadane's and `min_subarray` using inverse Kadane's. Total sum minus `min_subarray` yields circular maximum. |
| 4 | [1186. Maximum Subarray Sum with One Deletion](https://leetcode.com/problems/maximum-subarray-sum-with-one-deletion/) | **Medium** | **One Deletion** | Track two states at `i`: `no_deletion` (standard Kadane's) and `one_deletion` (`max(prev_no_del, prev_one_del + nums[i])`). |
| 5 | [1749. Maximum Absolute Sum of Any Subarray](https://leetcode.com/problems/maximum-absolute-sum-of-any-subarray/) | **Medium** | **Absolute Sum** | Run standard Kadane's twice (once for maximum subarray sum and once for minimum subarray sum). Answer is `max(abs(max_sum), abs(min_sum))`. |
| 6 | [2321. Maximum Score Of Spliced Array](https://leetcode.com/problems/maximum-score-of-spliced-array/) | **Hard** | **Array Swap** | Reduce swap effect to difference array `diff[i] = nums2[i] - nums1[i]`. Apply Kadane's on `diff` to find max potential gain. |
| 7 | [1191. K-Concatenation Maximum Sum](https://leetcode.com/problems/k-concatenation-maximum-sum/) | **Medium** | **Repeated Array** | Combine Kadane's over two concatenated arrays with array sum logic based on whether total sum is positive. |
| 8 | [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | **Easy** | **Difference Array** | Equivalent to Kadane's algorithm applied to the daily price difference array (`prices[i] - prices[i-1]`). |
| 9 | [2606. Find the Substring With Maximum Cost](https://leetcode.com/problems/find-the-substring-with-maximum-cost/) | **Medium** | **Mapped Values** | Map string characters to custom integer values, then execute standard Kadane's algorithm on the mapped array. |
| 10 | [363. Max Sum of Rectangle No Larger Than K](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/) | **Hard** | **2D Matrix Kadane** | Fix left and right columns, reduce 2D sum to 1D array across rows, then use dynamic 1D Kadane's / Binary Search logic. |