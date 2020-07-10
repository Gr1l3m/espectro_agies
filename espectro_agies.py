import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import math
import numpy as np
# from scipy.linalg import solve
import logging
import pandas as pd
from datetime import datetime
ahora = datetime.now().strftime('%d-%m-%y-%H-%M-%S')+'.log'
logging.basicConfig(level=logging.INFO, filename=ahora)


class Espectro(object):
    # Caracteristicas para calculo
    clase_obra = 0
    clase_sitio = 0
    fuente_sismica = 0
    distancia_horizontal = 0

    # Nivel de proteccion sismica
    nps = 0

    def __init__(self, municipio='', io=0., scr=0., s1r=0., velocidad_viento='', fa=1., fv=1., na=1., nv=1., kd=1.,
                 tiempo_total=1., delta_tiempo=1.,
                 r=1, io_propuesta=1., scr_propuesta=1., s1r_propuesta=1., tl=1.):

        if municipio:
            dfs = pd.read_excel('tablaMunicipios.xlsx', header=None, sheet_name='Hoja1')
            fila_municipio = dfs.loc[dfs[1].str.casefold() == municipio.casefold()]

            dfs2 = pd.read_excel('tablaMunicipios.xlsx', header=None, sheet_name='Hoja2')
            self.fila_propuesta = dfs2.loc[dfs2[1].str.casefold() == municipio.casefold()]

        if io:
            self.io = io
        else:
            self.io = float(fila_municipio[3])

        if scr:
            self.scr = scr
        else:
            self.scr = float(fila_municipio[4])

        if s1r:
            self.s1r = s1r
        else:
            self.s1r = float(fila_municipio[5])

        if velocidad_viento:
            self.velocidad_viento = velocidad_viento
        elif municipio:
            self.velocidad_viento = float(fila_municipio[6])
        else:
            self.velocidad_viento = 1

        self.fa = fa
        self.fv = fv
        self.na = na
        self.nv = nv
        self.kd = kd

        self.factor_reduccion = r

        self.tiempo_total = tiempo_total
        self.delta_tiempo = delta_tiempo

        self.arreglo_tiempo = np.arange(0, self.tiempo_total + self.delta_tiempo, self.delta_tiempo)
        self.espectro_resultado = np.zeros((len(self.arreglo_tiempo), 4))

        self.io_propuesta = io_propuesta
        self.scr_propuesta = scr_propuesta
        self.s1r_propuesta = s1r_propuesta
        self.tl = tl

    # Metodo para obtener el nivel de proteccion sismica
    def clase_obra(self, clase_obra):
        # self.clase_obra = clase_obra
        if self.io >= 4:
            if clase_obra == 1:
                self.nps = 'E'
            elif clase_obra == 2 or clase_obra == 3:
                self.nps = 'D'
            else:
                self.nps = 'C'
        elif self.io >= 3:
            if clase_obra == 1:
                self.nps = 'D'
            elif clase_obra == 2 or clase_obra == 3:
                self.nps = 'C'
            else:
                self.nps = 'B'
        elif self.io >= 2:
            if clase_obra == 1:
                self.nps = 'C'
            elif clase_obra == 2 or clase_obra == 3:
                self.nps = 'B'
            else:
                self.nps = 'A'

    # Metodo para obtener Fa y Fv
    def clase_sitio(self, clase_sitio):
        # self.clase_sitio = clase_sitio
        if type(clase_sitio) is str:
            if clase_sitio.casefold() == 'a':
                clase_sitio = 1
            elif clase_sitio.casefold() == 'b':
                clase_sitio = 1
            elif clase_sitio.casefold() == 'c':
                clase_sitio = 2
            elif clase_sitio.casefold() == 'd':
                clase_sitio = 3
            elif clase_sitio.casefold() == 'e':
                clase_sitio = 4
            elif clase_sitio.casefold() == 'f':
                clase_sitio = 5
        if clase_sitio == 5:
            print('Se requiere evaluación específico')
        elif clase_sitio == 4:
            if self.io == 2.1:
                self.fa = 1.7
                self.fv = 3.3
            elif self.io == 2.2:
                self.fa = 1.3
                self.fv = 2.8
            elif self.io == 3.1:
                self.fa = 1.1
                self.fv = 2.6
            elif self.io == 3.2:
                self.fa = 1.0
                self.fv = 2.4
            else:
                self.fa = 0.9
                self.fv = 2.2
        elif clase_sitio == 3:
            if self.io == 2.1:
                self.fa = 1.4
                self.fv = 2.2
            elif self.io == 2.2:
                self.fa = 1.2
                self.fv = 2.0
            elif self.io == 3.1:
                self.fa = 1.1
                self.fv = 1.9
            elif self.io == 3.2:
                self.fa = 1.0
                self.fv = 1.8
            else:
                self.fa = 1.0
                self.fv = 1.7
        elif clase_sitio == 2:
            if self.io == 2.1:
                self.fa = 1.3
                self.fv = 1.5
            elif self.io == 2.2:
                self.fa = 1.2
                self.fv = 1.5
            elif self.io == 3.1:
                self.fa = 1.2
                self.fv = 1.5
            elif self.io == 3.2:
                self.fa = 1.2
                self.fv = 1.5
            else:
                self.fa = 1.2
                self.fv = 1.4
        else:
            self.fa = 1.0
            self.fv = 1.0

    # Metodo para obtener Na y Nv
    def fuente_sismica(self, fuente_sismica, distancia_horizontal):
        # self.fuente_sismica = fuente_sismica
        # self.distancia_horizontal = distancia_horizontal
        if type(fuente_sismica) is str:
            if fuente_sismica.casefold() == 'a':
                fuente_sismica = 1
            elif fuente_sismica.casefold() == 'b':
                fuente_sismica = 2
            elif fuente_sismica.casefold() == 'c':
                fuente_sismica = 3
        if type(distancia_horizontal) is str:
            distancia_horizontal = int(distancia_horizontal)
        if fuente_sismica == 1:
            if distancia_horizontal <= 2:
                self.na = 1.25
                self.nv = 1.4
            elif distancia_horizontal == 5:
                self.na = 1.12
                self.nv = 1.2
            elif distancia_horizontal == 10:
                self.na = 1.0
                self.nv = 1.1
            else:
                self.na = 1.0
                self.nv = 1.0
        elif fuente_sismica == 2:
            if distancia_horizontal <= 2:
                self.na = 1.12
                self.nv = 1.2
            elif distancia_horizontal == 5:
                self.na = 1.0
                self.nv = 1.1
            elif distancia_horizontal == 10:
                self.na = 1.0
                self.nv = 1.0
            else:
                self.na = 1.0
                self.nv = 1.0
        else:
            self.na = 1.0
            self.nv = 1.0

    # metodo para obtener kd
    def tipo_sismo(self, tipo_sismo):
        if tipo_sismo == 1:
            self.kd = 0.66
        elif tipo_sismo == 2:
            self.kd = 0.80
        elif tipo_sismo == 3:
            self.kd = 1.00
        else:
            self.kd = 0.55

    def tipo_suelo_propuesta(self, suelo):
        self.io_propuesta = float(self.fila_propuesta[3])
        if suelo.casefold() == 'a':
            self.scr_propuesta = float(self.fila_propuesta[4])
            self.s1r_propuesta = float(self.fila_propuesta[5])
            self.tl = float(self.fila_propuesta[6])
        elif suelo.casefold() == 'b':
            self.scr_propuesta = float(self.fila_propuesta[7])
            self.s1r_propuesta = float(self.fila_propuesta[8])
            self.tl = float(self.fila_propuesta[9])
        elif suelo.casefold() == 'c':
            self.scr_propuesta = float(self.fila_propuesta[10])
            self.s1r_propuesta = float(self.fila_propuesta[11])
            self.tl = float(self.fila_propuesta[12])
        elif suelo.casefold() == 'd':
            self.scr_propuesta = float(self.fila_propuesta[13])
            self.s1r_propuesta = float(self.fila_propuesta[14])
            self.tl = float(self.fila_propuesta[15])
        else:
            self.scr_propuesta = float(self.fila_propuesta[16])
            self.s1r_propuesta = float(self.fila_propuesta[17])
            self.tl = float(self.fila_propuesta[18])

    def calcular(self):
        self.arreglo_tiempo = np.arange(0, self.tiempo_total + self.delta_tiempo, self.delta_tiempo)
        self.espectro_resultado = np.zeros((len(self.arreglo_tiempo), 4))

        scs = self.scr * self.fa * self.na
        s1s = self.s1r * self.fv * self.nv

        # Periodos
        ts = s1s / scs
        to = ts * 0.2

        scd = self.kd * scs
        s1d = self.kd * s1s

        # Aceleracion maxima del suelo
        amsd = 0.4 * scd

        for T in range(0, len(self.arreglo_tiempo)):
            if self.arreglo_tiempo[T] <= ts:
                self.espectro_resultado[T, 0] = self.arreglo_tiempo[T]
                self.espectro_resultado[T, 1] = scd
                self.espectro_resultado[T, 2] = scd/self.factor_reduccion
            else:
                self.espectro_resultado[T, 0] = self.arreglo_tiempo[T]
                self.espectro_resultado[T, 1] = s1d/self.arreglo_tiempo[T]
                self.espectro_resultado[T, 2] = s1d/self.arreglo_tiempo[T]/self.factor_reduccion

        self.calcular_propuesta()

    def calcular_propuesta(self):
        fa_propuesta = 1
        fv_propuesta = 1
        na_propuesta = 1
        nv_propuesta = 1

        scs = self.scr_propuesta * fa_propuesta * na_propuesta
        s1s = self.s1r_propuesta * fv_propuesta * nv_propuesta

        # Periodos
        ts = s1s / scs
        to = ts * 0.2

        scd = self.kd * scs
        s1d = self.kd * s1s

        # Aceleracion maxima del suelo
        amsd = 0.4 * scd

        for T in range(0, len(self.arreglo_tiempo)):
            if self.arreglo_tiempo[T] <= ts:
                self.espectro_resultado[T, 3] = scd
            else:
                if self.arreglo_tiempo[T] <= self.tl:
                    self.espectro_resultado[T, 3] = s1d/self.arreglo_tiempo[T]
                else:
                    self.espectro_resultado[T, 3] = (s1d/self.arreglo_tiempo[T]**2)*self.tl


