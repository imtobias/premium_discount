import numpy as np
import pandas as pd
import openpyxl

import streamlit as st

st.title('Premium Discount')
st.subheader('Procedure')
st.write("""Premium discounts
are an insurance-specific instance of the general notion in economics of quantity discounts: Clients get a discount for contracts with larger premiums. These
discounts are dictated by regulatory agencies, and are calculated exactly like income taxes for single-state policies: Apply a marginal tax (discount) rate to each 
income (premium) bracket, then add up the tax (discount) from each bracket. Each state has a specified premium discount table, which may have different rates and brackets.

The procedure for multi-state policies is similar: 

(1) For each state s, use the total policy premium T to calculate the premium discount D(s,T) for a single-state policy in state s with premium T.

(2) Let the premium written in state s be denoted by P(s). Then the premium discount on the policy is""")
st.latex(r'''\sum_s \frac{P(s)}{T}D(s,T). ''')

st.write("The calculator below produces the premium discount for each state, if you specify the policy's premium in each state.")
#get user inputs for bodyweight and target bodyweight loss as a percent;
#produce target calories and macros as output
#states = pd.read_csv("state_names.csv")
st.subheader('Calculator')
st.write('Enter each state\'s name and subject premium; the individual premium discounts appear below. If your policy has less than five states,\
    just enter the states you have and leave the other entries\' subject premium at zero.')
premium_tables = pd.read_csv("state_premium_tables.csv")
premium_tables['State'] = premium_tables['State'].str.title()
na_states = premium_tables[premium_tables['Table'].isna()]['State'].unique()
premium_tables = premium_tables.dropna()   
premium_tables['Table'] = premium_tables['Table'].str[-1]
#st.write(premium_tables)
#st.write('Missing states: ', na_states)
states = premium_tables['State'].tolist()
already_used_states = []
remaining_states = []
c11, c12 = st.columns(2)
with c11:
    state1 = st.selectbox(label="State 1",options=states)
    already_used_states.append(state1)
    remaining_states = list(set(states) - set(already_used_states))
    remaining_states.sort()
with c12:
    subject_premium1 = st.number_input('Subject premium 1',min_value=0)
c21, c22 = st.columns(2)
with c21:
    state2 = st.selectbox(label="State 2",options=remaining_states)
    already_used_states.append(state2)
    remaining_states = list(set(states) - set(already_used_states))
    remaining_states.sort()
with c22:
    subject_premium2 = st.number_input('Subject premium 2',min_value=0)
c31, c32 = st.columns(2)
with c31:
    state3 = st.selectbox(label="State 3",options=remaining_states)
    already_used_states.append(state3)
    remaining_states = list(set(states) - set(already_used_states))
    remaining_states.sort()
with c32:
    subject_premium3 = st.number_input('Subject premium 3',min_value=0)
c41, c42 = st.columns(2)
with c41:
    state4 = st.selectbox(label="State 4",options=remaining_states)
    already_used_states.append(state4)
    remaining_states = list(set(states) - set(already_used_states))
    remaining_states.sort()
with c42:
    subject_premium4 = st.number_input('Subject premium 4',min_value=0)
c51, c52 = st.columns(2)
with c51:
    state5 = st.selectbox(label="State 5",options=remaining_states)
    already_used_states.append(state5)
    remaining_states = list(set(states) - set(already_used_states))
    remaining_states.sort()
with c52:
    subject_premium5 = st.number_input('Subject premium 5',min_value=0)

table1 = pd.read_csv('table1.csv')
table7 = pd.read_csv('table7.csv')
table9 = pd.read_csv('table9.csv')

table1_layers = [
    [0,5000,0],
    [5000,100000,0.095],
    [100000,500000,0.119],
    [500000,10**9,0.124]
]
table7_layers = [
    [0,5000,0],
    [5000,100000,0.109],
    [100000,500000,0.126],
    [500000,10**9,0.144]
]
table9_layers = [
    [0,10000,0],
    [10000,200000,0.091],
    [200000,1750000,0.113],
    [1750000,10**9,0.123]
]

#layers is a list of lists, where each layers[k] = [start_layer_k,end_layer_k_,discount_k]
def discount_given_layers(premium, layers):
    cumulative_discount = 0
    for layer in layers:
        start_layer = layer[0]
        end_layer = layer[1]
        discount_rate = layer[2]
        discount = max((premium - start_layer) * discount_rate, 0) #if premium is lower than start layer, no negative discount
        discount = min(discount, (end_layer - start_layer) * discount_rate) #if premium exceeds end layer, cap discount from this layer
        cumulative_discount += discount
    return cumulative_discount

def premium_discount(premium, table_number):
    discount = 0
    if table_number == 1:
        discount = discount_given_layers(premium, table1_layers)
    if table_number == 7:
        discount = discount_given_layers(premium, table7_layers)
    if table_number == 9:
        discount = discount_given_layers(premium, table9_layers)
    return discount

#get state, discount_given_layers for state k * SP[k] / total_SP
total_premium = subject_premium1 + subject_premium2 + subject_premium3 + subject_premium4 + subject_premium5

res = []
for pair in [[state1, subject_premium1],[state2, subject_premium2],[state3, subject_premium3],[state4, subject_premium4],[state5, subject_premium5]]:
    state = pair[0]
    subject_premium = pair[1]
    if subject_premium > 0:
        discount = int(premium_discount(total_premium, int(premium_tables[premium_tables['State'] == state]['Table'].values)) * subject_premium / total_premium)
        res.append([state, discount])
discounts = pd.DataFrame(data=res, columns=['State','Premium Discount'])

st.write('')
st.write('Premium discounts by state:')
st.write(discounts)

st.subheader('Calculator details')
st.write('Each state uses one of three discount tables:')
st.write(premium_tables)

col1, col2, col3 = st.columns(3)

with col1:
    st.write('Table 1:')
    st.write(table1)


with col2:
    st.write('Table 7:')
    st.write(table7)

with col3:
    st.write('Table 9:')
    st.write(table9)

st.subheader('Contact')
st.write('For questions/help, you can reach me at tobyim@gmail.com')
