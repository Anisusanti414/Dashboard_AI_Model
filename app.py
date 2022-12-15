# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import statistics as st
from statistics import mode
import pandas as pd
import plotly.express as px

print('BERHASIL')

# 2. Create a Dash app instance
app = dash.Dash(
    external_stylesheets=[dbc.themes.SANDSTONE],
    name = 'Mining Eyes Analytics'
)

## --- Title
app.title = 'Mining Eyes Analytics'

## --- Navbar

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("Data_Train", href="#"), #header=True),
        #         dbc.DropdownMenuItem("Data_Validation", href="#"),
        #         # dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="Data_Train",
        # ),
    ],
    brand="Mining Eyes Analytics",
    brand_href="#",
    color="success",
    dark=True,
)

## Import Dataset gpp
training = pd.read_csv('data_input/training.csv')
data = pd.read_csv('data_input/Site.csv')
akurasi = pd.read_csv('data_input/akurasi.csv')

dev = pd.read_csv('data_input/Data_deviasi.csv')
dev = dev[dev['Jumlah Deviasi']<500]
dev_val = dev[dev['type_validation'] != 'not_yet']
data_validasi = pd.read_csv('data_input/val.csv')

### CARD CONTENT
total_hd = 180
total_lv = 259
total_person = 234
## -- VISUALIZATION

#PIE SITE
pie_site = px.pie(
    data,
    values='Jumlah dataset',
    names='Site',
    color_discrete_sequence=['darkgreen','green','lightgreen','aquamarine','springgreen','yellowgreen'],
    template='ggplot2',
     title='Distribution Dataset Each Site',
    hole=0.4
)

## BAR TOTAL ANOTASI
count_id = pd.crosstab(index=training['Object_id'],
            columns='Jumlah_Object',
            values=training['Object_id'],
            aggfunc='count')
count_id.reset_index(inplace=True)

bar_object = px.bar(
    count_id.sort_values('Jumlah_Object', ascending = False),
    x = 'Object_id',
    y = 'Jumlah_Object',
    color_discrete_sequence=['darkgreen'],
    title='Total Data Training for Each Object'
)


## BOXPLOT AREA ANOTASI
box_area = px.box(
    training.sort_values('Object_id'),
    x = 'Object_id',
    y = 'Area',
    color_discrete_sequence=['darkgreen'],
       title='Area Distribution of Each Object'
)

# ## CARD
# map= [
#     dbc.CardHeader('Number of MAP (%)'),
#     dbc.CardBody([
#         html.H1(akurasi['MAP(%)'].mean())
#     ]),
# ]

# akurasi_mean = [
#     dbc.CardHeader('Number of Accuracy'),
#     dbc.CardBody([
#         html.H1(akurasi['Accuracy(%)'].mean().round(2))
#     ]),
# ]


# ## BAR ACCURACY
# bar_acc = px.bar(
#     akurasi.sort_values('Accuracy(%)', ascending = False),
#     x = 'Object',
#     y = 'Accuracy(%)',
#     color_discrete_sequence=['darkgreen'],
#     title='Accuration Each Object'

# )

############EVALUATION
## -- CARD
total_deviasi = [
    dbc.CardHeader('Number of Data Deviation'),
    dbc.CardBody([
        html.H1(dev['Jumlah Deviasi'].sum())
    ]),
]

total_validasi = [
    dbc.CardHeader('Number of Data Validation'),
    dbc.CardBody([
        html.H1(dev_val['Jumlah Deviasi'].sum())
    ]),
]

## LINE
dev_day = pd.crosstab(index=[dev['Tanggal'],dev['type_validation']],
            columns='Jumlah_gambar',
            values=dev['Jumlah Deviasi'],
            aggfunc='sum')

dev_day.reset_index(inplace=True)
dev_day['Val'] = dev_day['type_validation']

for i in range(0,len(dev_day)):
    if dev_day['Val'][i] == 'not_yet':
        dev_day['Val'][i] = 'not'
    else:
        dev_day['Val'][i]= 'yes'

line_day = px.line(
    dev_day, 
    x="Tanggal", 
    y="Jumlah_gambar", 
    color = 'Val',
    labels = {
    'Jumlah_gambar':'Total Deviation',
    'Tanggal':'Date',
    'Val' : 'Already Validated?'},
    color_discrete_sequence=['Green','red'],
    title='Number of deviations that have been validated and have not been validated'
             
             )


## PIE VALIDATION
validasi = pd.crosstab(index=[data_validasi['Object'],data_validasi['Deviasi (T/F)']],
            columns='sum of deviation',
            values=data_validasi['Deviasi (T/F)'],
            aggfunc='count')
