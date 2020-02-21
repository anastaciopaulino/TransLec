import os, googletrans
from sys import argv
import translec as tr
from time import sleep

def main2():
    # -*- Color in your shell
    os.system('''
white="\033[1;37m"                                          
grey="\033[0;37m"                                           
purple="\033[0;35m"                                         
red="\033[1;31m"                                            
green="\033[1;32m"                                          
yellow="\033[1;33m"                                         
purple="\033[0;35m"                                         
cyan="\033[0;36m"                                           
cafe="\033[0;33m"                                           
fiuscha="\033[0;35m"                                        
blue="\033[1;34m"                                           
nc="\e[0m"                                                  

printf "$green
    ╔═══════════════════════════════════════════════════════════════════════════════╗
════╝

████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗     ███████╗ ██████╗
╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔════╝██╔════╝
   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     █████╗  ██║     
   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══╝  ██║     
   ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗███████╗╚██████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝


    ╔═══════════════════════════════════════════════════════════════════════════════╗
════╝"
''')
def main():
    # -*- Color in your shell
    os.system('''
white="\033[1;37m"                                          
grey="\033[0;37m"                                           
purple="\033[0;35m"                                         
red="\033[1;31m"                                            
green="\033[1;32m"                                          
yellow="\033[1;33m"                                         
purple="\033[0;35m"                                         
cyan="\033[0;36m"                                           
cafe="\033[0;33m"                                           
fiuscha="\033[0;35m"                                        
blue="\033[1;34m"                                           
nc="\e[0m"                                                  

printf "$green
    ╔═══════════════════════════════════════════════════════════════════════════════╗
════╝

████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗     ███████╗ ██████╗
╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔════╝██╔════╝
   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     █████╗  ██║     
   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══╝  ██║     
   ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗███████╗╚██████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝


    ╔═══════════════════════════════════════════════════════════════════════════════╗
════╝
    ╔══════════════════════════╗╔═══════════════════════════════════════════════════╗
    ║ ${yellow}⟫${red}⟫${white}⟫${green} Usage                ║║ ${yellow}⟫${red}⟫${white}⟫${green} Information                                   ║                       
    ║                          ║║                                                   ║                      
    ║     [+] --help | -h      ║║  [ List All Information                    ]      ║
    ║     [+] --descript | -d  ║║  [ Set the output language                 ]      ║
    ║     [+] --all            ║║  [ Translate all files                     ]      ║
    ║     [+] -l               ║║  [ Listar todos os arquivos (str/vtt)      ]      ║ 
    ║     [+] -f               ║║  [ Choose a text file                      ]      ║                      
    ╚══════════════════════════╝╚═══════════════════════════════════════════════════╝
════╗
    ╚═══════════════════════════════════════════════════════════════════════════════╝                                                            

"
''')

def _exec():
    main()
    try:
         # -*- -l -*-
        if(ls):
            os.system("clear")
            main2()
            tr.Path()
            tr.Path.printlist()

        # -*- --Descript -*-
        if(("--descript" in query) and ("--all" in query)):
            tr.Path()
            for file in tr.files:
                tr.Trans(file, query["--descript"])
        # -*- --all -*-
        if(("--all" not in query) and ("--descript" in query)):
            while True:
                phrase = str(input("Enter the phrase: "))
                if(phrase == "exit"):
                    print("Bay, Bay ...")
                    sleep(.5)
                    break
                transp = tr.Transp(phrase, query["--descript"])
    except:
        os.system('''
        red="\033[1;31m" 
printf "\n$red[!]$red Aconteceu um erro não Programavel $red[!]\nPor favor acesse: https://github.com/anastaciopaulino/TransLec\n"''')
        sleep(.5)            
    else:
        pass
ls = False
command = argv[1:]
count = 0
ftxt = False
query = {}
for instrucion in command:
    if ("--descript" in instrucion) or ("-d" in instrucion):
        try:
            out = command[count+1]
            query["--descript"] = out
        except IndexError:
            print("Value for '--descript'")
    if ("-l" in instrucion):
        ls = True
    if("--all" in instrucion):
        query["--all"] = True
    if ("-f" in instrucion):
        try:
            ftxt = command[count+1]
            query["-f"] = ftxt
        except IndexError:
            print("Value for '-f'")
    count += 1     

_exec()