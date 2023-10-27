import streamlit as st


def main():
    st.title("Quiz Application Interface")
    col1, col2 = st.columns(2)

context_template = col1.selectbox("Context Template", ["Story Cards"])

source_document_type = col2.selectbox("Source-Document-Type",
                                          ["Pick from asset library", "Text", "Document", "Video URL", "Web URL"])

    if source_document_type == "Text":
        text_content = st.text_area("Text Content")

    prompt = st.text_area("Prompt")

if st.button("Generate Storyboard"):
        generate_storyboard(context_template, source_document_type, prompt)


def generate_storyboard(context_template, source_document_type, prompt):
    st.subheader("Storyboard")

    num_rows = 5  # Number of rows of cards
    cards_per_row = 2  # Cards per row
    total_cards = num_rows * cards_per_row

for row in range(num_rows):
        row_cards = st.columns(cards_per_row)

    for card_number in range(row * cards_per_row, (row + 1) * cards_per_row):
            with row_cards[card_number % cards_per_row]:
                st.subheader(f"Card heading {card_number + 1}")
         card_heading = st.text_input(f"Card heading {card_number + 1}")
                card_body_type = st.selectbox(f"Card {card_number + 1} body type", ["Text", "Question", "Image"])
                card_body = st.text_area(f"Card {card_number + 1} body")


if __name__ == "__main__":
    main()
