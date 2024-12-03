# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.

def pregunta_01():
    
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```

"""



import pandas as pd
import glob
import os

def pregunta_01():
    """
    Genera dos archivos llamados "train_dataset.csv" y "test_dataset.csv" 
    con frases y su respectivo sentimiento, a partir de los datos almacenados 
    en la carpeta "input" que contiene las subcarpetas "train" y "test".

    Los archivos generados estarán en la carpeta "files/output/".
    """

    def procesar_datos(base_path, output_file):
        """
        Procesa los datos de un directorio base con subcarpetas de sentimientos
        y genera un archivo CSV consolidado.

        Args:
            base_path (str): Ruta base de los datos (por ejemplo, 'files/input/test' o 'files/input/train').
            output_file (str): Ruta completa del archivo CSV de salida.
        """
        # Listado de carpetas que representan las clases de sentimiento
        folder_list = ["negative", "neutral", "positive"]
        
        # Lista para almacenar todos los datos
        data = []
        
        # Recorrer las carpetas de sentimientos
        for folder in folder_list:
            # Obtener todos los archivos dentro de la carpeta
            filenames = glob.glob(f"{base_path}/{folder}/*")
            
            # Leer cada archivo y agregar su contenido junto con el sentimiento correspondiente
            for filename in filenames:
                # Leer el archivo y agregar una columna de sentimiento
                df = pd.read_csv(filename, sep="\t", header=None, names=["phrase"])
                df["sentiment"] = folder  # Agregar la columna de sentimiento
                data.append(df)
        
        # Concatenar todos los DataFrames en uno solo
        full_df = pd.concat(data, ignore_index=True)
        
        # Renombrar la columna "sentiment" a "target"
        full_df.rename(columns={"sentiment": "target"}, inplace=True)
        
        # Guardar el DataFrame consolidado en un archivo CSV
        full_df.to_csv(output_file, sep=",", index=False, header=True)
        
        return full_df

    # Crear la carpeta de salida si no existe
    output_folder = "files/output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Carpeta creada: {output_folder}")
    else:
        print(f"Carpeta ya existe: {output_folder}")

    # Procesar los conjuntos de datos de prueba y entrenamiento
    df_test = procesar_datos("files/input/test", f"{output_folder}/test_dataset.csv")
    df_train = procesar_datos("files/input/train", f"{output_folder}/train_dataset.csv")

    return df_test, df_train
