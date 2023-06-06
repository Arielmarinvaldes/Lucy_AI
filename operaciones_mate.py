# import logging

def convertir_numero(palabra):
    numeros = {
        'cero': 0,
        'uno': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6,
        'siete': 7,
        'ocho': 8,
        'nueve': 9,
        'diez': 10
        # Agrega más palabras numéricas según tus necesidades
    }
    
    palabra = palabra.lower()
    
    if palabra in numeros:
        return numeros[palabra]
    else:
        try:
            numero = int(palabra)
            return numero
        except ValueError:
            return None



# # logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
