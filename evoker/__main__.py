import sys

def main():
    match sys.argv[1]:
        case "serve":
            import server
            server.main()
        case "train":
            import train
            train.train(int(sys.argv[2]))
        case "predict":
            import predict
            print(predict.predict(" ".join(sys.argv[2:])))

if __name__ == "__main__":
    main()