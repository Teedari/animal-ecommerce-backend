
if __name__ == '__main__':
  print('hello world')
  def f(x, l=[]):
    for i in range(x):
      l.append(i * i)
    print(l)
    # i = i + ', Welcome to Turing'
  f(2)   
  f(3, [3,2,1])   
  f(3)   
  class Developer(object):
    def __init__(self, skills) -> None:
      self.skills = skills

    def __add__(self, other):
      skills = self.skills + other.skills
      return Developer(skills)
    
    def __str__(self) -> str:
      return "Skills"
    
    
  A = Developer('NodeJs')
  B = Developer('Python')
  
  print(A + B)
  