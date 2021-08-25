## EKS

To execute the yaml described Jobs, first create a cluster with eksctl

    $ eksctl create cluster --name python-ml-cluster --region us-east-2 --with-oidc -t t2.medium -m 2 -M 5 --ssh-access --ssh-public-key DIP --managed

Then, once it's done, apply the yaml

    $ kubectl apply -f docker-exp-<n>.yaml

And watch it with kubectl get

    $ kubectl get pods --all-namespaces

When done, delete cluster

    $ eksctl delete cluster python-ml-cluster