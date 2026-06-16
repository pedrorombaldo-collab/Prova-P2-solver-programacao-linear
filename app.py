import streamlit as st
from scipy.optimize import linprog
import numpy as np

st.set_page_config(page_title="Solver PL", layout="wide")

st.title("📈 Solver de Programação Linear")

tipo = st.selectbox(
    "Tipo de problema",
    ["Maximização", "Minimização"]
)

n_var = st.number_input(
    "Número de variáveis",
    min_value=1,
    max_value=20,
    value=4
)

n_rest = st.number_input(
    "Número de restrições",
    min_value=1,
    max_value=50,
    value=3
)

st.subheader("Função Objetivo")

c = []

cols = st.columns(int(n_var))

for i in range(int(n_var)):
    c.append(
        cols[i].number_input(
            f"x{i+1}",
            value=0.0,
            key=f"obj{i}"
        )
    )

st.subheader("Restrições")

A = []
B = []

for r in range(int(n_rest)):

    st.markdown(f"### Restrição {r+1}")

    linha = []

    cols = st.columns(int(n_var))

    for j in range(int(n_var)):
        valor = cols[j].number_input(
            f"x{j+1}",
            value=0.0,
            key=f"r{r}c{j}"
        )
        linha.append(valor)

    limite = st.number_input(
        "Limite",
        value=0.0,
        key=f"lim{r}"
    )

    A.append(linha)
    B.append(limite)

if st.button("Resolver"):

    coef = c.copy()

    if tipo == "Maximização":
        coef = [-x for x in coef]

    bounds = [(0, None)] * int(n_var)

    resultado = linprog(
        coef,
        A_ub=A,
        b_ub=B,
        bounds=bounds,
        method="highs"
    )

    if resultado.success:

        st.success("Solução encontrada!")

        for i in range(int(n_var)):
            st.write(
                f"x{i+1} = {resultado.x[i]:.4f}"
            )

        valor = resultado.fun

        if tipo == "Maximização":
            valor = -valor

        st.metric(
            "Valor Ótimo",
            round(valor, 4)
        )

    else:
        st.error("Problema sem solução viável.")
