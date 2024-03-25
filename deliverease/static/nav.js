const $routesLink = $('#routes-link')
const $stopsLink = $('#stops-link')
const $driversLink = $('#drivers-link')
const $customerslink = $('#customers-link')
const $adminsLink = $('#admin-link')
const $addCust = $('#add-cust')

const navlinks = [
    $routesLink,
    $stopsLink,
    $driversLink,
    $customerslink,
    $adminsLink
]

$routesLink.on('click', function() {
    hideAll(forms)
    $routes.show()
})

$stopsLink.on('click', function (){
    hideAll(forms)
    $stops.show()
});

$driversLink.on('click', function(){
    hideAll(components)
    $drivers.show()
})
$stopsLink.on('click', function(){
    hideAll(components)
    $stops.show()
})
$routesLink.on('click', function(){
    hideAll(components)
    $routes.show()
})
$adminsLink.on('click', function(){
    hideAll(components)
    $admins.show()
})

$addCust.on('click', function(){
    $search.hide();
    $custForm.show()
})

$('.navbar-collapse .nav-item').click(function(){
    $(".navbar-collapse").collapse('hide');
});