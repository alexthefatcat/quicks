# -*- coding: utf-8 -*-
r"""
Created on Thu Feb 20 16:12:06 2025

@author: alexm

Streamlit Example


#---------------------------------------------------------------
# conda prompt
# cd "C:\Users\alexm\OneDrive\Documents\GitHub\quicks\STREAMLIT"
# streamlit run streamlit_example.py
# streamlit run "C:\Users\alexm\OneDrive\Documents\GitHub\quicks\STREAMLIT\streamlit_example.py"

# Local URL: http://localhost:8501
# Network URL: http://192.168.1.79:8501
#---------------------------------------------------------------
  
   -> only run certain sections
   -> interactive graphs plotly?
  
  
   *> headers on the left
   *> click moves page to that section
  
  
Download Button
Click On Image: https://github.com/andfanilo/streamlit-drawable-canvas

pages naviagtion
navbar title
interactive graphs
function inputs outputs


top third party streamlit

dashboard


stages

i want the sidebar also to contain sections of the current page
which if you click on will move you down to that section


pages https://www.youtube.com/watch?v=o8p7uQCGD0U

allows you to edit
st.data_editor(df)

st.table(df) simple tabble
st.dataframe
placeholder
"""










import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
sys.path.append(r'C:\Users\alexm\OneDrive\Documents\GitHub\quicks')
from quick_example import image, film_df, func_nth_prime, text, pokemon_df

import streamlit as st


def get_function_info(func):
    import inspect
    signature = inspect.signature(func)
    parameters = signature.parameters
    help_message = inspect.getdoc(func)
    
    out = [[],{},None,None]
    
    for k,v in parameters.items():
        if v.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if v.default is inspect.Parameter.empty:
                out[0].append(k)
            else:
                out[1][k] = v.default      
        if v.kind == inspect.Parameter.VAR_POSITIONAL:
                out[2] =  k        
        
        if v.kind == inspect.Parameter.VAR_KEYWORD:
                out[3] =  k  
    return func.__name__, help_message, out



def line_no():
    import inspect
    return inspect.currentframe().f_back.f_lineno


def write_line_no():
    import inspect    
    line_number = inspect.currentframe().f_back.f_lineno
    st.markdown(f'<p style="color:red;">#line_no: {line_number}</p>', unsafe_allow_html=True)


if False:
    def func(a,b=4,c=4,*d,**e):
        'This is a function'
        return None   
    print(get_function_info(func))   

def basic_show_function(func, title=None):
    func_name, func_help, out = get_function_info(func)

    if title is None:
        st.write(func_name)
    else:
        st.write(title+':('+func_name+')')
    
    if func_help is not None:
        st.write(func_help)
    
    param_names = out[0]+list(out[1].keys())
    
    col_size = [2 for e in param_names]+ [len(param_names),len(param_names)]
    *columns,answer,blank = st.columns(col_size)
    
    func_inputs = []
    for i, (param_name, column) in enumerate(zip(param_names, columns)):
        func_inputs.append(columns[i].number_input(param_name, value=1, key='_'.join([func_name, param_name]))) 
        
    
    func_out =  str(func(  *[int(e) for e in func_inputs]   ))  
    
    
    answer.markdown(
        f"""    <div style="color: black; font-size: 16px; border: 1px solid #ccc; 
                            padding: 5px; border-radius: 4px; text-align: center; 
                            height: 38px; display: flex; align-items: center; justify-content: center; 
                            margin-top: 30px;">  <!-- Adds space above the box -->
                    {func_out}</div> """,
        unsafe_allow_html=True   )
    

def markdown__make_buttons_squashed():
    st.markdown("""
                <style>
                    div[data-testid="stColumn"] {
                        width: fit-content !important;
                        flex: unset;
                    }
                    div[data-testid="stColumn"] * {
                        width: fit-content !important;
                    }
                </style>
                """, unsafe_allow_html=True)

#-----------------------------------------------------------------------------

import plotly.express as px
from random import uniform




    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




