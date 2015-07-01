#!/bin/sh

mypath=$(cd `dirname $0` && pwd)

params="$mypath/uwsgi.ini"

uwsgi $params
