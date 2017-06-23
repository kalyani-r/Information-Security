#!/usr/bin/evn python

"""simple_unix_pwd_cracker.py: a simple unix passwork cracker."""

#python3 simple_unix_pwd_cracker.py -t 1 -i pwd_hash_task1.txt
#python3 simple_unix_pwd_cracker.py -t 2 -i pwd_hash_task2.txt
#python3 simple_unix_pwd_cracker.py -t 3 -i pwd_hash_task3.txt

import crypt
import getopt
import pdb
import sys
import time
from itertools import product
from string import ascii_letters

def read_file(filepath):
    file = open(filepath, 'r')
    return file.readlines()

def get_dictionary_list(path):
    orig_dict = []
    lines = read_file(path)
    for line in lines:
        line = line.rstrip('\n')
        orig_dict.append(line)
    
    return orig_dict

def get_salt_list():
    salts = []
    for combo in product(ascii_letters, repeat=2):
        salts.append(''.join(combo))
    return salts

def concat_dict_search(path,salt,pwd_hash):
    orig_dict = get_dictionary_list(path)
    
    #print("len orig_dict: ", len(orig_dict))
    i = 0
    
    for first_word in orig_dict:
        for second_word in orig_dict:
            if first_word < second_word: #only include second words that are after first words
                test_hash = crypt.crypt(first_word+second_word,salt)
                if pwd_hash == test_hash:
                    print("Plaintext value: ", first_word+second_word)
                    return True
                    break
                i+=1
                if i%100000==0: 
                    print("{:,}".format(i), "tries")#, " | ", first_word+second_word+"                                     ") 
                    print("\033[F\033[F") #sys.stdout.write
    
    return False    

def search_hash_dictionary(path,salt,pwd_hash):
    print("Hash: ", pwd_hash, " | Salt: ", salt)
    
    lines = get_dictionary_list(path)
    dic_size = len(lines)
    print("Dictionary size: ", dic_size)
    i = 0
    for line in lines:
        line = line.rstrip('\n')
        test_hash = crypt.crypt(line,salt)
        if pwd_hash == test_hash:
            print("Plaintext value: ", line)
            return True
            break
    print('\033[F\033[F\033[F')
    
    return False

def pwd_crack_task1(salt, pwd_hash):
    """Please complete this function:
         1) find the word (password) in the given dictionary such that its hash is
            matched to the given hash
         2) print out the word (password) in plaintext
    """
    start_time = time.time()
    search_hash_dictionary("web2",salt,pwd_hash)
    time_taken = time.time()-start_time
    print("Seconds required: ", time_taken)
    
def pwd_crack_task2(pwd_hash):
    """Please complete this function:
         1) find the word (password) in the given dictionary such that its hash is
            matched to the given hash
         2) print out the word (password) in plaintext
    """
    start_time = time.time()
    for salt in get_salt_list():
        if search_hash_dictionary("web2",salt,''.join([salt,pwd_hash])):
            print("Found, exiting...")
            break
    time_taken = time.time()-start_time
    print("Seconds required: ", time_taken)
    

def pwd_crack_task3(salt, pwd_hash):
    """Please complete this function:
         1) find the concatenation of two words (password) in the given dictionary such that its hash is
            matched to the given hash
         2) print out the word (password) in plaintext
    """
    start_time = time.time()
    concat_dict_search("web2",salt,pwd_hash)
    time_taken = time.time()-start_time
    print("Seconds required: ", time_taken)
    
def main(argv):
	input_file = ''
	task = ''
	try:
		opts, args = getopt.getopt(argv,"hi:t:",["infile=","task="])
	except getopt.GetoptError:
		print('python3 simple_unix_pwd_cracker.py -t <task number> -i <input_file>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('python3 simple_unix_pwd_cracker.py -t <task number> -i <input_file>')
			sys.exit()
		elif opt in ("-i", "--infile"):
			input_file = arg
		elif opt in ("-t", "--task"):
			task = arg
	print("Input file: ", input_file)
	print("Task: ", task)

	lines = read_file(input_file);
	if(task == '1'):
		salt = lines[0].rstrip('\n')
		pwd_hash = lines[1].rstrip('\n')
		pwd_crack_task1(salt, pwd_hash)
	elif(task == '2'):
		pwd_hash = lines[0].rstrip('\n')
		pwd_crack_task2(pwd_hash)
	elif(task == '3'):
		salt = lines[0].rstrip('\n')
		pwd_hash = lines[1].rstrip('\n')
		pwd_crack_task3(salt, pwd_hash)

if __name__ == '__main__':
	main(sys.argv[1:])