# espectro = Espectro(municipio='iztapa', fa=1, fv=1.7, na=1, nv=1, kd=0.8, t=6, dt=0.05)
# espectro.calcular()
# espectro.calcular_propuesta('d')

espectro = 0

matplotlib.use('TkAgg')

raiz = tk.Tk()

raiz.title("Espectro AGIES")
# raiz.state('zoomed')

# panel = PanedWindow(orient=HORIZONTAL)
# panel.pack(fill=BOTH, expand=1)

raiz.config(width='800', height='700')

# busqueda de io scr y s1r en base al municipio
tk.Label(raiz, text='Municipio').place(x='10', y='20')
en_municipio = tk.Entry(raiz)
en_municipio.place(x='100', y='20')

btn_buscar = tk.Button(raiz, text="Buscar", command=lambda: buscar(en_municipio))
btn_buscar.place(x='245', y='20')

tk.Label(raiz, text='Io').place(x='10', y='70')
en_io = tk.Entry(raiz)
en_io.place(x='100', y='70')
tk.Label(raiz, text='Scr').place(x='10', y='100')
en_scr = tk.Entry(raiz)
en_scr.place(x='100', y='100')
tk.Label(raiz, text='S1r').place(x='10', y='130')
en_s1r = tk.Entry(raiz)
en_s1r.place(x='100', y='130')

