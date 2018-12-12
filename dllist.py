from copy import deepcopy
# Doubly-linked list implementation

# 
# Modify this file
#
class Precondition(Exception):
    pass
class Postcondition(Exception):
    pass

class NoSuchLink(Exception):
    pass

# A double link has three fields
#  - data <-- The underlying data the link is storing
#  - back <-- A reference to the previous element
#             (possibly None)
#  - next <-- A reference to the next element
#             (possibly None)
class DoubleLink:
    def __init__(self,data,back,nxt):
        self.data    = data
        self.prevLnk = back
        self.nextLnk = nxt

    # Make this object work with "deep" equality. See this
    # StackOverflow post:
    #     https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python
    def __eq__(self, other): 
        if (other):
            return self.__dict__ == other.__dict__
        return False
    def __str__(self):
        return str(self.data)
    def hasNext(self):
        return (self.nextLnk != None)
    
    def hasPrev(self):
        return (self.prevLnk != None)

    def getData(self):
        return self.data

    def getNext(self):
        return self.nextLnk

    def getPrev(self):
        return self.prevLnk

    def setNext(self, n):
        self.nextLnk = n

    def setPrev(self, n):
        self.prevLnk = n


#A doubly-linked list
# 15 points
class DLList:
    # Constructor for empty doubly-linked list
    def __init__(self):
        self.first = None

    # Calculate the size of the list
    #  1 points
    def size(self):
        #edge case handled
        link = self.first
        i=0
        while(link != None):
            link = link.getNext()
            i+=1
        return i
        
    # Check whether this doubly-linked list is equal to another
    # list. Two lists should be equal when they contain exactly the
    # same sequence of elements, where the comparison of each object
    # happens using the == operator.
    # 
    # I.e., two lists (e.g., created using distinct calls to the
    # DoublyLinkedList constructor and subsequent calls to add)
    # containing the sequence of elements: 
    # 
    #   (1,1), (0,1), (1,0)
    # 
    # Should be equal
    #   2 points
    def __eq__(self, other): 
        if(self.first==None and other.first==None): return True
        a = self.first
        b = other.first
        while(a.hasNext() and b.hasNext()):
            if(a.getData()!=b.getData()): return False
            a = a.getNext()
            b = b.getNext()

        #we want to make sure the final two elements are
        if(a==None or b==None): return False #there is a length mismatch.
        elif(a.getData()==b.getData()): return True #have to check the last element
        else: return False #this should only occur when a!=b.
            

    # Add some data at the head of a doubly-linked list This should
    # take O(1) time
    #   2 points
    def add(self, data):
        #this will set the new data as the head and link the previoushead back to the new head.
        previousHead = self.first
        self.first = DoubleLink(data,None,previousHead)
        if(previousHead != None): previousHead.setPrev(self.first)
        if(self.first.getData() != data or self.first.getNext() != previousHead): raise Postcondition

    # Remove some piece of data from the list. Compare for equality of
    # data using ==
    #   2 points
    def remove(self,data):
        d = self.first
        isFound = False
        while(not isFound):
            if(d.getData() == data): isFound = True
            elif(not d.hasNext()): raise NoSuchElementException
            else: d = d.getNext()
        #once the element is found, it will be eliminated by referencing the next and previous elements instead.
        print("found element: "+str(d))
        if(d.hasNext()):
            d.getNext().setPrev(d.getPrev())
        if(d.hasPrev()):
            d.getPrev().setNext(d.getNext())
        else:
            self.first = d.getNext()
    # Check whether the list contains `data`
    #   2 points
    def contains(self, data):
        d = self.first
        isFound= False
        if(self.first==None):return self.first==data #to handle nones
        while(not isFound):
            if(d.getData()==data):return True
            elif(not d.hasNext()): return False #we have iterated through th elist
            else: d=d.getNext()

    # Reverse this linked-list in place. After a call to reverse, the
    # last element of the list should become the first, etc...
    #   2 points

    def reverse(self):
        reverseList = DLList()
        i = 0
        while(i<self.size()):
            reverseList.add(self.getIth(i))
            i+=1
        print(self.toArray())
        print(reverseList.toArray())
        self.first=reverseList.first
        print(self.toArray())
        if(self.toArray()!=reverseList.toArray()): raise Postcondition
        return self
    
   # Convert the elements of this list to an array
    #  2 points
    
    def toArray(self):
        def toArrayHelper(a,e):
            a.append(e.getData())
            if(e.hasNext()):
                toArrayHelper(a,e.getNext())

        arr = []
        d=self.first
        if(self.first==None): return arr
        toArrayHelper(arr,d)
        return arr
    # Get the `i`th element of the list
    # Precondition: i < self.size()
    # Otherwise, raise NoSuchElementException
    #  2 points
    def getIth(self, i):
        if(i>=self.size()): raise NoSuchElementException
        d = self.first
        c = 0
        while(c<i):
            d = d.getNext()
            c+=1
        return d.getData()
