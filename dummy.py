
from curses.ascii import isdigit


if __name__ == '__main__':
  
  
  print('hello world')
  query = 'name:godfred;age:12;house:22;'

  def getParams(queryStr):
    param_list = [*map(lambda x: x.split(':'), queryStr.split(';'))]
    params = {}
    for param in param_list:
        if len(param) == 2:
          params[param[0]] = param[1]
    return params
  
  for param in getParams(query).keys():
    print(param)
  