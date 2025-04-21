# Proyecto_BDD_Gran_Escala

## Integrantes:
1. Diego Moyano 202004509-7
2. Luis Zegarra 202073628-6
3. Nicolas Cancino

--- 
## Tabla 
<table>
  <tr>
    <th rowspan="2"></th>
    <th colspan="3">Avro</th>
    <th colspan="4">Parquet</th>
  </tr>
  <tr>
    <th>sin comprimir</th></th>
    <th>deflate</th>
    <th>snappy</th>
    <th>sin comprimir</th>
    <th>snappy</th>
    <th>gzip</th>
    <th>lz4</th>
  </tr>
  <tr>
    <td>1%</td>
    <td>0.02468</td>
    <td>0.02450</td>
    <td>0.02375</td>
    <td>0.01937</td>
    <td>0.01698</td>
    <td>0.01820</td>
    <td>0.01572</td>
  </tr>
  <tr>
    <td>10%</td>
    <td>0.22305</td>
    <td>0.25430</td>
    <td>0.22637</td>
    <td>0.14589</td>
    <td>0.14802</td>
    <td>0.16962</td>
    <td>0.14713</td>
  </tr>
  <tr>
    <td>25%</td>
    <td>0.57816</td>
    <td>0.60594</td>
    <td>0.56486</td>
    <td>0.38810</td>
    <td>0.37261</td>
    <td>0.43634</td>
    <td>0.37529</td>
  </tr>
  <tr>
    <td>50%</td>
    <td>1.15138</td>
    <td>1.21575</td>
    <td>1.15152</td>
    <td>0.77122</td>
    <td>0.77585</td>
    <td>0.83723</td>
    <td>0.76720</td>
  </tr>
  <tr>
    <td>100%</td>
    <td>2.29346</td>
    <td>2.45873</td>
    <td>2.31664</td>
    <td>1.53747</td>
    <td>1.56181</td>
    <td>1.69163</td>
    <td>1.56030</td>
  </tr>
</table>

## Gráfica

## Respuestas
Responda las siguientes preguntas:
### a) ¿Qué conclusiones puede obtener de los resultados anteriores? (15 puntos)
De los resultados, se puede analizar que el escritura y empaquetado de Parquet siempre es más rápido que el Avro; a la vez hay que destacar que Snappy para ambos tipos es el que mejor comportamiento tiene de los métodos utilizados.


### b) Basado en los resultados: ¿Qué combinación (formato/compresión) elegiría para almacenar el dataset en un data lake en la nube? Justifique su respuesta.(15 puntos)
Como estamos hablando de la nuve, entonces lo que se busca es la optimización de recursos por lo que un método como en este caso deflate para Avro y gzip para Parquet serían los recomendables. Si lo que se buscara es velocidada, optar por Lz4 en Parquet sería una buena idea, ya que por el tiempo que se demora nos dice que no comprime tanto el archivo como Gzip, pero aún así hace un trabajo disminuyendo el tamaño del archivo. No sería bueno Snappy porque solo se centra en la velocidad más que en disminuir el tamaño del archivo, cosa que es importante en este caso.

### c) ¿Cuál fue el principal desafío para desarrollar la presente tarea? (10 puntos)
