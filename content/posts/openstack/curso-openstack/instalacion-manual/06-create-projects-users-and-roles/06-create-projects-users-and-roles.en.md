---
title: "06 - Create domains, projects, users and roles in OpenStack"
date: 2025-11-23T12:00:00+00:00
description: "Learn how to organize your OpenStack environment by correctly creating domains, projects, users and roles."
tags: [openstack,installation,identity]
hero: images/openstack/instalacion-manual/crear-dominios-proyectos.png
weight: 6
---

Identity (Keystone) is OpenStack's authentication and authorization service. In this step I prepare the minimal Identity configuration we need to continue the installation and to test OpenStack.

Although the `default` domain already exists after `keystone-manage bootstrap`, I explicitly create the projects and users we use in the guides: `service` (for service users) and `demo` (for non‑admin user tests). I also create an example role and assign it to the `demo` user.

When I show passwords in examples it's for clarity; if you prefer, use `--password-prompt` to enter the password interactively and securely.

## Create the `service` project

As administrator, create the `service` project with:

```bash
openstack project create --domain default --description "Service Project" service
```

## Create the `demo` project

Create a `demo` project for tests and non‑admin usage:

```bash
openstack project create --domain default --description "Service Project" demo
```

## Create the `demo` user

Create the `demo` user in the `default` domain. In this example I show the password in clear (`demo`) for simplicity:

```bash
openstack user create --domain default --password demo demo
```

## Create a role and assign it to `demo` in the `demo` project

Create a role named `demo` and assign it to the `demo` user within the `demo` project:

```bash
openstack role create demo
openstack role add --project demo --user demo demo
```

## Example `demo-openrc` file and verification

Create a `demo-openrc` file with the environment variables for the `demo` user. Adapt it if your environment uses other URLs or domains:

```bash
cat > demo-openrc <<'EOF'
export OS_USERNAME=demo
export OS_PASSWORD=demo
export OS_PROJECT_NAME=demo
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller01:5000/v3
export OS_IDENTITY_API_VERSION=3
EOF
```

To verify authentication works with `demo`, source the variables and request a token:

```bash
source demo-openrc
openstack token issue
```

That concludes the basic configuration of projects, users and roles needed to continue with other services.
