import sys

def main():
    action = sys.argv[1]
    if action == "serve":
        import server
        server.main()
    elif action == "train":
        import train
        train.train(int(sys.argv[2]))
    elif action == "predict":
        import predict
        for _ in range(10):
            print(predict.predict(" ".join(sys.argv[2:])))

if __name__ == "__main__":
    main()