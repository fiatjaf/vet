window.$          = require 'jquery'
window.superagent = require 'superagent'

if $('body').width() < $('table').width()
  $('<link rel="stylesheet" href="/static/tables-to-cards.css">').appendTo('head')

$('select[data-fk]').each ->
  sel = $(@)
  tablename = sel.data('fk')
  superagent.get("/_/foreign-key-options/#{tablename}/").end (err, res) ->
    if err
      console.log err
      return
    for optionpair in res.body.options
      name = optionpair[0]
      id   = optionpair[1]
      sel.append("<option value='#{id}'>#{name}</option>")
