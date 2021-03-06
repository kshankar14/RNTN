#!/bin/sh

# Dataset
if [ -d "trees" ]; then
    echo ":: Dataset already downloaded"
else
    echo ":: Downloading dataset..."
    DATASET_ZIP=trainDevTestTrees_PTB.zip
    wget -c https://nlp.stanford.edu/sentiment/${DATASET_ZIP}
    echo ":: Extracting dataset into 'trees' folder..."
    unzip ${DATASET_ZIP}
    rm ${DATASET_ZIP}
fi

# Create a folder for storing models
if [ -d "models" ]; then
    echo ":: 'models' directory already created"
else
    echo ":: Creating 'models' directory to store models..."
    mkdir -p models
fi
