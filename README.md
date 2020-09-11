# Distributed Systems Project1

## Bogdanova Alina (BS18-SE02) & Dubina Nikita (BS18-SB01)

### Part 1. Docker.

1. **What is Docker-machine and what is it used for?**

Docker machine is a piece of software, which provides services for managing distinct docker hosts or a network of them.

2. **What is Docker Swarm, what is it used for and why is it important in Containers Orchestration?**

Docker Swarm is a cluster-management tool. It is important for the Containers Orchestration, because it improves system scalability. Docker Swarm joins several Docker-hosts in one virtual. It provides an API interface which is compatible with Docker API, and all the instruments, which are used by Docker’s API are working with Docker Swarm, moreover, they will think that they work with the one Docker machine, but in reality, they work with a cluster.

3. \*\*Install Docker-machine based on your virtualization platform (VirtualBox, Hyper-V, VMware), create a Machine (named Master), and collect some relevant information for you. Example:

-   Docker-machine drivers.
-   Docker-machine provisioning.
-   Experiment with some docker-machine commands (rm, stop, start commands).\*\*

Hyper-V was used as a virtualization platform.
Master machine was created, some info about it was collected, using commands:

```
docker-machine create --driver hyperv Master
```

```
$docker-machine inspect Master
```

Result:
![Docker machine inspect maste](./media/inspect_master.png)
Some commands were tested, e.g. create, rm, rm -f, start, stop, ssh

![Rm test](./media/docker-machine_rm_test.png)

4. **Create two Workers as well. Later we will connect them into one swarm. Make a screenshot for docker-machine ls command. You should have 3 running machines.**

```
docker-machine create --driver hyperv Worker1
docker-machine create --driver hyperv Worker2
```

Result of `docker ls command`:
![Docker ls](./media/docker_ls.png)

5. **Now that Docker Swarm is enabled, deploy a true container cluster farm across many Dockerized virtual machines. (One master and two workers). Verify the Docker Swarm status, identify the Master node(s), and how many workers active exist. Take as many screenshots as you need to explain the process.**

Create the swarm (on Master):

```
$docker swarm init --advertise-addr 192.168.1.27
```

![Swarm init master](./media/swarm_init_master.png)

Where `192.168.1.27` - Master’s ip address

Then, Workers should be connected to the swarm

Deploy container:

```
docker service create --replicas 2 -p 80:80 --name web nginx
```

--replicas - specification of amount of containers, which should be started

There also exist another way to deploy the app - docker stack.

```
docker stack deploy -c docker-compose.yaml web
```

![Docker stacke deploy](./media/docker_stack_create.png)

It creates two services, in our case: `web_web` and `web_redis`

Docker-compose.yaml:

```
version: '3'
services:
  web:
    Image: name/project1:v1
    ports:
      - "5000:5000"
  redis:
    image: "redis:alpine"
```

6. **How can a Worker be promoted to Master and vice versa? Please explain if special requirements are needed to perform this action? Perform the process and explain it.**

For worker to become master, this line should be run on the master:

```
$docker node promote Worker1
```

![Node promotion](./media/node_promotion_on_master.png)

![Worker1 becomes manager](./media/worker1_bacames_manager.png)
For master to become a worker, this line should be run on the master:

```
$docker node demote Worker1
```

![Depromotion of worker1](./media/depromotion_of_worker1.png)

![Depromote result](./media/swarm_depromote_worker1_result.png)

**Hint:** Check if worker nodes require the exact same system patch level.

7. **Deploy a simple Web page, e.g Nginx, showing the hostname of the host node it is running upon, and validate that its instances are spreading across the servers previously deployed on your farm.**

The commands, similar to 5 ex are runned here.
![Result nginx](./media/nginx.png) 8. **How to scale instances in the Docker Swarm? Could it be done automatically?**

If initially docker service was used to create the containers, then:

```
$docker service scale web=4
```

should be executed.

Scaling process:
![Scanning process](./media/scaling_process.png)

Scaling result:
![Scaling result](./media/scaling_result.png)
If `docker stack` was used, then the correct way is to update `docker-compose.yaml` file:

```
web:
	...
	deploy:
		replicas: 3
```

![Scale with stack](./media/scale_with_stack.png)

9. **Validate that when a node goes down a new instance is launched. Show how the redistribution of the instances can happen when the dead node comes back alive.**

Draining of the node:

```
$docker node update --availability drain Worker2
```

