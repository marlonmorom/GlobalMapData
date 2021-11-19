import plotly.graph_objects as go
import pandas as pd
from tkinter import *

#-----DataFrame Initialization-----
df = pd.read_csv('countries of the world.csv',decimal=',') #reading the csv file, using , as decimal separator
df_PT = pd.read_csv('pais_br.csv') #reading the csv file containing the countries' names translation

df.set_index('Country',inplace=True)
df_PT.set_index('Country',inplace=True)

df = df.join(df_PT,on='Country') #doing a join to fetch the names translation
df.reset_index(inplace=True) #reseting the index, making 'Country' a column again
df['País'].fillna(df['Country'],inplace=True) #replacing the values that had no match with the original names

df.reset_index(inplace=True)

#-----Translating the columns-----
#dictionary containing the translation of the columns
traducao = {'Area (sq. mi.)':'Área (milha quadrada)',
            'Population' : 'População',
            'Infant mortality (per 1000 births)' : 'Mortalidade Infantil (por 1000 nascimentos)',
            'GDP ($ per capita)' : 'PIB ($ per capita)',
            'Literacy (%)':'Alfabetização (%)'
            }

colunas_EN = sorted('Area (sq. mi.)/Population/Infant mortality (per 1000 births)/GDP ($ per capita)/Literacy (%)'.split('/'))
colunas_PT = sorted(list(map(lambda x: traducao[x],colunas_EN)))

def plot_EN():
    global pt
    pt = False
    botaoEN.destroy()
    botaoPT.destroy()
    entrada.destroy()
    
    #creating buttons dynamically
    for i,coluna in enumerate(colunas_EN):
        botao = (Button(root, text= coluna,command=lambda coluna=coluna:plot_map(coluna),width=40,
                 background='#4A706B', fg='white', font=('verdana', 10, 'bold')))
        botao.grid(padx=posx,pady=10,row = i)

def plot_PT():
    global pt
    pt = True
    botaoEN.destroy()
    botaoPT.destroy()
    entrada.destroy()
    
    #creating buttons dynamically
    for i,coluna in enumerate(colunas_EN):
        botao = (Button(root, text= traducao[coluna],command=lambda coluna=coluna:plot_map(coluna),width=40,
                 background='#4A706B', fg='white', font=('verdana', 10, 'bold')))
        botao.grid(padx=posx,pady=10,row = i)

def plot_map(column):
    #checking if portuguese was chosen, to set the text properly
    if pt == True:
        texto = 'País'
    else:
        texto = 'Country'
    fig = go.Figure(data=go.Choropleth(
        locationmode = 'country names',
        locations = df['Country'],
        z = df[column],
        text = df[texto],
        colorscale = 'YlGnBu',
        marker_line_color='darkgray',
        marker_line_width=0.5,
        hoverinfo = 'z+text',
    
    ))
    if pt == True:
        column = traducao[column]
    fig.update_layout(
        title_text=column,
        height = 800,
        width = 1800,
        geo=dict(
            showframe=True,
            projection_type='robinson'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
        )]
    
    )
    fig.show()

    
# -----creating the main screen-----
root = Tk()
root.configure(background='#CCF0EB')
userScreenWidth = root.winfo_screenwidth()
userScreenHeight = root.winfo_screenheight()
root.geometry("%dx%d" % (userScreenWidth, userScreenHeight))

mainText = StringVar()
mainText.set(
    'Selecione o idioma\n\nChoose your language')

entrada = Label(
    root,
    justify='center',
    font="Verdana 30",
    textvariable=mainText,
    borderwidth=4,
    background='#1F5750',
    fg='white',
    relief='solid',
)

posyBottom = 10  
labelHeight = entrada.winfo_reqheight()  # the Label's required height
labelWidth = entrada.winfo_reqwidth() # the Label's required width
factorPosy = 0.3  # displacement factor, in the vertical direction
posy = (userScreenHeight/2-labelHeight/2)*factorPosy # placing the label vertically in the middle of the user screen
posx = (userScreenWidth/2-labelWidth/2) # placing the label horizontally in the middle of the user screen

# -----main Buttons-----
botaoPT = Button(root, text='PT-BR', command=plot_PT, width=10,
                 background='#4A706B', fg='white', font=('verdana', 10, 'bold'))
botaoEN = Button(root, text='EN-US', command=plot_EN, width=10,
                 background='#4A706B', fg='white', font=('verdana', 10, 'bold'))


entrada.grid(padx=posx, pady=(posy, posyBottom), sticky="NESW")
botaoPT.grid(pady=5)
botaoEN.grid()

root.title("Mapa Mundi / World Map")
root.mainloop()
