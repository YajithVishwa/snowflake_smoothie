# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie
    """
)

order_name = st.text_input("Name of Order", "", placeholder='Tommy')

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME')
#st.dataframe(data=my_dataframe, use_container_width=True)

ing_list = st.multiselect('Choose up to 5 ing', my_dataframe, max_selections=5)

if ing_list:
    ingredients_string = ', '.join(ing_list)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + order_name + """')"""
    if st.button("Submit"):
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered for {order_name}!', icon="✅")