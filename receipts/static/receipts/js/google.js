//var app = angular.module('ReceiptsApp', []);
//
//var init = function() {
//  window.initGapi();
//}
//
//app.controller('MainController', function($scope, $window, gapiService) {
//  var postInitiation = function() {
//    // load all your assets
//  }
//  $window.initGapi = function() {
//    gapiService.initGapi(postInitiation);
//  }
//});
//
//app.service('gapiService', function() {
//  this.initGapi = function(postInitiation) {
//    gapi.client.load('helloWorld', 'v1', postInitiation, restURL);
//  }
//});