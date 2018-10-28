var app = angular.module('AboutApp', [
  'ngMaterial',
]);

app.config(function($locationProvider, $httpProvider, $mdThemingProvider) {
    $locationProvider.html5Mode(true);
    $mdThemingProvider.theme('aliTheme')
        .primaryPalette('green');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('AliCtrl', function ($scope) {
   $scope.albums = [{name:'Ali1',desc:'3 month', link:'https://photos.app.goo.gl/hiYEb8ecrVfb1dgV7',
   img:''},
   {name:'Ali2',desc:'Ali in DC', link:'https://photos.app.goo.gl/bbrhK3zYpeDXJEKy8',img:''}];
});