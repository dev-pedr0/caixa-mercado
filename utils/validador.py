def validar_numero(msg):
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Digite apenas números.")