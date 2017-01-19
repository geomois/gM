// JavaScript Document
var app = angular.module('myApp', []);

app.config(['$sceDelegateProvider', function($sceDelegateProvider) {
  // We must whitelist the JSONP endpoint that we are using to show that we trust it
  $sceDelegateProvider.resourceUrlWhitelist([
    'self',
    '../data/movieData.json'
  ]);
  }]);