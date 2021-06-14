class Token:

  def __init__ (self, num, name, line):
    self.token_num = num
    self.token_line = line 
    self.token_name = name
  
  def __str__(self):
    return self.token_name