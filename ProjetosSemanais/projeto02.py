import keyboard
import threading
import time

dfa = {}
esc_pressionado = False

def verificar_esc():
    global esc_pressionado
    while not esc_pressionado:
        if keyboard.is_pressed('esc'):
            esc_pressionado = True
            print("\nESC pressionado. Saindo do modo de entrada...")
            break
        time.sleep(0.1)  # Pequena pausa para não sobrecarregar a CPU

# Inicia a thread para verificar a tecla ESC
thread_esc = threading.Thread(target=verificar_esc)
thread_esc.daemon = True  # Permite que o programa termine mesmo se a thread estiver rodando
thread_esc.start()

print("Digite as transições do DFA (q0 0 q1) - ESC para sair:")

while not esc_pressionado:
    try:
        print("Transicao (ou pressione ESC para sair): ", end='', flush=True)
        transicao = input()
        
        if esc_pressionado:
            break
            
        if transicao:
            try:
                estado_atual, entrada, proximo_estado = transicao.split()
                if estado_atual not in dfa:
                    dfa[estado_atual] = {}
                dfa[estado_atual][entrada] = proximo_estado
                print(f"Transição adicionada: {estado_atual} --({entrada})--> {proximo_estado}")
            except ValueError:
                print("Formato inválido. Use: estado_atual simbolo proximo_estado")
    except EOFError:
        # Captura EOFError (Ctrl+D no Linux/macOS, Ctrl+Z no Windows)
        break
    except KeyboardInterrupt:
        # Captura Ctrl+C
        print("\nOperação cancelada pelo usuário.")
        break

if not dfa:
    print("Nenhuma transição definida. Encerrando programa.")
    exit()

estado_inicial = input("Estado inicial: ")
estados_finais = input("Estados finais (separados por espaço, ex: q0 q1 q3): ")

lista_finais = estados_finais.split()

w = input("Digite a string de entrada: ")

estado_atual = estado_inicial
caminho = f"δ({estado_inicial}, ε) = {estado_inicial}"
print(caminho)

for i, simbolo in enumerate(w):
    if estado_atual in dfa and simbolo in dfa[estado_atual]:
        proximo_estado = dfa[estado_atual][simbolo]
        # Constrói corretamente a string de processamento
        substring = w[:i] if i > 0 else 'ε'
        caminho = f"δ({estado_inicial}, {w[:i+1]}) = δ(δ({estado_inicial}, {substring}), {simbolo}) = δ({estado_atual}, {simbolo}) = {proximo_estado}"
        print(caminho)
        estado_atual = proximo_estado
    else:
        print(f"Transição inválida para: {estado_atual}, {simbolo}")
        estado_atual = None
        break

if estado_atual:
    if estado_atual in lista_finais:
        print("✅ Aceito")
    else:
        print("❌ Rejeitado")
else:
    print("❌ Rejeitado")