# busqueda de fa y fv
tk.Label(raiz, text='Clase de sitio').place(x='10', y='220')
en_clase_sitio = ttk.Combobox(raiz)
en_clase_sitio.place(x='100', y='220')
en_clase_sitio["values"] = ["A", "B", "C", "D", "E", "F"]

btn_clase_sitio = tk.Button(raiz, text="Fa y Fv", command=lambda: buscar_fa_fv(en_clase_sitio))
btn_clase_sitio.place(x='245', y='220')

tk.Label(raiz, text='Fa').place(x='10', y='270')
en_fa = tk.Entry(raiz)
en_fa.place(x='100', y='270')
tk.Label(raiz, text='Fv').place(x='10', y='300')
en_fv = tk.Entry(raiz)
en_fv.place(x='100', y='300')

# busqueda de na y nv
tk.Label(raiz, text='Fuente sismica').place(x='10', y='390')
en_fuente_sismica = ttk.Combobox(raiz)
en_fuente_sismica.place(x='100', y='390')
en_fuente_sismica["values"] = ["A", "B", "C"]
tk.Label(raiz, text='Dist. horizontal').place(x='10', y='420')
en_distancia_horizontal = ttk.Combobox(raiz)
en_distancia_horizontal.place(x='100', y='420')
en_distancia_horizontal["values"] = [2, 5, 10, 15]

