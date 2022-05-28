grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
grades = reversed(grades)
grades = {l:i for i,l in enumerate(grades)}

class Letter():
    
    def __init__(self, letter):
        self.letter = letter
        
    def __eq__(self, other):
        assert isinstance(other, Letter)
        
        return self.letter == other.letter
    
    def __lt__(self, other):
        assert isinstance(other, Letter)
        
        return grades[self.letter] < grades[other.letter]
    
    def __gt__(self, other):
        assert isinstance(other, Letter)
        
        return grades[self.letter] > grades[other.letter]
        
    def __le__(self, other):
        assert isinstance(other, Letter)
        
        return grades[self.letter] <= grades[other.letter]
    
    def __lt__(self, other):
        assert isinstance(other, Letter)
        
        return grades[self.letter] >= grades[other.letter]
    
    def __repr__(self):
        return self.letter
        