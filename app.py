import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Reporte de ventas',
                   page_icon=':moneyback:',
                   layout="wide")

st.title(':clipboard: Reporte de Ventas')
st.subheader('BURO GROUP')
st.markdown('##')

archivo_excel = 'MES.xlsx'
hoja_excel = 'BASE'

df = pd.read_excel('MES.xlsx',
                   sheet_name=hoja_excel,
                   usecols='A:O')

#st.dataframe(df)

st.sidebar.header("Opciones de filtro")
zona = st.sidebar.multiselect(
    "Seleccione la zona:",
    options=df['ZONA'].unique(),
    default=df['ZONA'].unique()
)

tutelado = st.sidebar.multiselect(
    "Tutelado (?):",
    options=df['TUTELADO'].unique(),
    default=df['TUTELADO'].unique(),
)

df_seleccion = df.query("ZONA == @zona & TUTELADO == @tutelado")



total_ventas = int(df_seleccion['IMPORTE_SOL_SOLES'].sum())
#tota_tutelados = int(df_seleccion['TUTELADO'].count())
total_operaciones = int(df_seleccion['IMPORTE_SOL_SOLES'].count())

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("ventas totales:")
    st.subheader(f"PEN S/. {total_ventas:,}")
    
with right_column:
    st.subheader("total operaciones")
    st.subheader(f" {total_operaciones}")

st.markdown("---")
    
st.dataframe(df_seleccion)

st.markdown("---")
st.markdown("---")

ventas_por_promotor = (df_seleccion.groupby(by=['PROMOTOR']).sum()[['IMPORTE_SOL_SOLES']].sort_values(by='IMPORTE_SOL_SOLES'))
 
fig_ventas_por_promotor = px.bar(
    ventas_por_promotor,
    x=ventas_por_promotor.index,
    y='IMPORTE_SOL_SOLES',
    title= '<b>Ventas por promotor</b>',
    color_discrete_sequence= ["#F5B932"]*len(ventas_por_promotor),
    template = 'plotly_white'
    )   

fig_ventas_por_promotor.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_ventas_por_promotor)
    