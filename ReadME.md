


# Installation
Click on use Template at the top righthand corner of the screen which would create a repository for you.

After Cloning the repo we are down to usage.

## Usage

first thing is to set up your virtual environment. 

By way of illustration I will provide snippets to help you setup.

Ps. All commands below are terminal commands.



creating a virtualenv via venv
```
python3 -m venv {name of your env}
```

To activate your venv

```
source {name of your venv}/bin/activate
```



Please create a dotenv file for your environment variables. An example environment variable is provided. This file is called ```.example.env```.

Installing Requirements can be done by using this command.


```
pip install -r requirements.txt

```

Migrating DB with Alembic

```
alembic upgrade heads
```

Starting your Server

```
uvicorn src.app.main:app --reload

```

## PostMan Collection.

I create a postman collection that can be forked for testing. here -> https://documenter.getpostman.com/view/17138168/2s93CGRbQg


## Contributing
There are few things that need to be worked on, they are 

1. Testing: I will be writting a comprehensive overwhelmingly encompassing test case which will cover every case especially edge cases. I would love to learn to write good test so I am willing to partner with engineers on this.

Intialy I was looking forward to writting test that handles edge cases oe exception block in place, however for now I am testing best case. 

What are the best cases? These are the apporiate response during the req-res cycle without any HTTPEception.


PR are welcome, For major changes, please open an issue first
to discuss what you would like to change.
