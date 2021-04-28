import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-n' ,'--name' ,required = True ,help ='Name of the person')
args = vars(ap.parse_args()) #vars returns the __dict__ attribute of the argument passsed. In this case it returns the dict of key-value pair where key is the argument
#and value is the value which pass through the command prompt.

print(f"hi there {args['name']}, it is nice to meet you")
