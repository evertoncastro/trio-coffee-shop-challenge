# Trio Coffee Shop Challenge

This repository contains a Django application for managing orders and customization of products. The application provides a REST API that allows managers to customize products and order statuses, while customers can place orders, customize their orders, and view order details. 


## Dependencies
- Python 3.10.11
- docker-compose


## Setup  

```
pip install virtualenv
```  

```
virtualenv env
```

```
source env/bin/activate
```

```
pip install -r requirements.txt
```


```
make run-server
```

## Tests

```
make run-tests
```

## Linter

```
make run-flake8
```

```
make formater
```