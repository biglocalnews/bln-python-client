# Contributing

This documents guides you through how to make improvements to the `bln` library by installing its source code and suggesting improvements.

```{contents} Sections
  :depth: 1
  :local:
```

## Create a fork

Start by visiting our project’s repository at [github.com/biglocalnews/bln-python-client](https://github.com/biglocalnews/bln-python-client) and creating a fork. You can learn how from [GitHub’s documentation](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

## Clone the fork

Now you need to make a copy of your fork on your computer using GitHub’s cloning system. There are several methods to do this, which are covered in the [GitHub documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

A typical terminal command will look something like the following, with your username inserted in the URL.

```bash
git clone git@github.com:your-username/bln-python-client.git
```

or

```bash
gh repo clone your-username/bln-python-client
```

## Install dependencies

You should [change directory](https://manpages.ubuntu.com/manpages/trusty/man1/cd.1posix.html) into folder where you code was downloaded.

```bash
cd bln-python-client
```

The `pipenv` package manager can install all of the Python tools necessary to run and test our code. Since you’ll be using the special tools we need as part of code development, add the `--dev` flag.

```bash
pipenv install --dev
```

Now install `pre-commit` to run a battery of automatic quick fixes against your work.

```bash
pipenv run pre-commit install
```

## Create a branch

Next will we [create a branch](https://www.w3schools.com/git/git_branch.asp) in your local repository where you an work without disturbing the mainline of code.

You can do this by running a line of code like the one below. You should substitute a branch that summarizes the work you're trying to do.

```bash
git checkout -b your-branch-name
```

For instance, if you were trying to fix an upload bug, you might name it something like this:

```bash
git checkout-b upload-bug-fix
```

## Perform you work

Now you do your thing. Make the necessary changes to the code until you get the job done.

## Run tests

Before you submit your work for inclusion in the project, you should run our tests to identify bugs. Testing is implemented via pytest. Run the tests with the following.

```bash
make test
```

If any errors, arise, carefully read the traceback message to determine what needs to be repaired.

## Push to your fork

Once you're happy with your work and the tests are passing, you should commit your work and push it to your fork.

```bash
git commit -am "Describe your work here"
git push origin your-branch-name
```

## Send a pull request

The final step is to submit a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests>) to the main respository, asking the maintainers to consider integrating your patch. GitHub has [a short guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) that can walk you through the process. You should tag your issue number in the request so that they are linked in GitHub’s system.
