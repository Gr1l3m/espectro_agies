
import numpy as np
import pandas as pd


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
        elif municipio:
            self.io = float(fila_municipio[3])
        else:
            self.io = 1

        if scr:
            self.scr = scr
        elif municipio:
            self.scr = float(fila_municipio[4])
        else:
            self.scr = 1

        if s1r:
            self.s1r = s1r
        elif municipio:
            self.s1r = float(fila_municipio[5])
        else:
            self.s1r = 1

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
            elif clase_obra in [2, 3]:
                self.nps = 'D'
            else:
                self.nps = 'C'
        elif self.io >= 3:
            if clase_obra == 1:
                self.nps = 'D'
            elif clase_obra in [2, 3]:
                self.nps = 'C'
            else:
                self.nps = 'B'
        elif self.io >= 2:
            if clase_obra == 1:
                self.nps = 'C'
            elif clase_obra in [2, 3]:
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


espectro = Espectro(municipio='Santa Lucía La Reforma')
