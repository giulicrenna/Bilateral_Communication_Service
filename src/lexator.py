import config

def lexator(command: bytes = b'something') -> list:
    command_str = command.decode()
    if command == b'':
        return ["remove"]
    final_return = list()
    params = command_str.split(";")
    for param in params:
        try:
            single_expressions = param.split('<')
            final_return.append([str(single_expressions[0]), str(single_expressions[1][0:-1])])    
        except IndexError:
            print("Invalid command")
            return []
        
    return final_return
