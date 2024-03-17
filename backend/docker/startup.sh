#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# let's go!
gunicorn --config /app/gunicorn.conf.py api.wsgi:application
