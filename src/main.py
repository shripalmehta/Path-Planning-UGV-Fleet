import streamlit as st

def main():
    st.title("Road Fixer")

    # Input for number of bots
    num_bots = st.number_input("Enter the number of bots in the fleet:", min_value=1, value=1, step=1)

    # Input for payload capacity
    payload_capacity = st.number_input("Enter the payload capacity for all bots (in kg):", min_value=0.1, value=100.0, step=0.1)

    # Display the entered values
    st.write(f"Fleet size: {num_bots} bot{'s' if num_bots > 1 else ''}")
    st.write(f"Payload capacity per bot: {payload_capacity} kg")

if __name__ == "__main__":
    main()