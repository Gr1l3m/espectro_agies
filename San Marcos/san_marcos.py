from espectro import Espectro
import pandas as pd

municipios = ['Ayutla', 'Catarina', 'Comitancillo',
              'Concepción Tutuapa', 'El Quetzal', 'El Rodeo',
              'El Tumbador', 'Esquipulas Palo Gordo', 'Ixchiguan', 'La Blanca']

tipos = ['a', 'b', 'c', 'd', 'e']

for m in municipios:
    for e in tipos:
        espectro = Espectro(municipio=m, na=1, nv=1, kd=0.8, tiempo_total=6, delta_tiempo=0.05)
        espectro.clase_sitio(e)
        espectro.tipo_suelo_propuesta(e)
        espectro.calcular()

        df_final = pd.DataFrame(espectro.espectro_resultado[:, [0, 2, 3]])
        filepath = m+' '+e+'.xlsx'
        df_final.to_excel(filepath, index=False)
