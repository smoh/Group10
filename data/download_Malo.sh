#!/bin/bash

# Download Malo+2013 catalog of moving group members
wget -O Malo.tar.gz "http://vizier.cfa.harvard.edu/viz-bin/nph-Cat/tar.gz?J%2FApJ%2F762%2F88"
mkdir Malo && tar -xzvf Malo.tar.gz -C Malo
