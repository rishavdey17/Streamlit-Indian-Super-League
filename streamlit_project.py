import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from mplsoccer.pitch import Pitch, VerticalPitch

st.title("Indian Super League 2024-25")
st.subheader("Actions and Heat Map of all players in the match.")

df = pd.read_csv("Mohun Bagan vs Punjab.csv")

player = st.selectbox("Select A Player", df['playerName'].sort_values().unique(), index = None)

def filter_data(df, player):
    if player:
        df = df[df['playerName'] == player]

    return df

filtered_data = filter_data(df, player)

pitch = VerticalPitch(pitch_type='opta', pitch_color='#09075a', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(10, 10), constrained_layout=True, tight_layout=False)
fig.set_facecolor('#09075a')

def plot_actions(df, ax, pitch):

    goal = df[df['typeId'] == 16]
    shot_miss = df[df['typeId'] == 13]
    shot_post = df[df['typeId'] == 14]
    shot_saved = df[df['typeId'] == 15]
    recovery = df[df['typeId'] == 49]
    offside = df[df['typeId'] == 55]
    shield = df[df['typeId'] ==56]

    tackle = df[df['typeId'] == 7]
    succ_tackle = tackle[tackle['outcome'] == 1]

    interception  = df[df['typeId'] == 8]
    block = df[df['typeId'] == 10]
    clearance = df[df['typeId'] == 12]

    foul = df[df['typeId'] == 4]
    foul_won = foul[foul['outcome'] == 1]

    dribble = df[df['typeId'] == 3]
    succ_dribble = dribble[dribble['outcome'] == 1]

    aerial = df[df['typeId'] == 44]
    aerial_won = aerial[aerial['outcome'] == 1]

    passes = df[df['typeId'] == 1]

    pickup = df[df['typeId'] == 52]
    punch = df[df['typeId'] == 41]

    kde = pitch.kdeplot(
                  passes.x, passes.y,ax = ax,
                  shade = True,
                  shade_lowest = False,
                  alpha = .5,
                  n_levels = 10,
                  cmap = 'magma')

    ax.scatter(goal['y'], goal['x'], s= 120, c = '#00ff00', edgecolor = '#000000', label = 'Goal')
    ax.scatter(shot_saved['y'], shot_saved['x'], s= 120, c = '#ffea00', edgecolor = '#000000', label = 'Saved/Blocked Shot')
    ax.scatter(shot_post['y'], shot_post['x'], s= 120, c = 'w', edgecolor = '#000000', label = 'Shot Off Woodwork')
    ax.scatter(shot_miss['y'], shot_miss['x'], s= 120, c = 'r', edgecolor = '#000000', label = 'Shot Off Target')
    ax.scatter(succ_dribble['y'], succ_dribble['x'], s= 120, c = '#dc6601', marker = 'X', edgecolor = '#000000', label = 'Dribble')
    ax.scatter(foul_won['y'], foul_won['x'], s= 120, c = '#009afd', marker = 'X', edgecolor = '#000000', label = 'Foul Won')
    ax.scatter(tackle['y'], tackle['x'], s= 100,c = 'w', marker = ',', edgecolor = '#000000', label = 'Tackle')
    ax.scatter(recovery['y'], recovery['x'], s= 100, c = '#ffea00', marker = ',', edgecolor = '#000000', label = 'Ball Recovery')
    ax.scatter(interception['y'], interception['x'], s = 100, c = '#ff007f', marker = ',', edgecolor = '#000000', label = 'Interception')
    ax.scatter(block['y'], block['x'], s = 100, c = '#008080', marker = ',', edgecolor = '#000000', label ='Block/Save')
    ax.scatter(clearance['y'], clearance['x'], s = 120, c = '#dd571c', marker = '^', edgecolor = '#000000', label = 'Clearance')
    ax.scatter(aerial_won['y'], aerial_won['x'], s = 100, c = '#9999ff', marker = '^', edgecolor = '#000000', label = 'Aerial Won')
    ax.scatter(offside['y'], offside['x'], s= 120, c = 'r', marker = 'P', edgecolor = '#000000', label = 'Offside Provoked')
    ax.scatter(shield['y'], shield['x'], s = 120, c = '#dd571c', marker = 'H', edgecolor = '#000000', label = 'Shielding Ball Out')
    ax.scatter(punch['y'], punch['x'], s = 100, c = '#ff007f', marker = '^', edgecolor = '#000000', label = 'Keeper Punch')
    ax.scatter(pickup['y'], pickup['x'], s = 100, c = '#dd571c', marker = 'P', edgecolor = '#000000', label = 'Keeper Pick-Up')

    ax.legend(loc = 'best', bbox_to_anchor=(1.16,0.01), framealpha = 0.6, ncol = 4, edgecolor = '#000000')


plot_actions(filtered_data, ax, pitch)

st.pyplot(fig)


