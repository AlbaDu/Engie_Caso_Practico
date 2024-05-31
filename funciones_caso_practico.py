
'''
    Código desarrollado en Python 3.12.3.
    Será necesario tener instaladas la librería pandas
'''

#Importación de librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Descarga de warnings
import warnings
warnings.filterwarnings('ignore')

def carga_xlsx(file_path):
    '''Lectura de ficheros de datos en formato xlsx con extracción de su información básica. 
        Toma un único argumento en formato string con el path al archivo.
        Devuelve el describe del archivo una vez cargado.
    '''
    df = pd.read_excel(file_path, dtype=str)
    return df

def valid_invoices(df):
    ''' Función que aplica los criterios minimos que debe tener una factura para que sea considerada validas. 
        Parte de un df y devuelve un df con las facturas que sí cumplen los requisitos
    '''
    #Lista de columnas a checkear que contienen información
    check_nulls = ['NumeroFactura','Emisor','RazonSocialEmisor','Receptor','RazonSocialReceptor','FechaFactura','Importe', 'Moneda','Contrato', 'Origen','ServicioFacturado']
    #Comprobación de que todos los campos tiene datos
    new_df = df.dropna(subset = check_nulls)
    #Comprobamos que no existen facturas con NumeroFactura duplicados, en caso de ocurrir se quedará la primera.
    new_df = new_df.drop_duplicates(subset=['NumeroFactura'], keep='first')
    new_df = new_df.reset_index(drop=True)

    if new_df.shape[0] < df.shape[0]:
        print('El archivo contenía ' + str(df.shape[0]-new_df.shape[0]) + ' facturas no validas, por favor ejecute la función invalid_invoices.')
    else:
        print('Todas las facturas del archivo son válidas.')
    return new_df

def invalid_invoices(df):
    ''' Función que aplica los criterios minimos que debe tener una factura para que sea considerada validas. 
        Parte de un df y devuelve un df con las facturas que no cumplen los requisitos
    '''
    #Lista de columnas a checkear que contienen información
    check_nulls = ['NumeroFactura','Emisor','RazonSocialEmisor','Receptor','RazonSocialReceptor','FechaFactura','Importe', 'Moneda','Contrato', 'Origen','ServicioFacturado']
    #DF auxiliar para comprobar que campos no tiene datos.
    aux_df = df.dropna(subset = check_nulls)
    ##DF auxiliar para comprobar que no hay NumeroFactura duplicados
    aux_df = aux_df.drop_duplicates(subset=['NumeroFactura'], keep='first')
    aux_lst = list(aux_df['NumeroFactura'])
    #DF con facturas erróneas por algún motivo
    new_df = df[~df['NumeroFactura'].isin(aux_lst)]
    new_df = new_df.reset_index(drop=True)
    print('El archivo contenía ' + str(new_df.shape[0]) + ' facturas no validas')
    return new_df

def global_info(df):
    ''' Funcion que proporciona datos agregados globales del fichero del dataframe de facturas válidas
        Parte del df con las facturas válidas y devuelve un df con información agregada
    '''
    #Calculo numero facturas
    a = df['NumeroFactura'].nunique()
    #Calculo de clientes
    b = df['RazonSocialEmisor'].nunique()
    #Facturacion total
    c = str(df['Importe'].astype(float).sum().round(3)) + str(df['Moneda'][1])

    #Construccion del DF final
    new_df = pd.DataFrame(data={'NumeroFacturasValidas':a, 'NumeroClientes':b,'FacturacionTotal':c}, index=[0])
    return new_df

def client_info(df):
    '''Funcion que proporciona datos agregados por cada cliente del fichero del dataframe de facturas válidas
       Parte del df con las facturas válidas y devuelve un df con información agregada
    '''
    final_df = pd.DataFrame(columns=['RazonSocialEmisor', 'Emisor ','NumeroOrigenes', 'NumServiciosFacturados', 'NumeroFacturas','FacturacionTotal'])
    #Clientes en el fichero
    clients = list(df['RazonSocialEmisor'].value_counts().keys())
    #Iteramos sobre los clientes
    for i in clients:
        #flitramos datos del cliente:
        df_aux = df[df['RazonSocialEmisor']== i]     
        #Extración datos asociados
        d = df_aux['Emisor'].unique()
        #Selección del Origen
        e = df_aux['Origen'].nunique()
        #Selección del ServicioFacturado
        f = df_aux['ServicioFacturado'].nunique()
        #Calculo de numero facturas
        g = df_aux.shape[0]
        #Facturacion total
        h = str(df_aux['Importe'].astype(float).sum().round(3)) + 'EUR'
        #Creación del dataframe
        new_df = pd.DataFrame(data={'RazonSocialEmisor':i, 'Emisor ':d,'NumeroOrigenes':e, 'NumServiciosFacturados':f, 'NumeroFacturas':g,'FacturacionTotal':h})

        final_df = pd.concat([final_df, new_df])
             
    return final_df







