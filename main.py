import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import numpy as np
import os
#criando um caminho flexivel para os arquivos serem carregados no programa(importante para compartilhar o codigo)
pasta_dados = os.path.join(os.getcwd(), "dados") 

#Função para importar as planilha do execel 
@st.cache_data
def importar_planilha(nome):
    return pd.read_excel(os.path.join(pasta_dados,nome))

#importando planilha do excel 
mouses = importar_planilha('mouses.xlsx')

# Configuração da página
st.set_page_config(page_title="Análise de Mouses")

# Título
st.title('Análise de Preços de Mouses')
st.markdown('**Trabalho de Estatística - Preço de Mouses no Mercado Livre**')

# Filtro por marca
marcas = ['Todas'] + list(mouses['marca'].unique())
marca_selecionada = st.selectbox('Filtrar por Marca', options=marcas)

if marca_selecionada != 'Todas':
    mouses_filtrados = mouses[mouses['marca'] == marca_selecionada]
else:
    mouses_filtrados = mouses

# Abas para organização
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Media, Mediana e moda", "Preço e modelo", "Frequência de marcas","Dpi e preço","Categoria e preço","Quantidade por categoria"])

with tab1:
    st.subheader('Estatísticas Básicas')
    opcao = st.radio("Selecione:", ('Média', 'Mediana', 'Moda'))
    
    if opcao == 'Média':
        st.success(f"**Média dos preços:** R$ {mouses_filtrados['preco_mouse'].mean():.2f}")
    elif opcao == 'Mediana':
        st.info(f"**Mediana dos preços:** R$ {mouses_filtrados['preco_mouse'].median():.2f}")
    else:
        st.error(f"**Moda dos preços:** R$ {mouses_filtrados['preco_mouse'].mode()[0]}")
    
    # Mostrar o DataFrame
    st.subheader('Tabela de Dados')
    st.dataframe(mouses, use_container_width=True, hide_index=True)
with tab2:
    st.subheader('Gráfico dos Preços')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(mouses_filtrados['modelo'], mouses_filtrados['preco_mouse'], color='skyblue')
    plt.xticks(rotation=90)
    plt.xlabel('Modelo')
    plt.ylabel('Preço (R$)')
    plt.title('Preço dos Mouses')
    st.pyplot(fig) 

with tab3:
    st.subheader('Frequência de Marcas (Presentes na tabela)')

    frequencia_absoluta = mouses['marca'].value_counts()
    frequencia_relativa = mouses['marca'].value_counts(normalize=True) * 100

    frequencia = pd.DataFrame({
    'Frequência Absoluta': frequencia_absoluta,
    'Frequência Relativa (%)': frequencia_relativa.round(2)
    })

    st.dataframe(frequencia, use_container_width=True, hide_index=True)

    # Gráfico de Pizza
    st.subheader('Distribuição de Marcas (%)')

    fig2, ax2 = plt.subplots()
    ax2.pie(frequencia_relativa, labels=frequencia_relativa.index, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')  
    st.pyplot(fig2)

with tab4:
    st.subheader('Relação DPI vs. Preço com Linha de Tendência')
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(mouses['dpi'], mouses['preco_mouse'], color='purple', alpha=0.7, edgecolors='w', s=80)

    # Criando linha de tendência
    coef = np.polyfit(mouses['dpi'], mouses['preco_mouse'], 1)
    poly1d_fn = np.poly1d(coef)
    ax.plot(mouses['dpi'], poly1d_fn(mouses['dpi']), color='red', linestyle='--')

    ax.set_xlabel('DPI')
    ax.set_ylabel('Preço (R$)')
    ax.set_title('DPI vs Preço com Tendência Linear')
    ax.grid(True)

    st.pyplot(fig)
    
with tab5:
    st.subheader('Relação de categoria e preço')
    preco_por_categoria = mouses.groupby('tipo_mouse')['preco_mouse'].mean().reset_index()
    fig_bar, ax_bar = plt.subplots(figsize=(8,6))
    ax_bar.bar(preco_por_categoria['tipo_mouse'], preco_por_categoria['preco_mouse'], color='skyblue')
    ax_bar.set_xlabel('Categoria (Tipo de Mouse)')
    ax_bar.set_ylabel('Preço Médio (R$)')
    ax_bar.set_title('Preço Médio por Categoria de Mouse')
    ax_bar.set_xticklabels(preco_por_categoria['tipo_mouse'], rotation=45, ha='right')
    ax_bar.grid(axis='y')
    
    for i in range(len(preco_por_categoria)):
        valor = preco_por_categoria['preco_mouse'][i]
        posicao_x = i
        posicao_y = valor
        ax_bar.text(posicao_x, posicao_y + 0.5, str(f'R$: {valor} reais'), ha='center', va='bottom', fontsize=10)
    st.pyplot(fig_bar)

with tab6:
    quantidade_por_categoria = mouses['tipo_mouse'].value_counts().reset_index()
    quantidade_por_categoria.columns = ['tipo_mouse', 'quantidade']


    fig_quantidade, ax_quantidade = plt.subplots(figsize=(8,6))
    ax_quantidade.bar(quantidade_por_categoria['tipo_mouse'], quantidade_por_categoria['quantidade'], color='lightgreen')
    ax_quantidade.set_xlabel('Categoria (Tipo de Mouse)')
    ax_quantidade.set_ylabel('Quantidade')
    ax_quantidade.set_title('Quantidade de Mouses por Categoria')
    ax_quantidade.set_xticklabels(quantidade_por_categoria['tipo_mouse'], rotation=45, ha='right')
    ax_quantidade.grid(axis='y')

    # Forçando números inteiros no eixo Y
    ax_quantidade.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Adicionando os valores nas barras
    for i in range(len(quantidade_por_categoria)):
        valor = quantidade_por_categoria['quantidade'][i]
        posicao_x = i
        posicao_y = valor
        ax_quantidade.text(posicao_x, posicao_y + 0.5, str(f'{valor} unidades'), ha='center', va='bottom', fontsize=10)

    st.pyplot(fig_quantidade)
