import argparse

def create_args_parser():
    parser = argparse.ArgumentParser(description='Enterprise usernames wordlist generator')
    
    maingroup = parser.add_argument_group(title='required')
    maingroup.add_argument('-t', nargs='?', help='target, ex.: http://10.10.10.99', metavar='url', required=True)
    maingroup.add_argument('-d', nargs='?', help='admin panel dir, default: /admin/login', metavar='dir', default='/admin/login')
    
    usernames_group = maingroup.add_mutually_exclusive_group(required=True)
    usernames_group.add_argument('-u', nargs='?', help='username', metavar='username')
    usernames_group.add_argument('-U', nargs='?', help='usernames wordlist file', metavar='filename')
    
    passwords_group = maingroup.add_mutually_exclusive_group(required=True)
    passwords_group.add_argument('-p', nargs='?', help='password', metavar='password')
    passwords_group.add_argument('-P', nargs='?', help='passwords wordlist file', metavar='filename')
    
    parser.add_argument('-s', nargs='?', help='sleep time after blocking IP', metavar='time in seconds', default=60)

    parser.add_argument('-v', action='version', version='%(prog)s 1.0.0')
    
    return parser
