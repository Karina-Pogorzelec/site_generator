from textnode import TextNode, TextType

def main():
    randomo = TextNode("This is some anchor text", TextType.text_link, "https://www.boot.dev")
    print(randomo)



if __name__ == "__main__":
    main()
