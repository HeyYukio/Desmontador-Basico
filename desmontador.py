# Henrique Yukio Murata

p1in = open('input.txt','r')  # abre o arquivo input.txt para leitura
p1out = open("compout.txt", "w")  # abre arquivo compout.txt para escrita

# convete de string em formato binario para hexadecimal

def Bin2Hex(binary):   

    switcher = {

        "0000": "0",
        "0001": "1",
        "0010": "2",
        "0011": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1010": "A",
        "1011": "B",
        "1100": "C",
        "1101": "D",
        "1110": "E",
        "1111": "F"
    }
    
    return switcher.get(binary, "Valor invalido")

# De acordo com os bits correpondentes ao codigo de op
# Extrai da memoria os bits referentes ao codigo de op e os bits referentes ao operando/endereco
# Atualiza o "ponteiro" i para proxima instrucao a ser lida
# Contem parte da logica de pre processamento e extracao dos dados/eventos, alem de atualizar o ponteiro

def ExtractMem (memory,i):  # note que, se tratando da memoria, i correponde nao mais a um ponteiro de caractere hexa, mas sim o endereco decimal da memoria 

    if Bin2Hex(memory[i][0:4]) == "3" or  Bin2Hex(memory[i][0:4]) == "B" or Bin2Hex(memory[i][0:4]) == "C": # se for uma instrução de 1 byte

        co = memory[i][0:4] 
        operando = memory[i][4:8]
        return co, operando , i+1 ,0
    
    if Bin2Hex(memory[i][0:4]) == "D" or  Bin2Hex(memory[i][0:4]) == "E" or Bin2Hex(memory[i][0:4]) == "F": # excecao para operacoes disponiveis

        co = "disp"                                     # indica que o codigo de op corresponde a uma op disponivel  
        operando = "disp"
        return co, operando , i+1,0                     # retorna indicacao e passa ponteiro para proximo endereco da memoria
    
    else:                                               # se for uma instrucao de 2 bytes 

        if i == len(memory)-1:                          # excecao para final da seccao da memoria
            co = "final"                                # guarda na string a indicacao de final da secao da memoria
            operando = "final"
            return co, operando , i+2,1 ,1              # retorna indicacao e atualiza ponteiro

        co = memory[i][0:4]                             # extracao em condicoes "normais" para isntrucoes de 2 bytes
        operando = memory[i][4:8]+memory[i+1][0:8]
        return co, operando , i+2 ,0

# De acordo com o caractere correpondente ao co
# Extrai do .txt o caractere referentea ao co e os caracteres referentes ao operando/endereco
# Atualiza o "ponteiro" i para proxima instrucao a ser lida
# Contem parte da logica de pre processamento e extracao dos dados/eventos, alem de atualizar ponteiro

def ExtractHex (line,nextline,i):

    if line[i] == "3" or  line[i] == "B" or line[i] == "C":    # se for uma instrucao de 1 byte

        co = line[i] 
        operando = line[i+1]
        return co, operando , i+3, 0
    
    if line[i] == "D" or  line[i] == "E" or line[i] == "F":     # excecao para operacoes "disponiveis"
                                                                
        co = "disp"                                             # indica que o co corresponde a uma op disponivel  
        operando = "disp"
        return co, operando , i+3, 0                            # retorna indicacao e passa ponteiro para proximo byte

    else:                                                       # se for uma instrucao de 2 bytes

        if nextline == "" and  i == len(line)-5:                # excecao para final do arquivo
            co = "final"                                        # guarda na string a indicacao de final de arquivo 
            operando = "final"
            return co, operando , i+6, 1                        # retorna indicacao e atualiza ponteiro

        if i == len(line)-5:                                    # excecao para final de linha     
            co = line[48]                                       # guarda caracetere hexa referente ao mnemonico
            operando = line[49]+nextline[9]+nextline[10]        # guarda caracteres hexa referentes ao operando/endereco
            return co, operando , i+6, 1

        co = line[i]                                            # extracao em condicoes "normais" para isntrucoes de 2 bytes
        operando = line[i+1]+line[i+3:i+5]
        return co, operando , i+6, 0

# Devolve string contendo mnemonico (em formato simbolico) + operando/endereço (em formato hexadecimal) 
# contem parte da tabela de eventos (ORIGiN e END foram indentificados nas funcoes Memoria e Txt)

