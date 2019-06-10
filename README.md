# nodecreep

## meet nodecreep aka spaghetti-tron
![spaghetti-tron](https://bouldertrackerpics.s3.us-east-2.amazonaws.com/Screen+Shot+2019-06-09+at+9.23.14+PM.png)

#### a kubernetes node monitoring/slack integrated cronjob that runs on a baremetal cluster of raspberrys pi

## AKA the worlds most overengineered cronjob
every hour it spins up, starts, and stops a pod that queries the core api and gets node statuses and sends the information to a slack integration of your choosing
![nodecreep-message](https://bouldertrackerpics.s3.us-east-2.amazonaws.com/Screen+Shot+2019-06-09+at+9.15.55+PM.png)
###### made to be super easy to deploy onto raspberry pi kubernetes cluster
just apply the yamls and use [my armhf docker image](https://hub.docker.com/r/tpageforfunzies/nodecreep)
that runs the `nodecreep/creep.py` script from this repo, in a docker container buit from the `Dockerfile` in this repo.
# - set up
###### 1.  add kubeconfig to configmap for mounting
```
cat ~/.kube/config
```
copy and paste over the following in the `kubernetes/ConfigMap.yaml` file
```
# apiVersion: v1
# clusters:
# - cluster:
#     certificate-authority-data: STUFF AND JUNK
#     server: YOUR API URL HERE
#   name: kubernetes
# - cluster:
#     certificate-authority:
#     server:
#   name: minikube
# contexts:
# - context:
#     cluster: kubernetes
#     user:
# etc
# etc
```

###### 2.  add slack info to the cronjob yaml
replace the `value` fields in the following in the `kubernetes/CronJob.yaml` file
```
env:
- name: SLACK_WEBHOOK
  value: "INSERT FULL SLACK WEBHOOK URL HERE"
- name: FOOTER_ICON
  value: "https://bouldertrackerpics.s3.us-east-2.amazonaws.com/spaghetti-tron.png"
- name: SLACK_USERNAME
  value: "INSERT YOUR SLACK INTEGRATIONS USERNAME"
```
  now you're ready to deploy which is shown below
  <br>
  # deploy
  make sure you've updated the values in the 2 yaml files shown above and it just comes down to applying them both, the configmap then the cronjob
  ###### 1.  run the deploy script
  run `scripts/deploy.sh`
  ```
============================================
===     youre using nodecreep? sick.     ===
===  make sure you updated all the vars  ===
============================================


======deploying configmap======
configmap/nodecreep-configmap changed
======deploying cronjob======
cronjob.batch/nodecreep changed
```
###### 2.  verify
enter a (may have to specify namespace, if so it's `default`)
```
kubectl get all
```
and you should see something like the following at the bottom of the output
```
NAMESPACE   NAME                      SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
default     cronjob.batch/nodecreep   0 */1 * * *   False     0        22m             123m
```


###### a small aside
the [kubernetes ttl controller that will eventually clean up after this process](https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/) is only in alpha and currently featuregated.  
<br>
_remember when I called it over-engineered?_
<br>this means to clean up the pod and job created every hour by the kubernetes native cronjob I had to add an actual operating system cronjob to a node with kubectl access like so:
<br>
<br>
`crontab -e` and add the following to the bottom. this runs at the XXth (05 for the fifth for example) minute of every hour to clean up after the pods created by the cronjob which runs at the 00 minute of every hour, so you can give yourself time to check the pod's logs if you want
```
XX */1 * * * kubectl delete pods -l cron-part && kubectl delete jobs -l cron-part
```
