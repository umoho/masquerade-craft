# MasqueradeCraft

A Pseudo Minecraft Server

## Descriptions

This simple program will accept Minecraft client (version 1.18.2) requests and then response.

When client ping the server, return a motd.

When player try to join the server, return a `Disconnect` packet to refuse.

## Usage

Simply use the following command at the path:

```bash
python .
```

## Configurations

If `conf.yml` doesn't exist, it will use default built-in configurations, and then creates a `conf.yml` when started.
