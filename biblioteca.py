from InquirerPy import prompt
from rich import print
import json
from time import sleep


class Livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.titulo} | {self.autor} | {self.ano} | {status}"


class Biblioteca:
    def __init__(self):
        self.livros = []
        self.carregar()

    def salvar(self):
        dados = []

        for livro in self.livros:
            dados.append({
                "titulo": livro.titulo,
                "autor": livro.autor,
                "ano": livro.ano,
                "disponivel": livro.disponivel
            })

        with open("livros.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    
    def carregar(self):
        try:
            with open("livros.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                livro = Livro(
                    item["titulo"],
                    item["autor"],
                    item["ano"]
                )

                livro.disponivel = item["disponivel"]
                self.livros.append(livro)

        except FileNotFoundError:
            pass

    def adicionar_livro(self):
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano = input("Ano: ")

        livro = Livro(titulo, autor, ano)
        self.livros.append(livro)

        self.salvar()

        print(f"\n[green]Livro '{titulo}' adicionado com sucesso![/green]")

    def listar_livros(self):
        if not self.livros:
            print("[yellow]Nenhum livro cadastrado.[/yellow]")
            return

        print("\n[cyan]=== LIVROS CADASTRADOS ===[/cyan]\n")

        for i, livro in enumerate(self.livros, start=1):
            print(f"{i}. {livro}")

    def buscar_livro(self):
        titulo = input("Digite o título: ")

        for livro in self.livros:
            if livro.titulo.lower() == titulo.lower():
                print(f"\n[green]Encontrado:[/green] {livro}")
                return livro

        print("[red]Livro não encontrado.[/red]")
        return None

    def emprestar_livro(self):
        titulo = input("Livro para empréstimo: ")

        for livro in self.livros:
            if livro.titulo.lower() == titulo.lower():

                if not livro.disponivel:
                    print("[red]Livro já está emprestado.[/red]")
                    return

                livro.disponivel = False
                self.salvar()
                print("[green]Livro emprestado com sucesso![/green]")
                return

        print("[red]Livro não encontrado.[/red]")

    def devolver_livro(self):
        titulo = input("\n[blue]Livro para devolução: [/]")

        for livro in self.livros:
            if livro.titulo.lower() == titulo.lower():

                if livro.disponivel:
                    print("[yellow]Este livro já está disponível.[/yellow]")
                    return

                livro.disponivel = True

                self.salvar()

                print("[green]Livro devolvido com sucesso![/green]")
                return

        print("[red]Livro não encontrado.[/red]")


class Main:
    def __init__(self):
        self.biblioteca = Biblioteca()

    def executar(self):

        while True:

            menu = [
                {
                    "type": "list",
                    "name": "opcao",
                    "message": "Selecione uma opção:",
                    "choices": [
                        "Adicionar Livro",
                        "Listar Livros",
                        "Buscar Livro",
                        "Emprestar Livro",
                        "Devolver Livro",
                        "Sair"
                    ]
                }
            ]

            resultado = prompt(menu)
            opcao = resultado["opcao"]

            if opcao == "Adicionar Livro":
                self.biblioteca.adicionar_livro()

            elif opcao == "Listar Livros":
                self.biblioteca.listar_livros()

            elif opcao == "Buscar Livro":
                self.biblioteca.buscar_livro()

            elif opcao == "Emprestar Livro":
                self.biblioteca.emprestar_livro()

            elif opcao == "Devolver Livro":
                self.biblioteca.devolver_livro()

            elif opcao == "Sair":
                sleep(0.8)
                print("\n[red]Obrigado por testar![/red]")
                break

if __name__ == "__main__":
    app = Main()
    app.executar()