validasi.reset_index(inplace=True)

pie_val = px.pie(
    validasi,
    values='sum of deviation',
    names='Deviasi (T/F)',
    color_discrete_sequence=['darkgreen','red'],
    template='ggplot2',
    title = 'Proportion True & False',
    hole=0.4
)

## BAR VALIDATION
bar_val = px.bar(
    validasi.sort_values('sum of deviation', ascending = False),
    x = 'Object',
    y = 'sum of deviation',
    color = 'Deviasi (T/F)',
    color_discrete_sequence=['darkgreen','red'],
    title='Number of Data Validation',
    labels = {
        'Deviasi (T/F)':'Deviation?'},
   barmode='group'
)

# ## Pie False
# validasi_false = pd.crosstab(index=[data_validasi['Object'],data_validasi['F1/F2']],
#             columns='sum of deviation',
#             values=data_validasi['Deviasi (T/F)'],
#             aggfunc='count')
# validasi_false.reset_index(inplace=True)

# pie_false = px.pie(
#     validasi_false,
#     values='sum of deviation',
#     names='F1/F2',
#     #color = 'Object'
#     color_discrete_sequence=['darkgreen','lightgreen'],
#     template='ggplot2',
#     title = 'Proportion False Type 1 and False Type 2',
#     hole=0.4
# )

## --- LAYOUT
app.layout = html.Div(children=[
    navbar,

    html.Br(),

    ## -- Component Main Page --
    html.Div([

        ## -- ROW 1 --
        dbc.Row([
            ## -- COLUMN 1
            dbc.Col([
                #html.H1('Analysis Mining Eyes Analytics'),
                dbc.Tabs([
                    ##--- TAB 1 : RANGKING
                    dbc.Tab([
                        ## ROW 1
                        dbc.Row([
                            ##--COLUMN 1
                            dbc.Col([ 
                                dbc.Card([
                                dbc.CardHeader('Select Model'),
                                dbc.CardBody(
                                    dcc.Dropdown(
                                        id='choose_model',
                                        options = akurasi['Model'].unique(),
                                        value = 1,
                                    ),
                                ),
                            ]),
                                html.Br(),
                                dbc.Card(id = 'map', color = 'green' ,),
                                html.Br(),
                                dbc.Card(id = 'akurasi_mean',color = 'lightgreen',),
                                html.Br(),

                            ], 
                            width = 4),

                            ## COLLUMN 2
                            dbc.Col(
                                [html.H4('Analysis of Distribution Model Mining Eyes Analytics'),

                                dcc.Graph(
                                    id='acc',
                                    #figure = bar_acc,
                                ),      
                                # dbc.Tab(
                                #     dcc.Graph(
                                #         id='acc',
                                #         figure = bar_acc,

                                #     ),
                                #     label = 'dist_acc'
                                # )
                                    
                                ],
                                width = 8),
                        ]),

                       
                        ### ROW 3
                        dbc.Row([
                            ## -- COLUMN 1
                                dbc.Col(
                                    ## -- Isi ada brapa banyak card
                                    [#html.H3('Distribution Dataset Training'),
                                    dbc.Tab(
                                        dcc.Graph(
                                            id='plot_site',
                                            figure = pie_site,

                                        ),
                                        label = 'Dist_Site'
                                    )
                                        
                                    ],
                                    width = 4),

                            ## -- COLUMN 2
                                dbc.Col(
                                    ## -- Isi ada brapa banyak card
                                    [
                                    dbc.Tab(
                                        dcc.Graph(
                                            id='plot_object',
                                            figure = bar_object,

                                        ),
                                        label = 'Dist_object'
                                    )
                                        
                                    ],
                                    width = 4),

                            ## -- COLUMN 3
                                dbc.Col(
                                    ## -- Isi ada brapa banyak card
                                    [
                                    dbc.Tab(
                                        dcc.Graph(
                                            id='plot_area',
                                            figure = box_area,

                                        ),
                                        label = 'Dist_area'
                                    )
                                        
                                    ],
                                    width = 4),

                        ]),
                        html.Hr()],

                        label = 'Model'),

                        

                    ## -- TAB 2 : DISTRIBUTION
                    dbc.Tab([
                    ### ROW 1
                        dbc.Row([
                            ##--COLUMN 1
                            dbc.Col([ html.H4('Analysis of Mining Eyes Analytics'),
                                html.Br(),
                                html.Br(),
                                dbc.Card(total_deviasi, color = 'green' ,),
                                html.Br(),
                                dbc.Card(total_validasi,color = 'lightgreen',),
                                html.Br(),

                            ], 
                            width = 4),

                            ## COLLUMN 2
                            dbc.Col(
                                [
                                dbc.Tab(
                                    dcc.Graph(
                                        id='dev_day',
                                        figure = line_day,

                                    ),
                                    label = 'dist_acc'
                                )
                                    
                                ],
                                width = 8),

                        ]),

                         ### ROW 2
                        dbc.Row([
                            ## -- COLUMN 1
                            dbc.Col([
                                html.H2('Analysis Dataset Validation Mining Eyes Analytics'),
                            ], 
                            width = 9),
                            ## -- COLUMN 2
                            dbc.Col([
                                dcc.Dropdown(
                                    id='choose_object',
                                    options = data_validasi['Object'].unique(),
                                    value = 'HD',
                                    ),
                            ],
                            width = 3),
                        ]),

                        ### ROW 3
                        dbc.Row([
                            ## -- COLUMN 1
                            dbc.Col(
                                [
                                dbc.Tab(
                                    dcc.Graph(
                                        id='pie_val',
                                        figure = pie_val,

                                    ),
                                    label = 'pie_val'
                                )
                                    
                                ],
                                width = 4),
                                

                            ## -- COLUMN 2

                            dbc.Col(
                                [
                                dbc.Tab(
                                    dcc.Graph(
                                        id='dev_val_object',
                                        figure = bar_val,

                                    ),
                                    label = 'bar_val'
                                )
                                    
                                ],
                                width = 4),
                                

                            ## -- COLUMN 3
                             dbc.Col(
                                [
                                
                                
                                # dcc.Dropdown(
                                #     id='choose_object',
                                #     options = data_validasi['Object'].unique(),
                                #     value = 'HD',
                                #     ),
                                   
                                dbc.Tab(
                                    dcc.Graph(
                                        id='pie_false',
                                        #figure = pie_false,

                                    ),
                                    label = 'pie_false'
                                )
                                    
                                ],
                                width = 4),   

                        ]),
                        html.Hr(),


                    ],
                    label = 'Evaluation'),
                ]),
            ],width = 12),
            ## -- COLUMN 2
        ]),


    ],style={
        'paddingLeft':'30px',
        'paddingRight':'30px'
    } 
    
    )
    #html.H1(children='Dashboard Overview'), #judul dashboard

])