with st.expander('Plotly Express', expanded=True):
    
    df_well = pd.DataFrame(columns=['NPHI', 'RHOB', 'GROUP'], )
    
    for i, group in enumerate(('London', 'Paris', 'Berlin')):
        for n in range(500):
            a = uniform(1,11)
            b = uniform(0,0.2)
            c = uniform(-.8,.8)
            out = (((a+20)*1+((i+b)/2)))+c
            df_well.loc[len(df_well)] = [a, out, group]

    fig = px.scatter(df_well, x='NPHI', y='RHOB',  color='GROUP',template='seaborn')
    
    st.plotly_chart(fig)
    
    
    fig = px.histogram(df_well[df_well['NPHI']<4], x='RHOB',  color='GROUP', opacity=0.6,barmode='overlay',template='seaborn',nbins=40)
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    
    st.plotly_chart(fig)
       



with st.expander('Dynamic Stages', expanded=True):

    if "info" not in st.session_state:
        st.session_state.info = {'step':1}
    
    def change_step(step, name, age):
        st.session_state.info['step'] = step
        st.session_state.info['name'] = name
        st.session_state.info['age'] = age
    
    @st.fragment()
    def stages():
        st.header('Dynamic Stages')
        st.text('''                also why are \\t not working I want to make a section a certian minimum size as i know later
                something will be inserted which will change its size''')
        step = lambda : st.session_state.info['step']
        
        name, age = st.session_state.info.get('name',''), st.session_state.info.get('age','')
        
        if step() == 1:
            st.subheader('Part 1: Enter Name')
            name = st.text_input('Name', value= st.session_state.info.get('name',''))
            
        if step() == 2:
            st.subheader('Part 2: Enter Age')
            age = st.text_input('Age', value= st.session_state.info.get('age',''))
            
        if step() == 3:
            st.subheader('Part 3: Check Details')
            
            st.write(f'Is the following correct?\n\tname:{name}\n\t age:{age}')
            if st.button('Submit'):
                st.success('Great')
                st.balloons()
                if False:
                    info = st.session_state.info
                    st.session_state.info = {'step':1,'prev':info}
        markdown__make_buttons_squashed()
        col1, col2, col3,*space = st.columns(3)
        
        prev_button  = col1.button('Previous', on_click=lambda :change_step(step()-1, name, age), disabled=step()<2)         
        next_button  = col2.button('Next' , on_click=lambda :change_step(step()+1, name, age),  disabled=step()>2)        
        rerun_button = col3.button('Run Rest Of Script')        
        st.text(f'Info From Above\n\tname:{name}\n\t age:{age}')  
        
        if rerun_button:
            st.rerun()
                            
    stages()
    st.divider()    
    name, age = st.session_state.info.get('name',''), st.session_state.info.get('age','')
    st.text(f'Info From Above\n\tname:{name}\n\t age:{age}')     

    







# import streamlit as st

# # Simulate page state (for example purposes)
# current_page = st.number_input("Page Number", min_value=1, max_value=10, step=1)

# # Display Previous and Next buttons
# col1, col2 = st.columns([1, 1])

# with col1:
#     if current_page > 1:
#         if st.button("Previous"):
#             st.write("Previous button clicked!")
#     else:
#         st.markdown(
#             """
#             <style>
#             .disabled-button {
#                 pointer-events: none;
#                 color: grey;
#                 background-color: #f0f0f0;
#                 border: 1px solid #ccc;
#                 padding: 0.5em 1em;
#                 border-radius: 5px;
#                 cursor: not-allowed;
#             }
#             </style>
#             <button class="disabled-button">Previous</button>
#             """,
#             unsafe_allow_html=True
#         )

# with col2:
#     if current_page < 10:  # Assuming 10 is the last page
#         if st.button("Next"):
#             st.write("Next button clicked!")
#     else:
#         st.markdown(
#             """
#             <style>
#             .disabled-button {
#                 pointer-events: none;
#                 color: grey;
#                 background-color: #f0f0f0;
#                 border: 1px solid #ccc;
#                 padding: 0.5em 1em;
#                 border-radius: 5px;
#                 cursor: not-allowed;
#             }
#             </style>
#             <button class="disabled-button">Next</button>
#             """,
#             unsafe_allow_html=True
#         )


 
#%%----------------------------------------------------------------------------
# conda prompt
# cd "C:\Users\alexm\OneDrive\Documents\GitHub\quicks\STREAMLIT"
# streamlit run streamlit_example.py

  # Local URL: http://localhost:8501
  # Network URL: http://192.168.1.79:8501
 #%%---------------------------------------------------------------------------- 
