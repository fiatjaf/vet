window.$ = require 'jquery'

if $('body').width() < $('table').width()
  $('<link rel="stylesheet" href="/static/tables-to-cards.css">').appendTo('head')
