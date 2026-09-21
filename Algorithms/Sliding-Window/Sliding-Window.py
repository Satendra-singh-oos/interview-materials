# Solution Of The Problem Mentioned in the Sliding-Window Readme.md

#-----------
# Maximum Average Subarray I
#-----------
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        if(k>len(nums)):return 0
        
        low=0
        high=k-1
        sum=0

        for i in range(k):
            sum+=nums[i]

        result=sum
        while high<len(nums):
            result=max(result,sum)
            sum= sum- nums[low]
            low+=1
            if high==len(nums)-1:break
            high+=1
            sum=sum+ nums[high]
        
        return result/k

#-----------
# Maximum Number of Vowels in a Substring of Given Length
#-----------
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        count = 0
        # Using a set makes lookups much faster O(1)
        vowel = {'a', 'e', 'i', 'o', 'u'}

        low = 0
        high = k - 1

        # Check all elements in the initial window (up to k elements)
        for i in range(k):
            if s[i] in vowel:
                count += 1

        ans = count

        while high < len(s):
            ans = max(ans, count)
            if s[low] in vowel:
                count -= 1
            low += 1
            if high == len(s) - 1: 
                break
            high += 1
            if s[high] in vowel:
                count += 1
                
        return ans


#-----------
# Find All Anagrams in a String
#-----------
class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        if len(s)<len(p):
            return[]

        p_count=[0]*26
        s_count=[0]*26
        window_size=len(p)
        low=0
        high=window_size-1
        result =[]

        for i in range(window_size):
            s_count[ord(s[i]) - ord("a")] += 1
            p_count[ord(p[i]) - ord("a")] += 1
        

        while(high<len(s)):
            if s_count == p_count:
                result.append(low)
            
            #remove low from the window
            s_count[ord(s[low]) - ord("a")] -= 1
            low+=1

            # edge case 
            if high == len(s)-1:
                break
            
            high+=1
            # now include the new high
            s_count[ord(s[high]) - ord("a")] += 1
            
        return result

