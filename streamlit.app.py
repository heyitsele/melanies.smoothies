# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# App title
st.title(":cup_with_straw: Pending Smoothie Orders! :cup_with_straw:")
st.write("""Orders that need to be filled.""")

# Filter for orders that are not yet filled
session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == False).collect()

if my_dataframe:
    editable_df = st.experimental_data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:

        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success('Order(s) Updated!', icon = "👍")
        except:
            st.write('Something went wrong.')
            
else:
    st.success('There are no pending orders right now', icon = "👍")
    

#st.write("""
 #   Below are the pending smoothie orders. 
  #  You can mark them as filled using the checkboxes, but saving changes will be handled later.
#""")


    #st.success('Someone clicked the button', icon = '👍')
    
    #og_dataset = session.table("smoothies.public.orders")
    #edited_dataset = session.create_dataframe(editable_df)
    
