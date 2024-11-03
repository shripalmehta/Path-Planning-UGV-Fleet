import streamlit as st

def main():
    st.title("Road Fixer")

    # Input for number of bots and payload capacity in the same row
    col1, col2 = st.columns(2)
    with col1:
        num_bots = st.number_input("Number of bots in the fleet:", min_value=1, value=1, step=1)
    with col2:
        payload_capacity = st.number_input("Payload capacity for all bots (kg):", min_value=0.1, value=100.0, step=0.1)

    # Partition line
    st.markdown("---")

    # Display the entered values
    st.write(f"Fleet size: {num_bots} bot{'s' if num_bots > 1 else ''}")
    st.write(f"Payload capacity per bot: {payload_capacity} kg")

if __name__ == "__main__":
    main()