btn_clase_sitio = tk.Button(raiz, text="Na y Nv", command=lambda: buscar_na_nv(en_fuente_sismica, en_distancia_horizontal))
btn_clase_sitio.place(x='245', y='420')

tk.Label(raiz, text='Na').place(x='10', y='450')
en_na = tk.Entry(raiz)
en_na.place(x='100', y='450')
tk.Label(raiz, text='Nv').place(x='10', y='480')
en_nv = tk.Entry(raiz)
en_nv.place(x='100', y='480')

# Kd
tk.Label(raiz, text='Tipo de sismo').place(x='10', y='570')
en_tipo_sismo = ttk.Combobox(raiz)
en_tipo_sismo.place(x='100', y='570')
en_tipo_sismo["values"] = [1, 2, 3, 4]

btn_tipo_sismo = tk.Button(raiz, text="Kd", command=lambda: buscar_kd(en_tipo_sismo))
btn_tipo_sismo.place(x='245', y='570')

tk.Label(raiz, text='Kd').place(x='10', y='600')
en_kd = tk.Entry(raiz)
en_kd.place(x='100', y='600')

# busqueda de datos de propuesta
tk.Label(raiz, text='Tipo de suelo').place(x='350', y='20')
en_tipo_suelo_propuesta = ttk.Combobox(raiz)
en_tipo_suelo_propuesta.place(x='430', y='20')
en_tipo_suelo_propuesta["values"] = ["A", "B", "C", "D", "E"]

btn_buscar_propuesta = tk.Button(raiz, text="Buscar propuesta", command=lambda: buscar_propuesta(en_tipo_suelo_propuesta))
btn_buscar_propuesta.place(x='585', y='20')

tk.Label(raiz, text='Io propuesta').place(x='350', y='70')
en_io_propuesta = tk.Entry(raiz)
en_io_propuesta.place(x='430', y='70')
tk.Label(raiz, text='Scr propuesta').place(x='350', y='100')
en_scr_propuesta = tk.Entry(raiz)
en_scr_propuesta.place(x='430', y='100')
tk.Label(raiz, text='S1r propuesta').place(x='350', y='130')
en_s1r_propuesta = tk.Entry(raiz)
en_s1r_propuesta.place(x='430', y='130')
tk.Label(raiz, text='TL').place(x='350', y='160')
en_tl_propuesta = tk.Entry(raiz)
en_tl_propuesta.place(x='430', y='160')

