import sys

class No():
    def __init__(self, estado, pai, acao):
        self.estado = estado
        self.pai = pai
        self.acao = acao


class FronteiraPilha():
    def __init__(self):
        self.fronteira = []

    def adicionar(self, no):
        self.fronteira.append(no)

    def contem_estado(self, estado):
        return any(no.estado == estado for no in self.fronteira)

    def vazia(self):
        return len(self.fronteira) == 0

    def remover(self):
        if self.vazia():
            raise Exception("fronteira vazia")
        else:
            no = self.fronteira[-1]
            self.fronteira = self.fronteira[:-1]
            return no


class FronteiraFila(FronteiraPilha):

    def remover(self):
        if self.vazia():
            raise Exception("fronteira vazia")
        else:
            no = self.fronteira[0]
            self.fronteira = self.fronteira[1:]
            return no

class Labirinto():

    def __init__(self, nome_arquivo):

        # Ler arquivo e definir altura e largura do labirinto
        with open(nome_arquivo) as f:
            conteudo = f.read()

        # Validar início e objetivo
        if conteudo.count("A") != 1:
            raise Exception("o labirinto deve ter exatamente um ponto de início")
        if conteudo.count("B") != 1:
            raise Exception("o labirinto deve ter exatamente um ponto de objetivo")

        # Determinar altura e largura do labirinto
        conteudo = conteudo.splitlines()
        self.altura = len(conteudo)
        self.largura = max(len(linha) for linha in conteudo)

        # Manter controle das paredes
        self.paredes = []
        for i in range(self.altura):
            linha = []
            for j in range(self.largura):
                try:
                    if conteudo[i][j] == "A":
                        self.inicio = (i, j)
                        linha.append(False)
                    elif conteudo[i][j] == "B":
                        self.objetivo = (i, j)
                        linha.append(False)
                    elif conteudo[i][j] == " ":
                        linha.append(False)
                    else:
                        linha.append(True)
                except IndexError:
                    linha.append(False)
            self.paredes.append(linha)

        self.solucao = None


    def imprimir(self):
        solucao = self.solucao[1] if self.solucao is not None else None
        print()
        for i, linha in enumerate(self.paredes):
            for j, coluna in enumerate(linha):
                if coluna:
                    print("█", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.objetivo:
                    print("B", end="")
                elif solucao is not None and (i, j) in solucao:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def vizinhos(self, estado):
        linha, coluna = estado
        candidatos = [
            ("cima", (linha - 1, coluna)),
            ("baixo", (linha + 1, coluna)),
            ("esquerda", (linha, coluna - 1)),
            ("direita", (linha, coluna + 1))
        ]

        resultado = []
        for acao, (r, c) in candidatos:
            if 0 <= r < self.altura and 0 <= c < self.largura and not self.paredes[r][c]:
                resultado.append((acao, (r, c)))
        return resultado


    def resolver(self):
        """Encontra uma solução para o labirinto, se existir."""

        # Manter controle do número de estados explorados
        self.num_explorados = 0

        # Inicializar a fronteira apenas com a posição inicial
        inicio = No(estado=self.inicio, pai=None, acao=None)
        fronteira = FronteiraPilha()
        fronteira.adicionar(inicio)

        # Inicializar um conjunto vazio de explorados
        self.explorados = set()

        # Continuar em loop até encontrar a solução
        while True:

            # Se não houver mais nada na fronteira, então não há caminho
            if fronteira.vazia():
                raise Exception("sem solução")

            # Escolher um nó da fronteira
            no = fronteira.remover()
            self.num_explorados += 1

            # Se o nó é o objetivo, então temos uma solução
            if no.estado == self.objetivo:
                acoes = []
                celulas = []
                while no.pai is not None:
                    acoes.append(no.acao)
                    celulas.append(no.estado)
                    no = no.pai
                acoes.reverse()
                celulas.reverse()
                self.solucao = (acoes, celulas)
                return

            # Marcar o nó como explorado
            self.explorados.add(no.estado)

            # Adicionar vizinhos à fronteira
            for acao, estado in self.vizinhos(no.estado):
                if not fronteira.contem_estado(estado) and estado not in self.explorados:
                    filho = No(estado=estado, pai=no, acao=acao)
                    fronteira.adicionar(filho)


    def salvar_imagem(self, nome_arquivo, mostrar_solucao=True, mostrar_explorados=False):
        from PIL import Image, ImageDraw
        tamanho_celula = 50
        borda_celula = 2

        # Criar um canvas em branco
        img = Image.new(
            "RGBA",
            (self.largura * tamanho_celula, self.altura * tamanho_celula),
            "preto"
        )
        draw = ImageDraw.Draw(img)

        solucao = self.solucao[1] if self.solucao is not None else None
        for i, linha in enumerate(self.paredes):
            for j, coluna in enumerate(linha):

                # Paredes
                if coluna:
                    fill = (40, 40, 40)

                # Início
                elif (i, j) == self.inicio:
                    fill = (255, 0, 0)

                # Objetivo
                elif (i, j) == self.objetivo:
                    fill = (0, 171, 28)

                # Solução
                elif solucao is not None e mostrar_solucao e (i, j) na solucao:
                    fill = (220, 235, 113)

                # Explorados
                elif solucao é not None e mostrar_explorados e (i, j) em self.explorados:
                    fill = (212, 97, 85)

                # Célula vazia
                else:
                    fill = (237, 240, 252)

                # Desenhar célula
                draw.rectangle(
                    ([(j * tamanho_celula + borda_celula, i * tamanho_celula + borda_celula),
                      ((j + 1) * tamanho_celula - borda_celula, (i + 1) * tamanho_celula - borda_celula)]),
                    fill=fill
                )

        img.save(nome_arquivo)


if len(sys.argv) != 2:
    sys.exit("Uso: python labirinto.py labirinto.txt")

m = Labirinto(sys.argv[1])
print("Labirinto:")
m.imprimir()
print("Resolvendo...")
m.resolver()
print("Estados Explorados:", m.num_explorados)
print("Solução:")
m.imprimir()
m.salvar_imagem("labirinto.png", mostrar_explorados=True)
