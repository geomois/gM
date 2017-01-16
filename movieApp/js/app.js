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
    .when('/overview', {
      controller: 'StartCtrl',
      templateUrl: 'templates/overview.htm'
    })
    .when('/time',{
      controller: 'TimerCtrl',
      templateUrl: 'templates/timer.htm'
    })
    .when('/overview'{
      controller: 'OverviewCtrl',
      templateUrl: 'templates/overview.htm'
    })
    .otherwise({
      redirectTo: 'start'
    });
});