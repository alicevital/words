def avaliar_tentativa(tentativa: str, resposta: str):
    resultado = ["absent"] * len(tentativa)
    resposta_lista = list(resposta)

    for i in range(len(tentativa)):
        if tentativa[i] == resposta[i]:
            resultado[i] = "correct"
            resposta_lista[i] = None

    for i in range(len(tentativa)):
        if resultado[i] == "correct":
            continue
        if tentativa[i] in resposta_lista:
            resultado[i] = "present"
            resposta_lista[resposta_lista.index(tentativa[i])] = None

    return resultado