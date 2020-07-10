from espectro import Espectro
from PyQt5.QtWidgets import *
import pandas as pd

# espectro = Espectro(municipio='iztapa', fa=1, fv=1.7, na=1, nv=1, kd=0.8, tiempo_total=6, delta_tiempo=0.05)
# espectro.calcular()

espectro = 0

app = QApplication([])
window = QWidget()

total = QHBoxLayout()

form = QFormLayout()
form2 = QFormLayout()

# Municipio
lin_municipio = QLineEdit()
form.addRow(QLabel('Municipio'), lin_municipio)
btn_buscar = QPushButton('Buscar')

form.addRow(btn_buscar)

lin_io = QLineEdit()
form.addRow("Io", lin_io)
lin_scr = QLineEdit()
form.addRow("Scr", lin_scr)
lin_s1r = QLineEdit()
form.addRow("S1r", lin_s1r)

# Fa y Fv
lin_c_sitio = QComboBox()
lin_c_sitio.insertItems(0, ["A", "B", "C", "D", "E", "F"])
form.addRow(QLabel('Clase de sitio'), lin_c_sitio)
btn_fa_fv = QPushButton('Calcular Fa y Fv')
form.addRow(btn_fa_fv)

lin_fa = QLineEdit()
form.addRow("Fa", lin_fa)
lin_fv = QLineEdit()
form.addRow("Fv", lin_fv)

# Na y Nv
form.addRow(QLabel('Fuente sismica'))
lin_fuente_sismica = QComboBox()
lin_fuente_sismica.insertItems(0, ["A", "B", "C"])
form.addRow("Tipo de fuente", lin_fuente_sismica)
lin_distancia_horizontal = QComboBox()
lin_distancia_horizontal.insertItems(0, ['2', '5', '10', '15'])
form.addRow("Dist. horizontal", lin_distancia_horizontal)
btn_na_nv = QPushButton('Calcular Na y Nv')
form.addRow(btn_na_nv)

lin_na = QLineEdit()
form.addRow("Na", lin_na)
lin_nv = QLineEdit()
form.addRow("Nv", lin_nv)

# Kd
lin_t_sismo = QComboBox()
lin_t_sismo.insertItems(0, ['1', '2', '3', '4'])
form.addRow(QLabel('Tipo de sismo'), lin_t_sismo)
btn_kd = QPushButton('Calcular Kd')
form.addRow(btn_kd)

lin_kd = QLineEdit()
form.addRow("Kd", lin_kd)

# Propuesta
form2.addRow(QLabel("Propuesta"))
lin_t_suelo_propuesta = QComboBox()
lin_t_suelo_propuesta.insertItems(0, ["A", "B", "C", "D", "E"])
form2.addRow(QLabel('Tipo de suelo'), lin_t_suelo_propuesta)
btn_buscar_propuesta = QPushButton('Datos de propuesta')
form.addRow(btn_buscar_propuesta)

lin_io_propuesta = QLineEdit()
form2.addRow("Io", lin_io_propuesta)
lin_scr_propuesta = QLineEdit()
form2.addRow("Scr", lin_scr_propuesta)
lin_s1r_propuesta = QLineEdit()
form2.addRow("S1r", lin_s1r_propuesta)
lin_tl_propuesta = QLineEdit()
form2.addRow("TL", lin_tl_propuesta)

btn_propuesta = QPushButton('Datos de propuesta')
form2.addRow(btn_propuesta)

form2.addRow(QLabel("Otros datos"))
lin_tiempo = QLineEdit()
form2.addRow("Tiempo (s)", lin_tiempo)
lin_delta_tiempo = QLineEdit()
form2.addRow("Delta tiempo (s)", lin_delta_tiempo)
lin_reduccion = QLineEdit()
form2.addRow("F. reducción", lin_reduccion)


btn_resolver = QPushButton('Calcular espectro')
form2.addRow(btn_resolver)


def buscar():
    global espectro
    espectro = Espectro(municipio=lin_municipio.text())

    lin_io.setText(str(espectro.io))
    lin_scr.setText(str(espectro.scr))
    lin_s1r.setText(str(espectro.s1r))


def buscar_fa_fv():
    global espectro
    espectro.clase_sitio(lin_c_sitio.currentText())

    lin_fa.setText(str(espectro.fa))
    lin_fv.setText(str(espectro.fv))


def buscar_na_nv():
    global espectro
    espectro.fuente_sismica(lin_fuente_sismica.currentText(), lin_distancia_horizontal.currentText())

    lin_na.setText(str(espectro.na))
    lin_nv.setText(str(espectro.nv))


def buscar_kd():
    global espectro
    espectro.tipo_sismo(int(lin_t_sismo.currentText()))

    lin_kd.setText(str(espectro.kd))


def buscar_propuesta():
    global espectro
    espectro.tipo_suelo_propuesta(lin_t_suelo_propuesta.currentText())

    lin_io_propuesta.setText(str(espectro.io_propuesta))
    lin_scr_propuesta.setText(str(espectro.scr_propuesta))
    lin_s1r_propuesta.setText(str(espectro.s1r_propuesta))
    lin_tl_propuesta.setText(str(espectro.tl))


def resolver():
    global espectro

    if lin_io.text():
        espectro.io = float(lin_io.text())
    if lin_scr.text():
        espectro.scr = float(lin_scr.text())
    if lin_s1r.text():
        espectro.s1r = float(lin_s1r.text())

    if lin_fa.text():
        espectro.fa = float(lin_fa.text())
    if lin_fv.text():
        espectro.fv = float(lin_fv.text())

    if lin_na.text():
        espectro.na = float(lin_na.text())
    if lin_nv.text():
        espectro.nv = float(lin_nv.text())

    if lin_kd.text():
        espectro.kd = float(lin_kd.text())

    if lin_tiempo.text():
        espectro.tiempo_total = float(lin_tiempo.text())
    if lin_delta_tiempo.text():
        espectro.delta_tiempo = float(lin_delta_tiempo.text())
    if lin_reduccion.text():
        espectro.factor_reduccion = float(lin_reduccion.text())

    if lin_io_propuesta.text():
        espectro.io_propuesta = float(lin_io_propuesta.text())
    if lin_scr_propuesta.text():
        espectro.scr_propuesta = float(lin_scr_propuesta.text())
    if lin_s1r_propuesta.text():
        espectro.s1r_propuesta = float(lin_s1r_propuesta.text())
    if lin_tl_propuesta.text():
        espectro.tl = float(lin_tl_propuesta.text())

    espectro.calcular()

    df_final = pd.DataFrame(espectro.espectro_resultado)
    filepath = lin_municipio.text()+lin_c_sitio.currentText()+lin_t_suelo_propuesta.currentText()+'.xlsx'
    df_final.to_excel(filepath, index=False)


btn_buscar.clicked.connect(buscar)
btn_buscar.show()

btn_fa_fv.clicked.connect(buscar_fa_fv)
btn_fa_fv.show()

btn_na_nv.clicked.connect(buscar_na_nv)
btn_na_nv.show()

btn_kd.clicked.connect(buscar_kd)
btn_kd.show()

btn_propuesta.clicked.connect(buscar_propuesta)
btn_propuesta.show()

btn_resolver.clicked.connect(resolver)
btn_resolver.show()

total.addLayout(form)
total.addLayout(form2)

window.setLayout(total)
window.show()

app.exec_()