def Decider (co, operando):

    if co == "0":
        str = "JP " + operando + "\n"
    if co == "1":
        str = "JZ " + operando + "\n"
    if co == "2":
        str = "JN " + operando + "\n"
    if co == "3":
        str = "CN " + operando + "\n"
    if co == "4":
        str = "+ " + operando + "\n"
    if co == "5":
        str = "- " + operando + "\n"
    if co == "6":
        str = "* " + operando + "\n"
    if co == "7":
        str = "/ " + operando + "\n"
    if co == "8":
        str = "LD " + operando + "\n"
    if co == "9":
        str = "MM " + operando + "\n"
    if co == "A":
        str = "SC " + operando + "\n"
    if co == "B":
        str = "OS " + operando + "\n"
    if co == "C":
        str = "IO " + operando + "\n"

    return str

# Se a entrada for conteudo da memoria

def Memoria(input_type):

    bin = "10000000001100101001000000110111100100000011010010010000001101101000000000110111010100000011010100010000001100001000000000110111010000000011001010010000001101111000000000110100010000000011001110010000001101000100000000110110100100000011011000000000000110001100000000110000000000010000001000000000000001000000000000000000"
    memory=[]
    limit = len(bin)//8
    i = 0
    count = 1

    # carregamento "manual" dos bits na memoria
    # cada endereco da memoria corresponde a um conjunto de 8 bits (1 byte)
    # exceto o ultimo endereco necessario que pode conter menos de 8 bits 

    while count <= limit:
        memory.append(bin[i:i+8])
        i=i+8
        count = count+1
    memory.append(bin[i:])          
    
    addr = "A1O"                             # guarda endereço de origem na string addr    
    str = "@ " + addr + "\n"                 # string para armazenar o que sera printado
    p1out.write(str)                         # printa mnemonico + endereço de origem

    overflow = 0        # seta overflow como 0

    i = 0               # seta ponteiro de endereco da memoria para 0

    # loop para extracao de eventos da memoria, consulta a tabela e print no .txt de saida 

    while i < (len(memory)-2):
        co, operando , i , overflow = ExtractMem (memory, i)
        if co != "disp" and co != "final":
            co = Bin2Hex(co)
            if len(operando) == 4:
                operando = Bin2Hex(operando)
            if len(operando) == 12:
                operando = Bin2Hex(operando[0:4]) + Bin2Hex(operando[4:8]) + Bin2Hex(operando[8:12])
            str = Decider (co, operando)
            p1out.write(str)
    
    str = "# " + addr + "\n"                   # guarda sring que compoem instrucao de END
    p1out.write(str)                           # printa a strign no arquivo .txt de saida

# Se a entrada for conteudo do .txt

def Txt(input_type):

    lines = p1in.readlines()                   # Le linhas do arquivo .txt e guarda numa lista de strings
                                               # em que cada linha corresponde a um string
    for i in range (0,len(lines)):             # Retira caracteres \n das strings
        lines[i] = lines[i].replace ("\n", "") 

    addr = lines[0][4]+lines[0][6:8]           # guarda endereço de origem na string addr
    str = "@ " + addr + "\n"                   # string para armazenar o que sera printado
    p1out.write(str)                           # printa endereço de mnemonico + endereço de origem no arquivo .txt de saida

    overflow = 0

    for count in range (0,len(lines)-1):       
           
        i=9                                   # seta ponteiro para primeiro caractere na primeira linha correpondente a instrucao
        if overflow == 1:                     # Se o caractere hexa no fim da linha nao for suficiente p caracterizar instrucao
            i=12                              # atauliza ponteiro para caractere inicial da proxima linha

        # loop para extracao de eventos do .txt de entrada, consulta a tabela e print no .txt de saida 

        while i < (len(lines[count])-3) : 
            co, operando , i, overflow = ExtractHex (lines[count],lines[count+1],i)  
            if co != "disp" and co != "final":
                str = Decider (co, operando)
                p1out.write(str)
    
    str = "# " + addr + "\n"                # guarda sring que compoem instrucao de END
    p1out.write(str)                        # printa a strign no arquivo .txt de saida

# Main
# Escolha do tipo de entrada

input_type= input("1 - Acessar memoria\n2 - Ler p1in.txt\nEscolha: ")

if input_type == "1":
    Memoria(input_type)
elif input_type == "2":
    Txt(input_type)
else: 
    print ("Entrada nao definida")
