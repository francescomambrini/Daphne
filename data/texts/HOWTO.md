# Hook Tests - How to

## What are Hook Tests?

A series of validation tests to verify that your TEI/Epidoc CTS-compliant texts 
validate against the [CapiTainS Guidelin](http://capitains.org/pages/guidelines).

## How do I run them?

The easiest thing is to use Docker (easiest, that is, if you already have Docker 
installed...). Here is how you do it:

### Setting up the hooktest docker container

* [Install Docker](https://docs.docker.com/install/), but hopefully you already have it, righ?
* Build and run the `hooktest` docker container

Run the following command to build the contaier (it will download some data from the internet):

```bash
`docker run -i --name hooktest -v /path/to/Daphne/data:/sources capitains/hooktest:latest`
```

(note that you may also have to run the docker command as sudo, depending on how you 
set up your docker environment: see [here](https://docs.docker.com/install/linux/linux-postinstall/))

Now you're running an interactive shell within the container. 
Note that you only need to run the `docker run` command once (that is, unless you 
decide to bind a different folder to the `/source` directory in the container). 
From the second time, in order to access the interactive shell of the container 
you only need to enter:

```bash
docker start -i hooktest
```

### Run the tests

The prompt is really minimalistic! But if you entered the `docker run` command above, 
you now have your basic data folder (the one with texts, annotation, and notes: see below) 
in the `/sources` directory of the container.

Try: `ls /sources`; if it mirrors your `Daphne/data` directory, you're good to go!

Then, the test itself is performed with:

```bash
./epidoc.sh texts/

```

(yes, give the relative path to `/sources` dir!)

The script will output a basic report on screen; more detailed information is written on 
the `result.json` and `results.html` files. In Linux, those files are owned by the `root` user 
and that's a bit annoying. See [here](https://stackoverflow.com/questions/27925006/share-files-between-host-system-and-docker-container-using-specific-uid) 
for possible solutions.

### What the heck is a `texts/data` folder doing within a `data` folder?!?

I know, it's confusing! However, I set up the Daphne project as a general repository of 
tools and texts dealing with complex linguistic annotation of Greek poetry. It seemed 
only natural to me to set it up with a basic structure distinguishing: scripts, documentation, 
data, each in its own directory. The first `/data` folder is then organized to hold: editions, annotations and commentaries.

This seemed straightforward. However, I discovered later that the CaPiTains guidelines 
require your CTS repository of editions to also have all your Epidoc texts into a folder named 
`data`.

Hence the repetion... It's not very neat, but I don't know what else to do.