![Drain worker2](./media/drain_worker2.png)
As it can be seen, new nodes are created instead of old one, using other machines (master and worker1)

Returning back:

Availability changing:
![Worker2 returned to be active](./media/undrain_worker2.png)

```
$docker node update --availability active Worker2
```

From the docker [docs](https://docs.docker.com/engine/swarm/swarm-tutorial/drain-node/):

> When you set the node back to Active availability, it can receive new tasks:
>
> -   during a service update to scale up
> -   during a rolling update
> -   when you set another node to Drain availability
> -   when a task fails on another active node

Result of another node draining:

![Draining of worker 1](./media/second_drain_worker1.png)

(Redistribution on the activated Worker 2)

10. **Perform some update in your application, a minor change in your sample application for example. How to replicate the changes in the rest of the farm servers?**

If docker service was used to create the app:

```
$docker service update --image <imagename>:<version> web
```

Result:
![Update using docker service](./media/update_service.png)

Example of update on 2 nodes:

We can see the same process, as if nodes would be drained: nodes are shutdown and restarted

As a result, new image can be seen on all the

If `docker stack` was used initially:

10.1. Build and push new image (tagged with version)

10.2. Update docker-compose.yaml file (version)

10.3. Apply updates:

```
$ docker stack up -c docker-compose.yaml web
```

10.4. Check the result:

![Update](./media/update.png)

11. **It is a good practice to monitor performance and logs on your servers farm. How can this be done with Docker Swarm? Could it be just CLI or maybe GUI?**

To show the logs of the service (we have 2 of them), the command (CLI) `$docker service logs service_name` can be used
The result of the command can be seen on the following screenshots:
Web_web logs

![Web logs](./media/wed_logs.png)

Web_redis logs
![Redis logs](./media/redis_logs.png)

If we are talking about GUI, then it is also a good practice, because, for example, we have such good practice with Portainer and its experience with working on Swarm clusters. It provides all the information about logs, basic statistics and provides an ability to connect to the terminal from the Web. Also it can manage the containers, images, networks etc. So, this is a really good practice, exactly in use of Swarm, because it can show the state of Docker instances, which unites in the Swarm.

Example of such an interfase:
![GUI logs](./media/gui2.png)
![GUI logs](./media/gui1.png)

12. **Please explain what is “Out Of Memory Exception (OOME)”, how it could affect Docker services, and which configuration can be set to avoid this issue?**

OOME is the situation when your services or containers try to use more memory than you have in your system. On Docker services it can affect this way: some of Docker containers can be killed by the kernel of OOM service. To prevent this scenario, you can just be sure that your containers run on the hosts with sufficient memory.

13. **Deploy a docker container with at least 15% of CPU every second for memory efficiency.**

To change the CPU utilization the following changes should be applied to the docker-compose.yaml file:

![CPU limits](./media/cpu_limits.png)

14. **Verify the size of the Docker images that you're working with. Can this size be reduced and how can we achieve this?**

To findout the current size of images the following command can be used

```
$docker system df
```

Of course the image of the Docker image can be reduced. Max drastic approach to do this is the Multi-Stage build. The main idea of this approach is to exclude not necessary instruments like compilers of some language from the final image. We do not include all the instruments in the image, we just want to have a working binary file. We can exclude compilers, debugging tools, libs, shell etc.

We can exactly:

-   do not install debug tools like vim/curl
-   Minimize Layers (write RUN in small amount of stings)
-   Use `-- no-install-recommends` on `apt-get install`
-   Add `rm -rf /var/lib/apt/lists/*` to same layer as `apt-get install`

### Part 2. App.

15. **Instead of a simple web page in step 7 elaborate your own web application. Be creative. Again, interaction with a user is required.**

This is a decoder ["like Artemy Lebedev's"](https://www.artlebedev.ru/decoder/). This tool was created for changing the keyboard layout of printed text. This version supports only Russian->English and English->Russian decodings.

![Result](./media/result.png)

### References:

-   [Manager and Worker nodes descroption](https://docs.docker.com/engine/swarm/join-nodes/)
-   [Docker swarm + create service tutorial](https://rominirani.com/docker-swarm-tutorial-b67470cf8872)
-   [Node promotion](https://stackoverflow.com/questions/42412863/changing-node-to-manager-in-docker-swarm-what-command-should-i-use)
-   [OOME](https://docs.docker.com/config/containers/resource_constraints/)
