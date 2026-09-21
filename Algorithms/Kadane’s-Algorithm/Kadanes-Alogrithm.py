#-----------
#53. Maximum Subarray
#-----------
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        ans=nums[0]
        best_answer=nums[0]

        for i in range(1,len(nums)):
            #we have 2 options either best_answer add the new i or new i create the new best answer
            best_answer=max(best_answer+nums[i],nums[i])
            ans=max(best_answer,ans)
        return ans