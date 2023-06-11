import copy
import json
import os
import pickle
import time
from collections import OrderedDict

import numpy as np
import PIL
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import zmq
from minio import Minio
from PIL import Image
from torch import nn, optim
from torch.autograd import Variable
from torch.optim import lr_scheduler
from torch.utils.data.sampler import SubsetRandomSampler
from torchvision import datasets, models, transforms


def main(model_name, epochs):
    # check if GPU is available
    train_on_gpu = torch.cuda.is_available()

    if not train_on_gpu:
        print("Bummer!  Training on CPU ...")
    else:
        print("You are good to go!  Training on GPU ...")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_dir = "flower_data"
    train_dir = data_dir + "/train"
    valid_dir = data_dir + "/valid"

    # Define your transforms for the training and testing sets
    data_transforms = {
        "train": transforms.Compose(
            [
                transforms.RandomRotation(30),
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
        "valid": transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
    }

    # Load the datasets with ImageFolder
    image_datasets = {
        x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
        for x in ["train", "valid"]
    }

    # Using the image datasets and the trainforms, define the dataloaders
    batch_size = 64
    dataloaders = {
        x: torch.utils.data.DataLoader(
            image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=4
        )
        for x in ["train", "valid"]
    }

    class_names = image_datasets["train"].classes

    dataset_sizes = {x: len(image_datasets[x]) for x in ["train", "valid"]}
    class_names = image_datasets["train"].classes

    print(dataset_sizes)
    print(device)

    # Label mapping
    with open("cat_to_name.json", "r") as f:
        cat_to_name = json.load(f)

    # Run this to test the data loader
    images, labels = next(iter(dataloaders["train"]))
    images.size()

    # # Run this to test your data loader
    images, labels = next(iter(dataloaders["train"]))
    rand_idx = np.random.randint(len(images))
    # print(rand_idx)
    print(
        "label: {}, class: {}, name: {}".format(
            labels[rand_idx].item(),
            class_names[labels[rand_idx].item()],
            cat_to_name[class_names[labels[rand_idx].item()]],
        )
    )

    if model_name == "densenet":
        model = models.densenet161(pretrained=True)
        num_in_features = 2208
        # print(model)
    elif model_name == "vgg":
        model = models.vgg19(pretrained=True)
        num_in_features = 25088
        # print(model.classifier)
    else:
        print("Unknown model, please choose 'densenet' or 'vgg'")

    # Create classifier
    for param in model.parameters():
        param.requires_grad = False

    def build_classifier(num_in_features, hidden_layers, num_out_features):
        classifier = nn.Sequential()
        if hidden_layers == None:
            classifier.add_module("fc0", nn.Linear(num_in_features, 102))
        else:
            layer_sizes = zip(hidden_layers[:-1], hidden_layers[1:])
            classifier.add_module("fc0", nn.Linear(num_in_features, hidden_layers[0]))
            classifier.add_module("relu0", nn.ReLU())
            classifier.add_module("drop0", nn.Dropout(0.6))
            classifier.add_module("relu1", nn.ReLU())
            classifier.add_module("drop1", nn.Dropout(0.5))
            for i, (h1, h2) in enumerate(layer_sizes):
                classifier.add_module("fc" + str(i + 1), nn.Linear(h1, h2))
                classifier.add_module("relu" + str(i + 1), nn.ReLU())
                classifier.add_module("drop" + str(i + 1), nn.Dropout(0.5))
            classifier.add_module(
                "output", nn.Linear(hidden_layers[-1], num_out_features)
            )

        return classifier

    hidden_layers = None  # [4096, 1024, 256][512, 256, 128]

    classifier = build_classifier(num_in_features, hidden_layers, 102)
    print(classifier)

    # Only train the classifier parameters, feature parameters are frozen
    if model_name == "densenet":
        model.classifier = classifier
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adadelta(
            model.parameters()
        )  # Adadelta #weight optim.Adam(model.parameters(), lr=0.001, momentum=0.9)
        # optimizer_conv = optim.SGD(model.parameters(), lr=0.0001, weight_decay=0.001, momentum=0.9)
        sched = optim.lr_scheduler.StepLR(optimizer, step_size=4)
    elif model_name == "vgg":
        model.classifier = classifier
        criterion = nn.NLLLoss()
        optimizer = optim.Adam(model.classifier.parameters(), lr=0.0001)
        sched = lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.1)
    else:
        pass

    # Adapted from https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
    def train_model(model, criterion, optimizer, sched, num_epochs=5):
        since = time.time()

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print("Epoch {}/{}".format(epoch + 1, num_epochs))
            print("-" * 10)

            # Each epoch has a training and validation phase
            for phase in ["train", "valid"]:
                if phase == "train":
                    model.train()  # Set model to training mode
                else:
                    model.eval()  # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == "train"):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        if phase == "train":
                            # sched.step()
                            loss.backward()

                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]

                print(
                    "{} Loss: {:.4f} Acc: {:.4f}".format(phase, epoch_loss, epoch_acc)
                )

                # deep copy the model
                if phase == "valid" and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

            print()

        time_elapsed = time.time() - since
        print(
            "Training complete in {:.0f}m {:.0f}s".format(
                time_elapsed // 60, time_elapsed % 60
            )
        )
        print("Best val Acc: {:4f}".format(best_acc))

        # load best model weights
        model.load_state_dict(best_model_wts)

        return model

    model.to(device)
    model = train_model(model, criterion, optimizer, sched, epochs)

    # Evaluation
    model.eval()

    accuracy = 0

    for inputs, labels in dataloaders["valid"]:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)

        # Class with the highest probability is our predicted class
        equality = labels.data == outputs.max(1)[1]

        # Accuracy is number of correct predictions divided by all predictions
        accuracy += equality.type_as(torch.FloatTensor()).mean()

    print("Test accuracy: {:.3f}".format(accuracy / len(dataloaders["valid"])))

    # Saving the checkpoint
    model.class_to_idx = image_datasets["train"].class_to_idx

    checkpoint = {
        "input_size": 2208,
        "output_size": 102,
        "epochs": epochs,
        "batch_size": 64,
        "model": models.densenet161(pretrained=True),
        "classifier": classifier,
        "scheduler": sched,
        "optimizer": optimizer.state_dict(),
        "state_dict": model.state_dict(),
        "class_to_idx": model.class_to_idx,
    }

    torch.save(checkpoint, "checkpoint_ic_d161.pth")

    minio_client = Minio(
        "localhost:8005",
        access_key="minio",
        secret_key="minio123",
        secure=False,
    )

    print(f"Uploading to minio: 'flower-data.{model_name}_{epochs}_checkpoint.pth'")
    minio_client.fput_object(
        "flower-data",
        object_name=f"flower-data.{model_name}_{epochs}_checkpoint.pth",
        file_path="checkpoint_ic_d161.pth",
    )


if __name__ == "__main__":
    # model_names = ["densenet", "vgg"]
    # main(model_name=model_names[0], epochs=1)

    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.connect("tcp://0.0.0.0:5005")

    while True:
        socket.send(b"RDY")
        _ = socket.recv_json()
        print("RCVD workload")