image2 = (254*(image/image.max())).astype('uint8')

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    sidebar_input = st.text_input('Enter some text')
st.header("Welcome to My Streamlit App")
    

 
 


st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app.")

pressed = st.button('I am a button')


#------------------------------------------------------------------------------
def multiply(a,b):
    return a*b

with st.expander('Text', expanded=True):
    #This still needs to be done
    
    st.write("""title, header, subheader, header, text
             write -> is quick general way to output anything acts like text if string
             markdown, caption(explains image above), code(code), latex(formula)
             divider
             st.echo I havent donw here pretty cool
             st.html
             also how to change the background color of certain words
             
             """)    
    
    
    st.title("Example of Text")
    st.title("st.title('text', help='tooltip*')",help='tooltip*') 
    
    
    st.title("_Streamlit_ is :blue[cool] :sunglasses:")
    
    st.title("title")
    st.header("_Streamlit_ is :blue[cool] :sunglasses:")
    st.header("This is a header with a divider", divider="gray")
    st.header("These headers have rotating dividers", divider=True)
        
    st.subheader("subheader")
    st.subheader("This is a subheader with a divider", divider="gray")
    st.subheader("One", divider=True)
    st.subheader("Two", divider=True)
    st.write("This is some text.")
    st.caption("A caption, typically __explaines__ somethign above with _italics_ :blue[colors] and emojis :sunglasses:")
    st.divider()
    st.text("This is text\n[and more text](that's not a Markdown link).")   
    st.write("""
    - **Bold Text Example**: Streamlit is **awesome**!
    - *Italicized Text Example*: Learning Streamlit is *fun*.
    - Highlight Text with Colors: :blue[Blue text], :green[Green text], :red[Red text].
    - Emojis to Add Personality: :sparkles: :smile: :rocket:
    - Combining Styles: This is **bold**, *italicized*, :red[colored], and even with emojis :star:
    - Strikethrough Example: ~~This text is crossed out~~.
    - Inline Code: Here's some `inline code` for display.
    - Markdown Quotes: > This is a block quote formatted in Markdown.
    """)
    code = '''def hello():
    print("Hello, Streamlit!")'''
    st.code(code, language="python")
    st.latex(r'''
        a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
        \sum_{k=0}^{n-1} ar^k =
        a \left(\frac{1-r^{n}}{1-r}\right)
        ''')    


    st.markdown("*Streamlit* is **really** ***cool***.")
    st.markdown('''
        :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
        :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
    st.markdown("Here's a bouquet &mdash;\
                :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")
    
    multi = '''If you end a line with two spaces,
    a soft return is used for the next line.
    
    Two (or more) newline characters in a row will result in a hard return.
    '''
    st.markdown(multi)
    
    
    
    #--live markdown
    md = st.text_area('Type in your markdown string (without outer quotes)',
                  "Happy Streamlit-ing! :balloon:")
    st.code(f"""
    import streamlit as st
    
    st.markdown('''{md}''')
    """)
    st.markdown(md)







import base64

# List of image paths
image_paths = [
    r"C:\Users\alexm\Downloads\90276_16__web.jpg",
    r"C:\Users\alexm\Downloads\15229_4__web.jpg",
    r"C:\Users\alexm\Downloads\jennifer-clark-topless-001.jpg"
]

# Initialize session state for image index
if "image_index" not in st.session_state:
    st.session_state.image_index = 0

# Function to navigate images
def navigate_images(direction):
    if direction == "next":
        st.session_state.image_index = (st.session_state.image_index + 1) % len(image_paths)
    elif direction == "prev":
        st.session_state.image_index = (st.session_state.image_index - 1) % len(image_paths)

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Get the current image as base64
image_base64 = image_to_base64(image_paths[st.session_state.image_index])




col1, _, col2 = st.columns([1, 2, 1])  # Add a narrower column between col1 and col2
with col1:
    if st.button("⬅️ Previous"):
        navigate_images("prev")
with col2:
    if st.button("Next ➡️"):
        navigate_images("next")



# Display image with overlay arrows using CSS
st.markdown(
    f"""
    <style>
        .image-container {{
            position: relative;
            text-align: center;
        }}
        .image-container img {{
            width: 100%;
            height: auto;
        }}
        .arrow {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background-color: rgba(0, 0, 0, 0.5);
            border: none;
            color: white;
            font-size: 24px;
            padding: 10px;
            cursor: pointer;
            z-index: 10;
        }}
        .arrow-left {{
            left: 10px;
        }}
        .arrow-right {{
            right: 10px;
        }}
    </style>
    <div class="image-container">
        <img src="data:image/jpeg;base64,{image_base64}">
        <button class="arrow arrow-left" onClick="window.location.reload()">&#9664;</button>
        <button class="arrow arrow-right" onClick="window.location.reload()">&#9654;</button>
    </div>
    """,
    unsafe_allow_html=True
)


    


with st.container(key = 'Contaniner-Functions', border=True):
    st.subheader("Functions")
    write_line_no()
    
    col1a, col2a, *colsa = st.columns([2,1,1])
    func_inp = col1a.number_input('Find Nth PrimeNumber', min_value=1, value=100)  
    func_inp2 =  str(func_nth_prime(int(func_inp)))   
    
    col2a.markdown(
       f""" <div style="color: black; font-size: 16px; border: 1px solid #ccc; 
                        padding: 5px; border-radius: 4px; text-align: center; 
                        height: 38px; display: flex; align-items: center; justify-content: center; 
                        margin-top: 30px;">  <!-- Adds space above the box -->  {func_inp2}    </div>    """,
        unsafe_allow_html=True)
    
    st.divider()
    basic_show_function(multiply)
    st.divider()
    basic_show_function(func_nth_prime, 'Find Nth PrimeNumber2')
    
 
#------------------------------------------------------------------------------

from st_keyup import st_keyup
with st.container(key = 'Contaniner-Fruit', border=True):
    st.subheader("Instant Search")
    write_line_no()
    # Notice that value updates after every key press
    data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
    value = st_keyup("Search Fruit:-", placeholder='Type Here ...')
    df = pd.DataFrame([e for e in data if value.lower() in e.lower()])
    html_table = df.to_html(index=False, header=False)
    st.markdown(html_table, unsafe_allow_html=True)

#------------------------------------------------------------------------------

'''
IN the future blocks like containers
can turn on and off doing it
can turn of and on updating the whole thing
have option
SHOW_LINE_NUMBERS = True at top
show code as well
'''

from st_keyup import st_keyup
with st.container(key = 'Contaniner-Animals', border=True):
    
    st.subheader("Animal Images")
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
    
    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)    
    










 
#------------------------------------------------------------------------------

from st_keyup import st_keyup


import streamlit as st

mark_down = """
<div style="display: flex; align-items: center; justify-content: space-between;">
    <div style="font-size: 24px; font-weight: bold;">Instant search</div>
    <div style="font-size: 12px; color: red; font-style: italic;">#45</div></div>
"""



with st.expander(mark_down, expanded=True):
    tab1, tab2 = st.tabs(["UI", "Code"])
    st.subheader("Instant Search")
    
    st.markdown(mark_down, unsafe_allow_html=True)
    
    
    write_line_no()
    # Notice that value updates after every key press
    data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
    value = st_keyup("Search Fruit :-", placeholder='Type Here ...',key='sdfs2')
    df = pd.DataFrame([e for e in data if value.lower() in e.lower()])
    html_table = df.to_html(index=False, header=False)
    st.markdown(html_table, unsafe_allow_html=True)

#------------------------------------------------------------------------------















if True:    
    
    
    
    
    col1, col2 = st.columns(2)
    prime1 = col1.number_input('Prime Number 1', min_value=1, value=100)
    jjjj = col2.caption('\n\n\n ')
    jjjjjj = col2.caption(func_nth_prime(int(prime1)))
    
    
    prime3 = col1.number_input('Prime Number 3', min_value=1, value=20)
    
    prime4 = col2.number_input('Prime Number 4', min_value=1, value=15)   
    
    prime2 = col2.metric(label='Prime', value = func_nth_prime(int(prime1)))
    
    
    age = st.slider("How old are you?", 0, 130, 25)
    st.write("I'm ", age, "years old")
    
    import time
    progress_bar = st.progress(0)
    for perc_completed in range(1,101):
        if 40<perc_completed<49:
            time.sleep(0.1)        
        time.sleep(0.025)
        progress_bar.progress(perc_completed,str(perc_completed)+'%')
    progress_bar.progress(perc_completed, 'Complete')    
    
    st.divider()
    
    
    with st.container(key = 'Contaniner-QuickTablesAndImages', border=True):
        st.subheader("QuickTablesAndImages")
        write_line_no()

        code = '''        st.write(film_df)
        st.image(image2, caption="Example Image", use_container_width =True)
        '''
        
        st.code(code, language='python')


        
        st.write(film_df)
        st.image(image2, caption="Example Image", use_container_width =True)
        
            

    

    
    
    
    
    
    
    
    
    
    
    
    st.title("Searchable Pokemon Table in Streamlit")
    
    st.metric(label='Tempature', value='82 C', delta='3')
    
    def searchable_table(df):
        col1, col2 = st.columns(2)
        option2 = col1.selectbox("Select Column:", list(df.columns))
        options1 = ['',]+list(sorted(df[option2].unique()))
        option1 = col2.selectbox("Choose an option:", options1)
        search_query = st.text_input("Search for pokemon:", key="search_input")
        filtered_df = pokemon_df
        if search_query:
            filtered_df = filtered_df[filtered_df['Name '].str.contains(search_query, case=False)]
        if option1!='':
            filtered_df = filtered_df[filtered_df['Type 1 ']==option1]
        st.dataframe(filtered_df, height=(1+len(filtered_df))*35) # st.write(filtered_df)
    searchable_table(pokemon_df)
    
    
    
    import time
    
    _LOREM_IPSUM = """
    Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
    nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    """
    
    
    def stream_data():
        for word in _LOREM_IPSUM.split(" "):
            yield word + " "
            time.sleep(0.2)
    
        yield pd.DataFrame(
            np.random.randn(5, 10),
            columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        )
    
        for word in _LOREM_IPSUM.split(" "):
            yield word + " "
            time.sleep(0.02)
    
    
    if st.button("Stream data"):
        st.write_stream(stream_data)
    
    
    # Sample data for the line chart
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    temperature = [15, 17, 14, 18, 20, 19, 16]
    
    # st.bar_chart(df)
    # st.line_chart(df)
    # # Sample data for the bar chart
    # products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    # sales = [20, 35, 30, 35, 27]
    # df = pd.DataFrame(data=[sales], columns=products) 
    
    #import matplotlib.pyplot as plt
    # # Create the bar chart
    # plt.figure(figsize=(10, 6))
    # plt.bar(products, sales, color='skyblue')
    # plt.xlabel('Products')
    # plt.ylabel('Sales')
    # plt.title('Sales of Different Products')
    # plt.show()
    
    
    # # Create the line chart
    # plt.figure(figsize=(10, 6))
    # plt.plot(days, temperature, marker='o', linestyle='-', color='tomato')
    # plt.xlabel('Days of the Week')
    # plt.ylabel('Temperature (°C)')
    # plt.title('Temperature Variation Over a Week')
    # plt.grid(True)
    # plt.show()
    
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.plot(x, y, label='Sine Wave')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    
    
    with st.expander("Sin Wave2"):
        st.title("Sine Wave Graph")
        st.write("This is a simple sine wave graph created using Matplotlib and displayed in Streamlit.")
        st.pyplot(fig)
    
    
    with st.popover("Open popover"):
        st.markdown("Hello World 👋")
        name = st.text_input("What's your name?")
        red = st.checkbox("Show name in red", True)
    if red:
        st.write(f":red[Your name:  {name}]")    
    else:
        st.write(f"Your name:  {name}")    
        
        
        
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
    
    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)    
    
    
    
    tab1, tab2 = st.tabs(["UI", "Code"])
    
    with tab1:
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        # Create a figure and axis
        fig, ax = plt.subplots()
        ax.plot(x, y, label='Sine Wave')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        
        with st.expander("Sin Wave2"):
            st.title("Sine Wave Graph")
            st.write("This is a simple sine wave graph created using Matplotlib and displayed in Streamlit.")
            st.pyplot(fig)
    
    with tab2:
        code_text = '''
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        # Create a figure and axis
        fig, ax = plt.subplots()
        ax.plot(x, y, label='Sine Wave')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        
        with st.expander("Sin Wave2"):
            st.title("Sine Wave Graph")
            st.write("This is a simple sine wave graph created using Matplotlib and displayed in Streamlit.")
            st.pyplot(fig)
        '''
        
        # Display the code-like text
        st.code(code_text, language='python')
        
    
    
    
    
    code_text = '''
    def hello_world():
        print("Hello, World!")
    
    if __name__ == "__main__":
        hello_world()
    '''
    
    # Display the code-like text
    st.code(code_text, language='python')
    
    
    with st.form(key = 'Sample Form'):
       st.title("form stuff")
       prime3 = st.number_input('Prime Number 33', min_value=1, value=20)
       st.form_submit_button()
    
    with st.container(key = 'Contaniner-Everton', border=True):
        st.write("I'm  years old")    
        st.write("I'm  dssdcsd years old")
    
    
    
    placeholder = st.empty()
    placeholder.write('click button to change dyanmic content')
    placeholder_changed = 0
    if st.button('change placeholder'):
        if placeholder_changed==0:
            placeholder.write('changed')
            placeholder_changed+=1
        else:
            placeholder.write('changed again')        
        
     
    # Initialize the counter
    if "count" not in st.session_state:
        st.session_state.count = 0
    
    # Define a function to increment the counter
    def increment_counter():
        st.session_state.count += 1
    
    # Create a placeholder for displaying the counter
    placeholder = st.empty()
    
    # Create a button to increment the counter
    if st.button('Increment',help='count the number of clicks'):
        increment_counter()
    
    # Update the placeholder with the current counter value
    placeholder.text(f'Counter: {st.session_state.count}')
    
    
    import streamlit as st
    
    # Define functions for different pages
    def home():
        st.title("Home Page")
        st.write("Welcome to the Home Page!")
    
    def about():
        st.title("About Page")
        st.write("This is the About Page.")
    
    def contact():
        st.title("Contact Page")
        st.write("This is the Contact Page.")
    st.sidebar.markdown('---')
    # Create a sidebar for navigation
    menu = st.sidebar.radio("Navigation", ["Home", "About", "Contact"])
    st.sidebar.divider()
    # Render the selected page
    if menu == "Home":
        home()
    elif menu == "About":
        about()
    elif menu == "Contact":
        contact()
    
        
    
    my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    #st.sidebar.download_button("Download fixed image", image2, "fixed.png", "image/png")
    
    
     
    # Define a function to create sections
    def section(title):
        st.markdown(f"<h2 id='{title}'>{title}</h2>", unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    section_options = ["Home", "About", "Contact", "Section 1", "Section 2"]
    selected_section = st.sidebar.selectbox("Go to", section_options)
    
    # Scroll to the selected section
    st.markdown(f"<script>document.getElementById('{selected_section}').scrollIntoView();</script>", unsafe_allow_html=True)
    
    # Main content
    st.title("Multi-section App")
    section("Home")
    st.write("Welcome to the Home Page!")
    section("About")
    st.write("This is the About Page.")
    section("Contact")
    st.write("This is the Contact Page.")
    section("Section 1")
    st.write("Content for Section 1.")
    section("Section 2")
    st.write("Content for Section 2.")
    


