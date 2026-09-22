#-------
# 141. Linked List Cycle
#-------
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast = head
        slow = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
                
        return False
    
    
#-------
# 142. Linked List Cycle II
#-------
# Explanation of Logic:
# Let L1 = distance from head to the cycle entry.
# Let C  = length of the cycle.
# Let d  = distance from the cycle entry to the meeting point
#          in the direction of traversal.
#
# At the meeting point:
#   slow traveled = L1 + d
#   fast traveled = 2(L1 + d)
#
# Since both pointers are at the same node, the extra distance traveled
# by fast must be an integer number of complete cycles:
#
#   2(L1 + d) - (L1 + d) = kC
#   L1 + d = kC
#   L1 = kC - d
#      = (k - 1)C + (C - d)
#
# C - d is the distance from the meeting point back to the cycle entry
# along the direction of traversal.
#
# Therefore, if one pointer starts from head and another starts from the
# meeting point, and both move one step at a time, they will meet at the
# cycle entry.


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast: 
                break
        else:
            return None
            
        ptr1 = head
        ptr2 = slow
        while ptr1 != ptr2:
            ptr1 = ptr1.next
            ptr2 = ptr2.next
            
        return ptr1



#-----
# 876. Middle of the Linked List
#-----
class Solution:
    def middleNode(self, head: ListNode | None) -> ListNode | None:
        slow=head
        fast=head

        while fast and fast.next:
            slow=slow.next
            fast=fast.next.next

        return slow
