import cv2

import numpy as np

video = cv2.VideoCapture('pedra-papel-tesoura.mp4') #Captura do Vídeo

if not video.isOpened():
    raise Exception("Vídeo não abriu") #Expection se o Vídeo não abrir

while True:

    
    ret, frame = video.read() #Ler o frame do vídeo

    foto = frame.copy() #Copio o frame para fazer outro retorno

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Filtro de HSV

    img = cv2.blur(img_hsv, (15, 15), 0)  #Blur

    lower_hsv_1 = np.array([0, 21, 5])  # Arrays para Montar Filtro HSV
    higher_hsv_1 = np.array([18, 200, 200])

    lower_hsv_2 = np.array([0, 1, 1])
    higher_hsv_2 = np.array([255, 150, 250])

    mask_1 = cv2.inRange(img, lower_hsv_1, higher_hsv_1)  # Máscara 1

    mask_2 = cv2.inRange(img, lower_hsv_2, higher_hsv_2)  # Máscara 2

    img_filtro = cv2.bitwise_or(mask_1, mask_2)  # Imagem filtrada (para calcular Massa do Objeto)

    contours, _ = cv2.findContours(img_filtro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Encontrar os Contornos da Imagem img_filtro

    cv2.drawContours(foto, contours, -1, [0, 157, 255], 3) #Desenhando os Contornos

    cont_1 = contours[1] #Contorno Jogador 1

    cont_2 = contours[0] #Contorno Jogador 2

    dicionario_1 = cv2.moments(cont_1) #Dicionário dos Contornos Jogador 1

    dicionario_2 = cv2.moments(cont_2) #Dicionário dos Contornos Jogador 2

    area1 = int(dicionario_1['m00']) #Área Jogador 1

    area2 = int(dicionario_2['m00'])#Área Jogador 2







    # Definindo tipo de jogada de acordo com área do objeto

    if area1 < 58000:
        area1 = "Tesoura"
    elif area1 > 58000 and area1 < 70000:
        area1 = "Pedra"
    elif area1 > 70000:
        area1 = "Papel"

    if area2 < 58000:
        area2 = "Tesoura"

    elif area2 > 58000 and area2 < 70000:
        area2 = "Pedra"

    elif area2 > 70000:
        area2 = "Papel"

    if area1 == "Pedra" and area2 == "Tesoura":
        area1 = "Tesoura"
        area2 = "Pedra"






    # REGRA DO JOGO
    if area1 == area2:
        resultado = "Empate!"

    elif (area1 == "Tesoura" and area2 == "Papel"):
        resultado = "Vitoria do Jogador 1"

    elif (area1 == "Papel" and area2 == "Tesoura"):
        resultado = "Vitoria do Jogador 2"

    elif (area1 == "Pedra" and area2 == "Tesoura"):
        resultado = "Vitoria do Jogador 1"

    elif (area1 == "Tesoura" and area2 == "Pedra"):
        resultado = "Vitoria do Jogador 2"

    elif (area1 == "Papel" and area2 == "Pedra"):
        resultado = "Vitoria do Jogador 1"

    elif (area1 == "Pedra" and area2 == "Papel"):
        resultado = "Vitória do Jogador 2"









    #Colocando Textos na Foto

        # Resultado da Jogada
    cv2.putText(foto, str(resultado), (600, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 157, 255), 4, cv2.LINE_AA)

    #Jogada do Jogador 1
    cv2.putText(foto,("Jogador 1 = " + str(area1)),(25, 950),cv2.FONT_HERSHEY_SIMPLEX,2, (0, 157, 255), 4, cv2.LINE_AA)

    #Jogada do Jogador 2
    cv2.putText(foto,("Jogador 2 = " + str(area2)),(1000, 950),cv2.FONT_HERSHEY_SIMPLEX,2, (0, 157, 255), 4, cv2.LINE_AA)

    #Ajustando tamanho do vídeo
    img_final = cv2.resize(foto, (1366, 768))

    cv2.imshow("Imagem", img_final)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if not ret:
        break


video.release()

cv2.destroyAllWindows()