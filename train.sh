#! /bin/sh

CURRENT=$(cd $(dirname $0);pwd)

cd $CURRENT && screen -dmS mxfont python train.py cfgs/train_jp.yaml
