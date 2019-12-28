# Useful Scripts for Linux and Python
General Linux/Python scripts for various purposes

- This folder has several folders, each with miscellaneous scripts and setups for different tasks.
```
----- /1_settings         # setups for linux environments
  |-- /2_simple_scripts   # scripts for common linux utility
  |-- /3_simple_plot      # scripts for very simple plotting
```

#######################################################################################
# Initializing a new Linux (Ubuntu) with common packages
```
> apt-get.csh
    [update|build|noness|python|science|java]
       
     update:  update/upgrade currently installed packages
     build:   install essential "build" linux packages
     noness:  install non-essential linux packages
     science: install "science"-related linux packages
     python:  install often-used python pacakges, including Conda packages
     java:    install Java OpenJDK and Oracle
     Other:   inside this script, there are list of RStudio and Conda packages
```

#######################################################################################
# Personalized linux .tcshrc/.cshrc and .vimrc scripts, etc.
```
> cshrc    # for csh and tcsh
> vimrc
> pymolrc
```
* add "." to convert them to system scripts .cshrc and .vimrc

#######################################################################################
# Miniconda settings
- Save an existing conda environment to a .yml file:
```
> conda activate <environment name>
> conda env export | grep -v "^prefix: " > <saved environment>.yml
```

- Create a new environment using a .yml file:
```
> conda env create --name <new environment> --file=<saved environment>.yml
```

#######################################################################################
# Create link between GitHub server and Visual Studio Code
**Link to GitHub**

- Create a link between your computer and GitHub server by first getting the RSA SSH key from the terminal by using **ssh_keygen**. When prompt, enter **nothing** to the questions. This will generate a key stored in the file **id_rsa** in **~/.ssh**. Copy the SSH key.
```
> ssh-keygen

Generating public/private rsa key pair.
Enter file in which to save the key (/home/ylo/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/ylo/.ssh/id_rsa.
Your public key has been saved in /home/ylo/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:Up6KjbnEV4Hgfo75YM393QdQsK3Z0aTNBz0DoirrW+c ylo@klar
The key's randomart image is:
+---[RSA 2048]----+
|    .      ..oo..|
|   . . .  . .o.X.|
|    . . o.  ..+ B|
|   .   o.o  .+ ..|
|    ..o.S   o..  |
|   . %o=      .  |
|    @.B...     . |
|   o.=. o. . .  .|
|    .oo  E. . .. |
+----[SHA256]-----+

> cat ~/.ssh/id_rsa
ssh-rsa FOW9TUQ2J09Jqp4t0u009UGQ0409QJA.... <username>@<localhost>
```
- In GitHub website, under **User** --> **Settings** --> **SSH and GPG keys**, add via **New SSH key**. Will need to do this for every computer to link to GitHub.

> ---
**Upload files to GitHub**

- In GitHub website, create a new repository.
- In the empty repository, in the green "Clone or download", copy the SSH key in "Use SSH"
- In the shell terminal, go to the folder that will be linked to the Github.

```
> cd repository_folder/
> git init
> git remote add origin <SSH key of the GitHub repository>
> git pull origin master
> code .
```
- Once VSCode is open in the folder, via the **Source Control** tab (Ctrl+Shift+G), **Stage Change (+)** to single or all files, then **Commit** (Check mark), then in the _lower left corner_ click the _"cloud-looking thing"_ to upload changes made to the files to GitHub. After the first submit, the _"cloud-looking thing"_ will change into a _"cycle-looking thing"_.
