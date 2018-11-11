# Ansible test

Make testinfra easier with ansible repository.

Write your test directly in your roles

## purpose of ansible-tests
I want to be able to write testinfra tests in my role and use my inventories and my playbooks to run them

## Usages

```
ansible-tests --file-name tests.yml --inventory inventory/dev.ini
```

## Test your ansible roles

Your tests should be in test directory inside your role :

```
nginx
    ├── defaults
    │   └── main.yml
    ├── handlers
    │   └── main.yml
    ├── tasks
    │   └── main.yml
    └── tests
        └── test_nginx.py

```

Example of test file :

```
# tests/test_nginx.py

def test_check_nginx_is_installed(host):
  nginx = host.package('nginx')
  assert nginx.is_installed

def test_nginx_is_running(host):
  nginx = host.service('nginx')
  assert nginx.is_running

```

Example of corersponding task file :

```
# tasks/main.yml
---
- name: install nginx
  package:
    name: nginx
    state: present

- name: start nginx
  service:
    name: nginx
    state: started
```


## Configure ansible-test

To run ansible test, you have to respect this requirements:
* your roles must be in `roles` directory
* you must have a playbook or a file to describe the matching between tests and servers


## tests.yml supported formats

```
- hosts: bdd
  roles: postgres
- hosts: all
  roles: secu
```

```
- hosts: all
  roles:
    - base
    - secu
```

```
- hosts:
  - bdd
  - web-app
  roles:
  - role: secu
  - role: users
```


```
- hosts: bdd:web-app
  roles:
  - role: secu
```

You should be able to use directly your playbook if you don't use stuff like `!group` to exclude some group
