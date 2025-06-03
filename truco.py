import tkinter as tk  # Biblioteca para criar interface gráfica
from tkinter import messagebox  # Caixa de mensagens para mostrar resultados
import random  # Para embaralhar e sortear cartas

# Hierarquia de força das cartas no Truco Mineiro com manilhas fixas
HIERARQUIA = [
    '4♣',  # Manilha mais forte
    '7♥',
    'A♠',
    '7♦',
    '3♠', '3♥', '3♦', '3♣',
    '2♠', '2♥', '2♦', '2♣',
    'A♦', 'A♥', 'A♣',
    'K♠', 'K♥', 'K♦', 'K♣',
    'J♠', 'J♥', 'J♦', 'J♣',
    'Q♠', 'Q♥', 'Q♦', 'Q♣',
    '7♠', '7♣',
    '6♠', '6♥', '6♦', '6♣',
    '5♠', '5♥', '5♦', '5♣',
    '4♠', '4♥', '4♦'  # As demais cartas
]

# Naipes disponíveis no jogo
NAIPES = ['♠', '♥', '♦', '♣']

# Valores usados para formar as cartas (ordem tradicional)
VALORES = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']

# Função para gerar o baralho completo (40 cartas do truco)
def gerar_baralho():
    return [f"{v}{n}" for v in VALORES for n in NAIPES]

# Função que distribui 3 cartas para cada jogador
def distribuir_cartas():
    baralho = gerar_baralho()
    random.shuffle(baralho)  # Embaralha o baralho
    return baralho[:3], baralho[3:6]  # 3 primeiras para o jogador, 3 seguintes para o computador

# Classe principal da interface do jogo
class TrucoMineiroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Truco Mineiro - Versão Clássica")

        # Variáveis do estado do jogo
        self.jogador_cartas = []
        self.computador_cartas = []
        self.rodadas_jogadas = 0
        self.pontos_jogador = 0
        self.pontos_computador = 0

        # Frame que contém as cartas do jogador
        self.frame_cartas = tk.Frame(self.root)
        self.frame_cartas.pack(pady=10)

        # Label para mostrar o status da partida
        self.label_status = tk.Label(self.root, text="Truco Mineiro - Jogue sua carta", font=('Arial', 14))
        self.label_status.pack()

        # Criação dos botões das 3 cartas
        self.cartas_labels = []
        for i in range(3):
            lbl = tk.Button(
                self.frame_cartas,
                text="?",
                font=('Arial', 18),
                width=4,
                command=lambda i=i: self.jogar_carta(i)
            )
            lbl.grid(row=0, column=i, padx=10)
            self.cartas_labels.append(lbl)

        # Botão para começar nova rodada
        self.btn_nova_rodada = tk.Button(self.root, text="Nova Rodada", command=self.nova_rodada)
        self.btn_nova_rodada.pack(pady=10)

        # Inicia a primeira rodada
        self.nova_rodada()

    # Função que reinicia uma rodada (nova mão)
    def nova_rodada(self):
        self.rodadas_jogadas = 0
        self.pontos_jogador = 0
        self.pontos_computador = 0

        # Distribui cartas para ambos os jogadores
        self.jogador_cartas, self.computador_cartas = distribuir_cartas()

        # Atualiza os botões das cartas do jogador
        for i, carta in enumerate(self.jogador_cartas):
            self.cartas_labels[i]['text'] = carta
            self.cartas_labels[i]['state'] = 'normal'

        self.label_status['text'] = "Truco Mineiro - Jogue sua carta"

    # Função chamada quando o jogador escolhe uma carta
    def jogar_carta(self, idx):
        carta_jogador = self.jogador_cartas[idx]
        carta_computador = random.choice(self.computador_cartas)  # CPU escolhe carta aleatória
        self.computador_cartas.remove(carta_computador)  # Remove carta usada pelo computador

        # Compara as cartas jogadas
        resultado = self.comparar_cartas(carta_jogador, carta_computador)

        # Atualiza pontuação de acordo com o resultado
        if "você" in resultado.lower():
            self.pontos_jogador += 1
        elif "computador" in resultado.lower():
            self.pontos_computador += 1

        # Exibe resultado da rodada
        messagebox.showinfo("Resultado da Rodada",
                            f"Você jogou: {carta_jogador}\n"
                            f"Computador jogou: {carta_computador}\n\n"
                            f"{resultado}")

        # Desabilita o botão da carta usada
        self.cartas_labels[idx]['state'] = 'disabled'
        self.rodadas_jogadas += 1

        # Finaliza a partida após 3 jogadas
        if self.rodadas_jogadas == 3:
            self.encerrar_partida()

    # Função que exibe o placar final após 3 jogadas
    def encerrar_partida(self):
        if self.pontos_jogador > self.pontos_computador:
            resultado = "Você venceu a partida!"
        elif self.pontos_jogador < self.pontos_computador:
            resultado = "O computador venceu a partida!"
        else:
            resultado = "A partida terminou empatada!"

        # Exibe resultado final com pontuação
        messagebox.showinfo("Fim da Partida",
                            f"Pontuação Final:\n"
                            f"Você: {self.pontos_jogador} ponto(s)\n"
                            f"Computador: {self.pontos_computador} ponto(s)\n\n"
                            f"{resultado}")
        self.btn_nova_rodada['state'] = 'normal'

    # Função que compara a força das cartas com base na hierarquia
    def comparar_cartas(self, carta1, carta2):
        valor1 = HIERARQUIA.index(carta1) if carta1 in HIERARQUIA else -1
        valor2 = HIERARQUIA.index(carta2) if carta2 in HIERARQUIA else -1
        if valor1 < valor2:
            return "Você venceu esta rodada!"
        elif valor1 > valor2:
            return "O computador venceu esta rodada."
        else:
            return "Empate."

# Execução principal da interface
if __name__ == "__main__":
    root = tk.Tk()
    app = TrucoMineiroGUI(root)
    root.mainloop()
