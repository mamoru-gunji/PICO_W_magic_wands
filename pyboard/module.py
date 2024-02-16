def print_filename():
    print(__name__)

if __name__ == "__main__":
    print("This is being run directly as", __name__)
else:
    print("This is being imported from", __name__)
