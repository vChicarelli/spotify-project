def get_input(input_text, input_list):
    while True:
        try:
            number = int(input(f"{input_text}:"))
            if 1 <= number <= len(input_list):
                return input_list[number-1]
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")