from Bitarray import *
# 导入哈希表
from GeneralHashFunctions.GeneralHashFunctions import *



def my_hash(words:list())->int:
    answer = 0
    my_bit_array = Bitarray(5000000)
    for word in words:
        elf = ELFHash(word) % 5000000
        dek = DEKHash(word) % 5000000
        djb = DJBHash(word) % 5000000
        fnv = FNVHash(word) % 5000000
        #elf = 1
        #dek = 1
        #djb = 1
        #fnv = 1
        # 验证是否都存在
        if my_bit_array.get(elf) == 1 and my_bit_array.get(dek) == 1  and my_bit_array.get(fnv) == 1 and my_bit_array.get(djb) == 1:
            continue
        else:
            answer += 1
            my_bit_array.set(elf)
            my_bit_array.set(dek)
            my_bit_array.set(djb)
            my_bit_array.set(fnv)
    return answer

# Test1: 女王去世

files = ["./Hashcheck/test1.txt","./Hashcheck/test2.txt","./Hashcheck/test3.txt","./Hashcheck/test4.txt"]
strings = ["the announcement of Her Majstery's death", "joint announcement of Permanent members of the United Nations Security Council", "Conan Doyle's The Five Orange Pips", "Conan Doyle's A Study in Scarlet"]

total = list()
for i in range(4):
    file = open(files[i], encoding="utf-8")
    content = file.read()
    file.close() 
    words_list = content.split()
    total += words_list
    words = set(words_list)
    length = my_hash(words_list)
    print("There are {0} words in the {1}.".format(len(words_list),strings[i]))
    print("There are {0} vocabularies in the {1}.".format(len(words),strings[i]))
    print("Our method calculates {0} words in the {1}.".format(length, strings[i]))
    print("There are {0} errors.".format(len(words) - length))

words = set(total)
length = my_hash(total)
print("There are {0} words in total pages.".format(len(total)))
print("There are {0} vocabularies in total pages.".format(len(words)))
print("Our method calculates {0} words in total pages.".format(length))
print("There are {0} errors.".format(len(words) - length))


# Tes