### CALLBACK bar acc
@app.callback(
    Output(component_id='acc', component_property='figure'),
    Input(component_id='choose_model',component_property='value')
)

def update_plot3(model_name):
    akurasi_model = akurasi[akurasi['Model']==model_name]
    
    #Visualization
## BAR ACCURACY
    bar_acc = px.bar(
        akurasi_model.sort_values('Accuracy(%)', ascending = False),
        x = 'Object',
        y = 'Accuracy(%)',
        color_discrete_sequence=['darkgreen'],
        title='Accuration Each Object'

    )
    return bar_acc

### CALLBACK card MAP
@app.callback(
    Output(component_id='map', component_property='children'),
    Input(component_id='choose_model',component_property='value')
)

def update_plot3(model_name):
    akurasi_model = akurasi[akurasi['Model']==model_name]
    
    ## CARD
    map= [
        dbc.CardHeader('Number of MAP (%)'),
        dbc.CardBody([
            html.H1(akurasi_model['MAP(%)'].mean())
        ]),
    ]

    return map

### CALLBACK card Akurasi
@app.callback(
    Output(component_id='akurasi_mean', component_property='children'),
    Input(component_id='choose_model',component_property='value')
)

def update_plot3(model_name):
    akurasi_model = akurasi[akurasi['Model']==model_name]
    
    ## CARD
    akurasi_mean = [
    dbc.CardHeader('Number of Accuracy (%)'),
    dbc.CardBody([
        html.H1(akurasi_model['Accuracy(%)'].mean().round(2))
    ]),
    ]


    return akurasi_mean

## CALLBACK pie false
@app.callback(
    Output(component_id='pie_false', component_property='figure'),
    Input(component_id='choose_object',component_property='value')
)

def update_plot3(object_name):
    validasi_false = data_validasi[data_validasi['Object']==object_name]

    # Pie False
    validasi_false = pd.crosstab(index=[validasi_false['Object'],validasi_false['F1/F2']],
                columns='sum of deviation',
                values=validasi_false['Deviasi (T/F)'],
                aggfunc='count')
    validasi_false.reset_index(inplace=True)

    ## CARD
    pie_false = px.pie(
    validasi_false,
    values='sum of deviation',
    names='F1/F2',
    #color = 'Object'
    color_discrete_sequence=['darkgreen','lightgreen'],
    template='ggplot2',
    title = 'Proportion False Type 1 and False Type 2',
    hole=0.4
    )



    return pie_false






## 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()