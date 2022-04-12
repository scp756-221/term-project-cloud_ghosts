[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7089621&assignment_repo_type=AssignmentRepo)
# Team Cloud Ghosts
Term Project repo

## How To Bring Up The Cluster & Microservice

1. Inside c756-exer/cluster, make a copy of tpl-vars-blank.txt as tpl-vars.txt

Make the changes to the values inside (details of each parameter are in the same file):
ZZ-REG-ID=
ZZ-AWS-ACCESS-KEY-ID=
ZZ-AWS-SECRET-ACCESS-KEY=

Note: for security purpose, do not commit the tpl-vars.txt file to repository (this file is git ignored)

Then run 
~~~
make -f k8s-tpl.mak templates
~~~

2. Bring up the tooling with

~~~
./tool/shell.sh
~~~

3. Inside the new container, create all the template files needed with the following
/home/k8s# make -f k8s-tpl.mak templates
tools/process-templates.sh

4. Run the following to create the cluster

~~~
make -f eks.mak start
~~~

5. We can view the clusters with the following command:

~~~
/home/k8s# make -f allclouds.mak
~~~

6. Create the namespace

~~~
/home/k8s#  kubectl config use-context aws756
/home/k8s#  kubectl create ns c756ns
/home/k8s#  kubectl config set-context aws756 --namespace=c756ns
~~~

7. Build the images that will be used for deployment

~~~
/home/k8s# make -f k8s.mak cri
~~~

8. Install itsio:

~~~
/home/k8s# kubectl config use-context aws756
/home/k8s# istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
/home/k8s# kubectl label namespace c756ns istio-injection=enabled
~~~

9. Deploy all components all at once:

~~~
/home/k8s# make -f k8s.mak gw db s1 s2 s3
~~~

10. Load records with the following:

The csv files to modify are in the gatling/resource/ directory:
bestseller.csv
reader.csv
book.csv

~~~
/home/k8s# make -f k8s.mak loader
~~~


11. Run k9s to view that there are no errors

~~~
k9s
~~~

12. Provisioning

~~~
make -f k8s.mak provision
make -f k8s.mak kiali
~~~
