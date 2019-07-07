# infrastructure-designer
reading, visualizing, creating CloudFormation

###

This is based on reading 
[Amazon Web Services in Action](https://www.amazon.com/Amazon-Services-Action-Andreas-Wittig/dp/1617295116/ref=pd_lpo_sbs_14_t_0?_encoding=UTF8&psc=1&refRID=3TH0HSPX33YHF137EKWC) which has lots of fairly complex, working architectures, that will create the infrastructure and run on AWS.

Here I'm going with the idea that the infrastructure specification is a graph, and that aspects of the architecture are subgraphs.

So in theory, I can load a CloudFormation into a graph.  Since the
graph is a complete specification of the infrastructure, both analyzing
a graph and modifying the graph are operations on the infrastructure.

##### Using Visitors to Query a Tree

Suppose I want to know the following about a cloudformation configuration:

- What is my attack surface at the port level?
  - is my VPC internet accessible?
  - do I have private subnets?
  - is communication restricted by ports?  security groups?  network ACLs?
- What is my fault tolerance?
  - which resources can fail?  which recover from failure?  which don't fail?
  - does architecture detect and recover from failure?
- Is my infrastructure scalable?
  - are scaling metric used?
  - are there scaling up/scaling down patterns?
  - is there a measurement of need to scale up or down?

##### Using Visitors to Modify a Tree

Suppose I want to have these components in my architecture:

- bastion host in its own subnet accessing all my EC2 instances

