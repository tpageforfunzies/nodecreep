#!/usr/bin/
echo '============================================'
echo '===     youre using nodecreep? sick.     ==='
echo '===  make sure you updated all the vars  ==='
echo '============================================'
echo ''
echo ''
echo '======deploying configmap======'
kubectl apply -f kubernetes/ConfigMap.yaml
echo '======deploying cronjob======'
kubectl apply -f kubernetes/CronJob.yaml