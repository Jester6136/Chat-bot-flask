import random
import json
import torch
from model import NeuralNet
from language_utils import convert_to_vec,tokenize,normalization_text


device =torch.device('cpu')

with open('intents.json','r') as f:
    intents = json.load(f)

FILE = 'data.pth'
data = torch.load(FILE)

input_size = data['input_size']
output_size = data['output_size']
hidden_size = data['hidden_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size=input_size,hidden_size=hidden_size,num_classes=output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sabow"

def response_msg(msg):
    sentence = normalization_text(msg)
    sentence = tokenize(sentence)

    X = convert_to_vec(sentence,all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)

    _,predicted = torch.max(output,dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output,dim =1)
    prob = probs[0][predicted.item()]

    if prob.item() >0.8:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return " I do not understand... "

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = response_msg(sentence)
        print(resp)