# Solution Of The Problem Mentioned in the Two-Pointer Readme.md


#---------------------
# Two Sum II - Input Array Is Sorted
#---------------------
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
            left=0
            right=len(numbers)-1

            while left<right:
                sum = numbers[left]+numbers[right]
                if sum == target:
                    return [left+1,right+1]
                elif sum>target:
                    right-=1
                else:
                    left+=1
            return []
    
#---------------------
#   Container With Most Water
#---------------------
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left=0
        right=len(height)-1
        result=0
        while left<right:
            width = right - left
            if height[left] < height[right]:
                area= height[left]*width
                result=max(area,result)
                left+=1
            
            elif height[right]<height[left]:
                area= height[right]*width
                result=max(area,result)
                right-=1

            else:
                area=height[left]*width
                result= max(area,result)
                left+=1
                right-=1
        return result