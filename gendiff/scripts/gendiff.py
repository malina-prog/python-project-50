import argparse

def main():
    parser = argparse.ArgumentParser(description="Compares two configuration files and shows a difference.")
    parser.add_argument('first_file', type=str,)
    parser.add_argument('second-file', type=str,)
    parser.add_argument("-f", "--format",help="Set format of output.",default="stylish",)

    args = parser.parse_args()
    
if __name__ == "__main__":
    main()