# tiempo
tk.Label(raiz, text='Otros datos').place(x='350', y='250')
tk.Label(raiz, text='Tiempo total').place(x='350', y='280')
en_tiempo = tk.Entry(raiz)
en_tiempo.place(x='430', y='280')
tk.Label(raiz, text='Delta tiempo').place(x='350', y='310')
en_delta_tiempo = tk.Entry(raiz)
en_delta_tiempo.place(x='430', y='310')
tk.Label(raiz, text='Reducción').place(x='350', y='370')
en_reduccion = tk.Entry(raiz)
en_reduccion.place(x='430', y='370')

btn_resolver = tk.Button(raiz, text="Encontrar el espectro", command=lambda: resolver())
btn_resolver.place(x='430', y='460')


def set_text(e, text):
    e.delete(0, END)
    e.insert(0, text)


set_text(en_tiempo, 6)
set_text(en_delta_tiempo, 0.05)


def buscar(mun):
    global espectro
    espectro = Espectro(municipio=mun.get())

    set_text(en_io, str(espectro.io))
    set_text(en_scr, str(espectro.scr))
    set_text(en_s1r, str(espectro.s1r))


def buscar_propuesta(tipo_suelo):
    global espectro
    espectro.tipo_suelo_propuesta(tipo_suelo.get())

    set_text(en_io_propuesta, espectro.io_propuesta)
    set_text(en_scr_propuesta, espectro.scr_propuesta)
    set_text(en_s1r_propuesta, espectro.s1r_propuesta)
    set_text(en_tl_propuesta, espectro.tl)


def buscar_fa_fv(c_sitio):
    global espectro
    espectro.clase_sitio(c_sitio.get())

    set_text(en_fa, espectro.fa)
    set_text(en_fv, espectro.fv)


def buscar_na_nv(f_sismica, distancia):
    global espectro
    espectro.fuente_sismica(f_sismica.get(), distancia.get())

    set_text(en_na, espectro.na)
    set_text(en_nv, espectro.nv)


def buscar_kd(en_t_sismo):
    global espectro
    espectro.tipo_sismo(int(en_t_sismo.get()))

    set_text(en_kd, espectro.kd)


def resolver():
    global espectro

    if en_io.get():
        espectro.io = float(en_io.get())
    if en_scr.get():
        espectro.scr = float(en_scr.get())
    if en_s1r.get():
        espectro.s1r = float(en_s1r.get())

    if en_fa.get():
        espectro.fa = float(en_fa.get())
    if en_fv.get():
        espectro.fv = float(en_fv.get())

    if en_na.get():
        espectro.na = float(en_na.get())
    if en_nv.get():
        espectro.nv = float(en_nv.get())

    if en_kd.get():
        espectro.kd = float(en_kd.get())

    if en_tiempo.get():
        espectro.tiempo_total = float(en_tiempo.get())
    if en_delta_tiempo.get():
        espectro.delta_tiempo = float(en_delta_tiempo.get())
    if en_reduccion.get():
        espectro.factor_reduccion = float(en_reduccion.get())

    if en_io_propuesta.get():
        espectro.io_propuesta = float(en_io_propuesta.get())
    if en_scr_propuesta.get():
        espectro.scr_propuesta = float(en_scr_propuesta.get())
    if en_s1r_propuesta.get():
        espectro.s1r_propuesta = float(en_s1r_propuesta.get())
    if en_tl_propuesta.get():
        espectro.tl = float(en_tl_propuesta.get())

    espectro.calcular()
    # logging.info(espectro.espectro_resultado)

    df_final = pd.DataFrame(espectro.espectro_resultado)
    filepath = 'my_excel_file.xlsx'
    df_final.to_excel(filepath, index=False)


# Barra de menu
menubar = tk.Menu(raiz)
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About")
menubar.add_cascade(label="Ayuda", menu=helpmenu)

# display the menu
raiz.config(menu=menubar)

raiz.mainloop()
