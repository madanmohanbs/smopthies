# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw:  Customize your Smoothies")
st.write(
  """
  **Choose your fruits in your Smooties** .
  """
)

name_of_order = st.text_input('Order Name')
st.write('Name of order: '+ name_of_order)

cnx = st.connection("snowflake")
session = cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas();
st.dataframe(data=pd_df, use_container_width=True)
st.stop()


ingrediants = st.multiselect('Choose upto 5 fruits',my_dataframe,max_selections=5)
if ingrediants:
    #st.write(ingrediants)
    #st.text(ingrediants)
    
    ingredients_string=''
    for fruit in ingrediants:
        ingredients_string += fruit+ ' '
        st.subheader("ingredients of :"+fruit)
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit)
        #st.text(smoothiefroot_response.json())
        sfdf = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    st.write(ingredients_string) 

    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients,name_on_order)
            values ('{ingredients_string}','{name_of_order}')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
    #st.write(my_insert_stmt)
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!'+name_of_order, icon="✅")

#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
#sfdf = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
