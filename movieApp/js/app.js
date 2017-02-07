

var app = angular.module('mimeApp', ['ngCookies','ngRoute']);

app.config(function ($routeProvider) {
  $routeProvider
    .when('/game', {
      controller: 'GameCtrl',
      templateUrl: 'templates/game.htm'
    })
    .when('/start', {
      controller: 'StartCtrl',
      templateUrl: 'templates/start.htm'
    })
    .when('/time',{
      controller: 'TimerCtrl',
      templateUrl: 'templates/timer.htm'
    })
    .when('/overview',{
      controller: 'OverviewCrtl',
      templateUrl: 'templates/overview.htm'
    })
    .otherwise({
      redirectTo: '/overview'
    });
});