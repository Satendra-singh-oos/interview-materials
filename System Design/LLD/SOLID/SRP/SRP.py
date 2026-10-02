# Single Responsibility Principle OR Sepration of concern 
# if you have a aclasss that clas should jave its own primpriy responsiblity and it should not take other reposnbil;ity
# you dont want to overload your object with to many rspobvlity antipatater ->god obbjject its bad

class Journal:
    def __init__(self):
        self.entries=[]
        self.count=0
        
    def add_entry(self,text):
        self.count+=1
        self.entries.append(f'{self.count}:{text}')
        
    def remove_entry(self,pos):
        self.count-=1
        del self.entries[pos]

    def __str__(self):
        return '\n'.join(self.entries)
    
    # this break single responsibility
    # def save(self,filename):
    #     file=open(filename,'w')
    #     file.write(str(self))
    #     file.close()
    
    # def load(self,filename):
    #     pass
    
    # def load_from_web(self,uri ):
    #         pass
    

class JournalManger:
    @staticmethod
    def save(journal,filename):
        file=open(filename,'w')
        file.write(str(journal))
        file.close()
    @staticmethod
    def load(journal,filename):
        pass

    @staticmethod
    def load_from_web(journal,uri ):
            pass
        
        
    
    
j = Journal()
j.add_entry("I am not happy today :( ")
j.add_entry("I created a bug today")

print(f'Journal entries:\n{j}')  

file = r'./journal.txt'

JournalManger.save(j,file)

with open(file) as fh:
    print(fh.read())